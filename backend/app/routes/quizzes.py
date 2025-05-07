import logging
from fastapi import APIRouter, HTTPException, Request
from typing import List
from ..models import QuizCreate, QuizInfo, QuizSubmission, QuizResult, Quiz
from ..database import Database
from bson import ObjectId

# Configure logging
logger = logging.getLogger(__name__)

class QuizService:
    """Service class to handle quiz-related operations."""

    def __init__(self, database: Database):
        self.database = database

    async def list_quizzes(self) -> List[QuizInfo]:
        """Get a list of all available quizzes."""
        quizzes = await self.database.get_all_quizzes()
        return [
            QuizInfo(
                quiz_name=quiz["quiz_name"],
                id=str(quiz["_id"]) if "_id" in quiz else None,
                total_questions=len(quiz.get("questions", []))
            )
            for quiz in quizzes if quiz
        ]

    async def create_quiz(self, quiz: QuizCreate):
        """Create a new quiz."""
        quiz_name = quiz.quiz_name

        # Check if quiz already exists
        existing_quiz = await self.database.get_quiz_by_name(quiz_name)
        if existing_quiz:
            raise HTTPException(status_code=409, detail=f"Quiz '{quiz_name}' already exists")

        # Validate correct_answer is a, b, c, or d
        for i, question in enumerate(quiz.questions):
            if question.correct_answer not in ["a", "b", "c", "d"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {i+1}: correct_answer must be one of: a, b, c, d"
                )

        # Save the quiz to MongoDB
        quiz_data = quiz.dict()
        inserted_id = await self.database.save_quiz(quiz_data)

        return {
            "message": f"Quiz '{quiz_name}' created successfully",
            "id": str(inserted_id)
        }

    async def get_quiz_by_name(self, quiz_name: str):
        """Get a specific quiz (without correct answers)."""
        quiz = await self.database.get_quiz_by_name(quiz_name)

        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found")

        # Create a copy of the questions without correct answers
        questions_for_client = [
            {k: v for k, v in q.items() if k != "correct_answer"}
            for q in quiz["questions"]
        ]

        return {
            "quiz_name": quiz["quiz_name"],
            "questions": questions_for_client,
            "total_questions": len(questions_for_client)
        }

    async def delete_quiz(self, quiz_name: str):
        """Delete a quiz."""
        quiz = await self.database.get_quiz_by_name(quiz_name)
        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found")

        success = await self.database.delete_quiz(quiz_name)
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to delete quiz '{quiz_name}'")

        return {"message": f"Quiz '{quiz_name}' deleted successfully"}

    async def submit_quiz(self, quiz_name: str, submission: QuizSubmission):
        """Submit answers for a quiz and get results."""
        quiz = await self.database.get_quiz_by_name(quiz_name)

        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found")

        # Validate answers
        answers = submission.answers
        questions = quiz["questions"]

        if len(answers) != len(questions):
            raise HTTPException(
                status_code=400,
                detail=f"Expected {len(questions)} answers, got {len(answers)}"
            )

        # Grade the quiz
        results = submission.validate_submission(questions)
        return QuizResult.calculate(quiz_name, results)


# Initialize router and service
router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
    responses={404: {"description": "Quiz not found"}},
)

database = Database()
quiz_service = QuizService(database)


# Define routes
@router.get("/", response_model=List[QuizInfo])
async def list_quizzes():
    """Get a list of all available quizzes."""
    return await quiz_service.list_quizzes()


@router.post("/", status_code=201)
async def create_quiz(quiz: QuizCreate):
    """Create a new quiz."""
    return await quiz_service.create_quiz(quiz)


@router.get("/name/{quiz_name}")
async def get_quiz_by_name(quiz_name: str):
    """Get a specific quiz (without correct answers)."""
    return await quiz_service.get_quiz_by_name(quiz_name)


@router.delete("/{quiz_name}")
async def delete_quiz(quiz_name: str):
    """Delete a quiz."""
    return await quiz_service.delete_quiz(quiz_name)


@router.post("/{quiz_name}/submit", response_model=QuizResult)
async def submit_quiz(quiz_name: str, submission: QuizSubmission):
    """Submit answers for a quiz and get results."""
    return await quiz_service.submit_quiz(quiz_name, submission)