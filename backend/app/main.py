import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routes.quizzes import router as quiz_router


class QuizAPI:
    def __init__(self):
        # Configure logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Load environment variables
        load_dotenv()

        # MongoDB connection settings
        self.MONGODB_URL = os.getenv("MONGODB_URL")
        self.DB_NAME = os.getenv("DB_NAME", "quizzes_db")

        # Initialize FastAPI app
        self.app = FastAPI(
            title="Quiz API",
            description="API for creating and taking quizzes",
            version="1.0.0",
            lifespan=self.lifespan
        )

        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",
                "https://your-deployed-frontend.com",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Include routers
        self.app.include_router(quiz_router)

        # Add routes
        self.add_routes()

    @asynccontextmanager
    async def lifespan(self, app):
        try:
            app.mongodb_client = AsyncIOMotorClient(
                self.MONGODB_URL or "mongodb://localhost:27017",
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            await app.mongodb_client.admin.command('ping')
            app.mongodb = app.mongodb_client[self.DB_NAME]
            await app.mongodb.quizzes.create_index("quiz_name", unique=True)
            self.logger.info("Connected to MongoDB!")
        except Exception as e:
            self.logger.error(f"MongoDB connection error: {e}")
            app.mongodb_client = None
            app.mongodb = None

        yield

        if app.mongodb_client:
            app.mongodb_client.close()
            self.logger.info("MongoDB connection closed")

    def add_routes(self):
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
                    "DELETE /quizzes/{quiz_name}": "Delete a quiz"
                }
            }

        @self.app.get("/health")
        async def health_check():
            is_db_connected = hasattr(self.app, "mongodb_client") and self.app.mongodb_client is not None
            return {"status": "healthy", "database_connected": is_db_connected}

    def run(self):
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        debug = os.getenv("DEBUG", "False").lower() == "true"

        # Run the app
        import uvicorn
        uvicorn.run(self.app, host=host, port=port, reload=debug)


if __name__ == "__main__":
    # Instantiate and run the QuizAPI
    quiz_api = QuizAPI()
    quiz_api.run()