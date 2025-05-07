import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List
from .routes.quizzes import router as quiz_router
from .database import Database
from .utils import QuizFileManager


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

        # Initialize database
        self.db = Database()

        # Initialize file manager
        self.file_manager = QuizFileManager()

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
            # Connect to the database
            await self.db.connect()
            app.mongodb = self.db.database
            self.logger.info("Connected to MongoDB!")
        except Exception as e:
            self.logger.error(f"MongoDB connection error: {e}")
            app.mongodb = None

        yield

        # Disconnect from the database
        await self.db.disconnect()

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
                    "DELETE /quizzes/{quiz_name}": "Delete a quiz",
                    "POST /quizzes/save": "Save a quiz to a file",
                    "GET /quizzes/load/{quiz_name}": "Load a quiz from a file"
                }
            }

        @self.app.get("/health")
        async def health_check():
            is_db_connected = hasattr(self.app, "mongodb_client") and self.app.mongodb_client is not None
            return {"status": "healthy", "database_connected": is_db_connected}

        @self.app.get("/quizzes")
        async def get_quizzes():
            return await self.db.get_all_quizzes()

        @self.app.post("/quizzes/save")
        async def save_quiz(quiz_name: str, questions: List[dict]):
            file_path = self.file_manager.save_quiz(quiz_name, questions)
            return {"message": f"Quiz saved to {file_path}"}

        @self.app.get("/quizzes/load/{quiz_name}")
        async def load_quiz(quiz_name: str):
            quiz_data = self.file_manager.load_quiz(quiz_name)
            if not quiz_data:
                return {"error": "Quiz not found"}, 404
            return {"quiz": quiz_data}

    def run(self):
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        debug = os.getenv("DEBUG", "False").lower() == "true"

        # Run the app
        import uvicorn
        uvicorn.run(self.app, host=host, port=port, reload=debug)

quiz_api = QuizAPI()
quiz_api.run()