import os
import sys
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from .routes.quizzes import router as quiz_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")

# Define lifespan context manager


@asynccontextmanager
async def lifespan(app):
    try:
        app.mongodb_client = AsyncIOMotorClient(
            MONGODB_URL or "mongodb://localhost:27017",
            serverSelectionTimeoutMS=5000  # Add timeout
        )
        # Test connection
        await app.mongodb_client.admin.command('ping')
        app.mongodb = app.mongodb_client[DB_NAME]
        await app.mongodb.quizzes.create_index("quiz_name", unique=True)
        logger.info("Connected to MongoDB!")
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
        # Still allow the app to start without MongoDB
        app.mongodb_client = None
        app.mongodb = None

    yield

    if app.mongodb_client:
        app.mongodb_client.close()
        logger.info("MongoDB connection closed")

# Create FastAPI app with lifespan
app = FastAPI(
    title="Quiz API",
    description="API for creating and taking quizzes",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://quiz-creator-v2.netlify.app/",  # Add any other URLs
        "*"  # Or use this during development to allow all origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quiz_router)

# Use environment variables
app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
app.mongodb = app.mongodb_client[DB_NAME]


@app.get("/")
async def root():
    return {
        "message": "Quiz API is running with MongoDB",
        "endpoints": {
            "GET /quizzes": "List all available quizzes",
            "GET /quizzes/name/{quiz_name}": "Get quiz details by name",
            "GET /quizzes/id/{quiz_id}": "Get quiz details by ID",
            "POST /quizzes": "Create a new quiz",
            "POST /quizzes/{quiz_name}/submit": "Submit answers and get results",
            "DELETE /quizzes/{quiz_name}": "Delete a quiz"
        }
    }


@app.get("/health")
async def health_check():
    # Check if MongoDB is connected
    is_db_connected = hasattr(
        app, "mongodb_client") and app.mongodb_client is not None
    return {"status": "healthy", "database_connected": is_db_connected}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    # Run the app directly
    import uvicorn
    uvicorn.run(app, host=host, port=port, reload=debug)
