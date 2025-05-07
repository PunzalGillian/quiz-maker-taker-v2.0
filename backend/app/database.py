import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

class Database:
    def __init__(self):
        # Configure logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Load environment variables
        load_dotenv()

        # MongoDB connection settings
        self.MONGODB_URL = os.getenv("MONGODB_URL")
        self.DB_NAME = os.getenv("DB_NAME", "quizzes_db")

        # Verify MongoDB URL exists
        if not self.MONGODB_URL:
            self.logger.error("MONGODB_URL not found in .env file!")
            self.logger.error("Please configure MONGODB_URL in your .env file")
            raise ValueError("MONGODB_URL is not configured")

        # Initialize MongoDB client
        self.client = None
        self.database = None
        self.quizzes_collection = None

    async def connect(self):
        """Establish a connection to the MongoDB database."""
        try:
            self.client = AsyncIOMotorClient(self.MONGODB_URL, serverSelectionTimeoutMS=5000)
            self.database = self.client[self.DB_NAME]
            self.quizzes_collection = self.database.quizzes

            # Log connection information (without exposing credentials)
            connection_url_parts = self.MONGODB_URL.split('@')
            if len(connection_url_parts) > 1:
                # Hide username and password in logs
                safe_url = f"mongodb+srv://****:****@{connection_url_parts[1]}"
            else:
                safe_url = self.MONGODB_URL
            self.logger.info(f"MongoDB configured with: {safe_url}")

            # Ensure indexes are created
            await self.quizzes_collection.create_index("quiz_name", unique=True)
            self.logger.info("Indexes created successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB connection: {e}")
            raise

    async def disconnect(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")

    async def get_all_quizzes(self):
        """Get all quizzes from the database."""
        cursor = self.quizzes_collection.find({})
        quizzes = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            quizzes.append(document)
        return quizzes

    async def get_quiz_by_name(self, quiz_name):
        """Get a quiz by name."""
        quiz = await self.quizzes_collection.find_one({"quiz_name": quiz_name})
        if quiz:
            quiz["id"] = str(quiz["_id"])
        return quiz

    async def save_quiz(self, quiz_data):
        """Save a quiz to the database."""
        result = await self.quizzes_collection.insert_one(quiz_data)
        return result.inserted_id

    async def delete_quiz(self, quiz_name):
        """Delete a quiz by name."""
        result = await self.quizzes_collection.delete_one({"quiz_name": quiz_name})
        return result.deleted_count > 0

    async def get_quiz_by_id(self, quiz_id):
        """Get a quiz by ID."""
        try:
            quiz_obj_id = ObjectId(quiz_id)
            quiz = await self.quizzes_collection.find_one({"_id": quiz_obj_id})
            if quiz:
                quiz["id"] = str(quiz["_id"])
            return quiz
        except Exception as e:
            self.logger.error(f"Error getting quiz by ID {quiz_id}: {e}")
            return None