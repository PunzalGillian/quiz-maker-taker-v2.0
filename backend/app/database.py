import os
import sys
import logging
from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "quizzes_db")


class Database:
    """MongoDB database connection and operations"""

    def __init__(self, url, db_name):
        self._url = url
        self._db_name = db_name
        self._client = None
        self._database = None
        self._quizzes = None
        self._connect()

    def _connect(self):
        """Connect to MongoDB database"""
        try:
            # Create MongoDB client with a timeout
            self._client = AsyncIOMotorClient(
                self._url, serverSelectionTimeoutMS=5000)
            self._database = self._client[self._db_name]
            self._quizzes = self._database.quizzes

            # Log connection information (without exposing credentials)
            connection_url_parts = self._url.split('@')
            if len(connection_url_parts) > 1:
                # Hide username and password in logs
                safe_url = f"mongodb+srv://****:****@{connection_url_parts[1]}"
            else:
                safe_url = self._url
            logger.info(f"MongoDB configured with: {safe_url}")

        except Exception as e:
            logger.error(f"Failed to initialize MongoDB connection: {e}")
            raise

    async def get_all_quizzes(self):
        """Get all quizzes from the database"""
        cursor = self._quizzes.find({})
        quizzes = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            quizzes.append(document)
        return quizzes

    async def get_quiz(self, quiz_name):
        """Get a quiz by name"""
        quiz = await self._quizzes.find_one({"quiz_name": quiz_name})
        if quiz:
            quiz["id"] = str(quiz["_id"])
        return quiz

    async def save_quiz(self, quiz_data):
        """Save a quiz to the database"""
        result = await self._quizzes.insert_one(quiz_data)
        return result.inserted_id

    async def delete_quiz(self, quiz_name):
        """Delete a quiz by name"""
        result = await self._quizzes.delete_one({"quiz_name": quiz_name})
        return result.deleted_count > 0

    async def get_quiz_by_id(self, quiz_id):
        """Get a quiz by ID"""
        try:
            logger.info(f"get_quiz_by_id called with ID: {quiz_id}")
            quiz_obj_id = ObjectId(quiz_id)
            logger.info(f"ObjectId created: {quiz_obj_id}")

            quiz = await self._quizzes.find_one({"_id": quiz_obj_id})
            logger.info(f"Quiz found: {quiz is not None}")

            if quiz:
                quiz["id"] = str(quiz["_id"])
            return quiz
        except Exception as e:
            logger.error(f"Error getting quiz by ID {quiz_id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    async def get_quiz_by_id_from_db(self, db, quiz_id):
        """Get a quiz by ID using a specific database connection"""
        try:
            quiz_obj_id = ObjectId(quiz_id)
            quiz = await db.quizzes.find_one({"_id": quiz_obj_id})
            if quiz:
                quiz["id"] = str(quiz["_id"])
            return quiz
        except Exception as e:
            logger.error(f"Error getting quiz by ID {quiz_id}: {e}")
            return None


# Verify MongoDB URL exists
if not MONGODB_URL:
    logger.error("MONGODB_URL not found in .env file!")
    logger.error("Please configure MONGODB_URL in your .env file")
    sys.exit(1)

# Create database instance
db = Database(MONGODB_URL, DB_NAME)

# For backward compatibility, expose the original function names
get_all_quizzes = db.get_all_quizzes
get_quiz = db.get_quiz
save_quiz_to_db = db.save_quiz
delete_quiz_from_db = db.delete_quiz
get_quiz_by_id = db.get_quiz_by_id
get_quiz_by_id_from_app = db.get_quiz_by_id_from_db
