import os
import json
from typing import List, Dict, Optional, Any
from .models import Question
from fastapi.responses import JSONResponse
from bson import ObjectId

# Global constants
QUIZ_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'quizzes')
os.makedirs(QUIZ_DIR, exist_ok=True)

# MongoDB serialization helpers


class JSONEncoder(json.JSONEncoder):
    """JSON encoder that handles MongoDB ObjectId serialization"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def mongodb_response(data: Any) -> JSONResponse:
    """Convert MongoDB documents to JSON-serializable response"""
    return JSONResponse(
        content=json.loads(json.dumps(data, cls=JSONEncoder))
    )


def save_quiz(quiz_name: str, questions: List[Question]) -> str:
    """Save a quiz to a file"""
    quiz_file = os.path.join(QUIZ_DIR, f"{quiz_name}.txt")

    with open(quiz_file, "w") as file:
        for question in questions:
            question_block = f"{question.question}\n"
            question_block += f"a) {question.option_a}\n"
            question_block += f"b) {question.option_b}\n"
            question_block += f"c) {question.option_c}\n"
            question_block += f"d) {question.option_d}\n"
            question_block += f"Correct answer: {question.correct_answer}\n\n"
            file.write(question_block)

    return quiz_file


def load_quiz(quiz_name: str) -> Optional[List[Dict]]:
    """Load a quiz from a file"""
    quiz_file = os.path.join(QUIZ_DIR, f"{quiz_name}.txt")

    if not os.path.exists(quiz_file):
        return None

    with open(quiz_file, "r") as file:
        content = file.read()

    parsed_questions = []
    question_blocks = content.strip().split("\n\n")

    for block in question_blocks:
        lines = block.strip().split("\n")

        if not lines:
            continue

        question = lines[0]
        options = lines[1:5]

        correct_line = lines[5]
        correct_answer = correct_line.split(": ")[1].strip()

        parsed_questions.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })

    return parsed_questions
