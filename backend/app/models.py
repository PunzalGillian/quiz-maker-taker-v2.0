from typing import List, Dict, Optional
from pydantic import BaseModel


class Question(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str


class QuizCreate(BaseModel):
    quiz_name: str
    questions: List[Question]


class Answer(BaseModel):
    answer: str  # Single answer (a, b, c, or d)


class QuizSubmission(BaseModel):
    answers: List[Answer]


class QuizResultItem(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool


class QuizResult(BaseModel):
    quiz_name: str
    score: int
    total_questions: int
    percentage: float
    results: List[QuizResultItem]


class QuizInfo(BaseModel):
    quiz_name: str
    id: Optional[str] = None
    total_questions: int = 0


class Quiz(BaseModel):
    id: Optional[str] = None
    quiz_name: str
    questions: List[dict]  # Or define a proper Question model

    class Config:
        schema_extra = {
            "example": {
                "quiz_name": "Python Basics",
                "questions": [
                    {
                        "question": "What is Python?",
                        "option_a": "A programming language",
                        "option_b": "A snake",
                        "option_c": "A database",
                        "option_d": "An operating system",
                        "correct_answer": "a"
                    }
                ]
            }
        }
