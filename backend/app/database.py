import os
import sys
import logging
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

# Verify MongoDB URL exists
if not MONGODB_URL:
    logger.error("MONGODB_URL not found in .env file!")
    logger.error("Please configure MONGODB_URL in your .env file")
    sys.exit(1)

try:
    # Create MongoDB client with a timeout
    client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    database = client[DB_NAME]

    # Collection references
    quizzes_collection = database.quizzes

    # Log connection information (without exposing credentials)
    connection_url_parts = MONGODB_URL.split('@')
    if len(connection_url_parts) > 1:
        # Hide username and password in logs
        safe_url = f"mongodb+srv://****:****@{connection_url_parts[1]}"
    else:
        safe_url = MONGODB_URL
    logger.info(f"MongoDB configured with: {safe_url}")

except Exception as e:
    logger.error(f"Failed to initialize MongoDB connection: {e}")
    # Re-raise to make initialization failures obvious
    raise

# Database helper functions


async def get_all_quizzes():
    """Get all quizzes from the database"""
    cursor = quizzes_collection.find({})
    quizzes = []
    async for document in cursor:
        document["id"] = str(document["_id"])
        quizzes.append(document)
    return quizzes


async def get_quiz(quiz_name):
    """Get a quiz by name"""
    quiz = await quizzes_collection.find_one({"quiz_name": quiz_name})
    if quiz:
        quiz["id"] = str(quiz["_id"])
    return quiz


async def save_quiz_to_db(quiz_data):
    """Save a quiz to the database"""
    result = await quizzes_collection.insert_one(quiz_data)
    return result.inserted_id


async def delete_quiz_from_db(quiz_name):
    """Delete a quiz by name"""
    result = await quizzes_collection.delete_one({"quiz_name": quiz_name})
    return result.deleted_count > 0


async def get_quiz_by_id(quiz_id):
    """Get a quiz by ID"""
    try:
        logger.info(f"get_quiz_by_id called with ID: {quiz_id}")
        quiz_obj_id = ObjectId(quiz_id)
        logger.info(f"ObjectId created: {quiz_obj_id}")

        quiz = await quizzes_collection.find_one({"_id": quiz_obj_id})
        logger.info(f"Quiz found: {quiz is not None}")

        if quiz:
            quiz["id"] = str(quiz["_id"])
        return quiz
    except Exception as e:
        logger.error(f"Error getting quiz by ID {quiz_id}: {e}")
        # Print full stack trace for debugging
        import traceback
        logger.error(traceback.format_exc())
        return None


async def get_quiz_by_id_from_app(db, quiz_id):
    """Get a quiz by ID using the app's MongoDB connection"""
    try:
        quiz_obj_id = ObjectId(quiz_id)
        quiz = await db.quizzes.find_one({"_id": quiz_obj_id})
        if quiz:
            quiz["id"] = str(quiz["_id"])
        return quiz
    except Exception as e:
        logger.error(f"Error getting quiz by ID {quiz_id}: {e}")
        return None
