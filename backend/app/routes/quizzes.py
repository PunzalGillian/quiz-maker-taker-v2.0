import os
import logging
from fastapi import APIRouter, HTTPException, Request, Depends, Query, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from ..models import QuizCreate, QuizInfo, QuizSubmission, QuizResult, Quiz
from ..database import (
    get_all_quizzes,
    get_quiz,
    save_quiz_to_db,
    delete_quiz_from_db,
    get_quiz_by_id as get_quiz_by_id_db,
    database
)
from bson import ObjectId
from ..utils import mongodb_response
from ..shuffling import shuffle_quiz

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
    responses={404: {"description": "Quiz not found"}},
)


@router.get("/", response_model=List[QuizInfo])
async def list_quizzes():
    """Get a list of all available quizzes"""
    quizzes = await get_all_quizzes()
    return [
        {
            "quiz_name": quiz["quiz_name"],
            "id": str(quiz["_id"]) if "_id" in quiz else None,
            "total_questions": len(quiz.get("questions", []))
        }
        for quiz in quizzes if quiz
    ]


@router.post("/", status_code=201)
async def create_quiz(quiz: QuizCreate):
    """Create a new quiz"""
    quiz_name = quiz.quiz_name

    # Check if quiz already exists
    existing_quiz = await get_quiz(quiz_name)
    if existing_quiz:
        raise HTTPException(
            status_code=409, detail=f"Quiz '{quiz_name}' already exists")

    # Validate correct_answer is a, b, c, or d
    for i, question in enumerate(quiz.questions):
        if question.correct_answer not in ["a", "b", "c", "d"]:
            raise HTTPException(
                status_code=400,
                detail=f"Question {i+1}: correct_answer must be one of: a, b, c, d"
            )

    # Save the quiz to MongoDB
    quiz_data = quiz.dict()
    inserted_id = await save_quiz_to_db(quiz_data)

    return {
        "message": f"Quiz '{quiz_name}' created successfully",
        "id": str(inserted_id)
    }


@router.get("/name/{quiz_name}")
async def get_quiz_by_name(
    quiz_name: str,
    request: Request,
    shuffle: bool = Query(
        True, description="Whether to shuffle questions and options")
):
    """Get a quiz by its name with option to shuffle questions and answers."""
    try:
        # Find the quiz in the database
        quiz = await request.app.mongodb.quizzes.find_one({"quiz_name": quiz_name})

        if not quiz:
            raise HTTPException(
                status_code=404, detail=f"Quiz '{quiz_name}' not found")

        # Convert ObjectId to string for JSON response
        quiz["id"] = str(quiz["_id"])

        # Shuffle quiz questions and options if requested
        if shuffle:
            quiz = shuffle_quiz(quiz)

        return quiz
    except Exception as e:
        logger.error(f"Error retrieving quiz by name: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve quiz: {str(e)}")


@router.get("/id/{quiz_id}")
async def get_quiz_by_id(
    quiz_id: str,
    request: Request,
    shuffle: bool = Query(
        True, description="Whether to shuffle questions and options")
):
    """Get a quiz by its ID with option to shuffle questions and answers."""
    try:
        # More robust ObjectId validation
        try:
            if not ObjectId.is_valid(quiz_id):
                raise HTTPException(
                    status_code=400, detail=f"Invalid ObjectId format: {quiz_id}")
            obj_id = ObjectId(quiz_id)
        except Exception as e:
            logger.error(f"Invalid ObjectId: {quiz_id}, Error: {e}")
            raise HTTPException(
                status_code=400, detail=f"Invalid quiz ID format: {quiz_id}")

        # Find quiz
        quiz = await request.app.mongodb.quizzes.find_one({"_id": obj_id})

        if not quiz:
            logger.warning(f"Quiz with ID {quiz_id} not found")
            raise HTTPException(
                status_code=404, detail=f"Quiz with ID {quiz_id} not found")

        # Add explicit logging for shuffle parameter
        logger.info(f"Quiz {quiz_id}: shuffle={shuffle}")

        # Use mongodb_response only after shuffling!
        quiz_data = dict(quiz)  # Convert from MongoDB document
        quiz_data["id"] = str(quiz_data.pop("_id"))  # Handle ObjectId

        # Apply shuffling
        if shuffle:
            try:
                quiz_data = shuffle_quiz(quiz_data)
                logger.info(f"Quiz shuffled successfully")
            except Exception as e:
                logger.error(f"Failed to shuffle quiz: {e}", exc_info=True)
                # Continue with unshuffled quiz

        # Return response
        return mongodb_response(quiz_data)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in get_quiz_by_id: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve quiz: {str(e)}")


@router.get("/debug/{quiz_id}")
async def debug_quiz_id(quiz_id: str, request: Request):
    """Debug endpoint for IDs"""
    try:
        # Check if ID is valid ObjectId
        try:
            obj_id = ObjectId(quiz_id)
            is_valid = True
        except:
            is_valid = False

        # Use request.app.mongodb instead of quizzes_collection
        db_connected = request.app.mongodb is not None

        return {
            "quiz_id": quiz_id,
            "is_valid_objectid": is_valid,
            "converted_id": str(ObjectId(quiz_id)) if is_valid else None,
            "database_connected": db_connected,
            "app_has_mongodb": hasattr(request.app, "mongodb")
        }
    except Exception as e:
        return {
            "quiz_id": quiz_id,
            "error": str(e),
            "error_type": type(e).__name__
        }


@router.post("/{quiz_name}/submit", response_model=QuizResult)
async def submit_quiz(quiz_name: str, submission: QuizSubmission):
    """Submit answers for a quiz and get results"""
    quiz = await get_quiz(quiz_name)

    if not quiz:
        raise HTTPException(
            status_code=404, detail=f"Quiz '{quiz_name}' not found")

    # Validate answers
    answers = submission.answers
    questions = quiz["questions"]

    if len(answers) != len(questions):
        raise HTTPException(
            status_code=400,
            detail=f"Expected {len(questions)} answers, got {len(answers)}"
        )

    # Grade the quiz
    score = 0
    results = []

    for i, (question, answer) in enumerate(zip(questions, answers)):
        user_answer = answer.answer.lower()
        correct_answer = question["correct_answer"]
        is_correct = user_answer == correct_answer

        if is_correct:
            score += 1

        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    percentage = (score / len(questions)) * 100 if questions else 0

    return {
        "quiz_name": quiz_name,
        "score": score,
        "total_questions": len(questions),
        "percentage": round(percentage, 1),
        "results": results
    }


@router.delete("/{quiz_name}")
async def delete_quiz(quiz_name: str):
    """Delete a quiz"""
    # Check if quiz exists
    quiz = await get_quiz(quiz_name)
    if not quiz:
        raise HTTPException(
            status_code=404, detail=f"Quiz '{quiz_name}' not found")

    # Delete the quiz
    success = await delete_quiz_from_db(quiz_name)
    if success:
        return {"message": f"Quiz '{quiz_name}' deleted successfully"}
    else:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete quiz '{quiz_name}'")


@router.get("/mock-quiz")
async def get_mock_quiz():
    """Return a mock quiz for testing"""
    return {
        "id": "mock-123",
        "quiz_name": "Mock Quiz",
        "questions": [
            {
                "question": "What is a correct syntax to output 'Hello World' in Python?",
                "option_a": "print(\"Hello World\")",
                "option_b": "p(\"Hello World\")",
                "option_c": "echo \"Hello World\"",
                "option_d": "echo(\"Hello World\");",
                "correct_answer": "a"
            },
            {
                "question": "How do you insert COMMENTS in Python code?",
                "option_a": "#This is a comment",
                "option_b": "//This is a comment",
                "option_c": "/*This is a comment*/",
                "option_d": "**This is a comment",
                "correct_answer": "a"
            }
        ]
    }
