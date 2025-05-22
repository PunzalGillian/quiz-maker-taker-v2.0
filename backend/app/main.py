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


class QuizApp:
    """Main Quiz API application class"""

    def __init__(self):
        """Initialize the Quiz application"""
        # Load configuration
        self._mongodb_url = os.getenv(
            "MONGODB_URL", "mongodb://localhost:27017")
        self._db_name = os.getenv("DB_NAME")
        self._host = os.getenv("HOST", "0.0.0.0")
        self._port = int(os.getenv("PORT", "8000"))
        self._debug = os.getenv("DEBUG", "False").lower() == "true"

        # Create FastAPI app
        self.app = FastAPI(
            title="Quiz API",
            description="API for creating and taking quizzes",
            version="1.0.0",
            lifespan=self._lifespan
        )

        # Configure app
        self._setup_cors()
        self._setup_routes()
        self._setup_endpoints()

    @asynccontextmanager
    async def _lifespan(self, app):
        """Lifespan context manager for database connections"""
        try:
            app.mongodb_client = AsyncIOMotorClient(
                self._mongodb_url,
                serverSelectionTimeoutMS=5000  # Add timeout
            )
            # Test connection
            await app.mongodb_client.admin.command('ping')
            app.mongodb = app.mongodb_client[self._db_name]
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

    def _setup_cors(self):
        """Set up CORS middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",
                "https://quiz-creator-v2.netlify.app",
                "http://localhost:3000",
                "*"
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        """Set up API routes"""
        self.app.include_router(quiz_router)

    def _setup_endpoints(self):
        """Set up basic API endpoints"""

        @self.app.get("/")
        async def root():
            return {
                "message": "Quiz API is running with MongoDB",
                "endpoints": {
                    "GET /quizzes": "List all available quizzes",
                    "GET /quizzes/name/{quiz_name}": "Get quiz details by name",
                    "GET /quizzes/id/{quiz_id}": "Get quiz details by ID",
                    "POST /quizzes": "Create a new quiz",
                    "POST /quizzes/{quiz_name}/submit": "Submit answers and get results",
                    "DELETE /quizzes/{quiz_name}": "Delete a quiz"}}

        @self.app.get("/health")
        async def health_check():
            # Check if MongoDB is connected
            is_db_connected = hasattr(
                self.app, "mongodb_client") and self.app.mongodb_client is not None
            return {"status": "healthy", "database_connected": is_db_connected}

    def run(self):
        """Run the application"""
        uvicorn.run(
            self.app,
            host=self._host,
            port=self._port,
            reload=self._debug
        )


# Create app instance
quiz_app = QuizApp()
app = quiz_app.app

# Run when directly executed
if __name__ == "__main__":
    quiz_app.run()
