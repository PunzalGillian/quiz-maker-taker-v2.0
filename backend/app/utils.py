import os
import json
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
from .models import Question
from fastapi.responses import JSONResponse
from bson import ObjectId

# Global constants
QUIZ_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'quizzes')
os.makedirs(QUIZ_DIR, exist_ok=True)


class Serializer(ABC):
    """Abstract base class for serialization."""

    @abstractmethod
    def serialize(self, data: Any) -> Any:
        """Serialize data to a format."""
        pass


class MongoDBJSONSerializer(Serializer):
    """Serializer for MongoDB documents to JSON."""

    def serialize(self, data: Any) -> JSONResponse:
        """Convert MongoDB documents to JSON-serializable response."""
        return JSONResponse(
            content=json.loads(json.dumps(data, cls=self.JSONEncoder))
        )

    class JSONEncoder(json.JSONEncoder):
        """JSON encoder that handles MongoDB ObjectId serialization."""

        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return super().default(o)


class QuizFileManager:
    """Class for managing quiz files on disk."""

    def __init__(self, quiz_dir: str = QUIZ_DIR):
        """Initialize with quiz directory path."""
        self._quiz_dir = quiz_dir
        os.makedirs(self._quiz_dir, exist_ok=True)

    def _get_quiz_file_path(self, quiz_name: str) -> str:
        """Get the file path for a quiz."""
        return os.path.join(self._quiz_dir, f"{quiz_name}.txt")

    def save_quiz(self, quiz_name: str, questions: List[Question]) -> str:
        """Save a quiz to a file."""
        quiz_file = self._get_quiz_file_path(quiz_name)

        with open(quiz_file, "w") as file:
            for question in questions:
                question_block = f"{question.question}\n"
                question_block += f"a) {question.option_a}\n"
                question_block += f"b) {question.option_b}\n"
                question_block += f"c) {question.option_c}\n"
                question_block += f"d) {question.option_d}\n"
                question_block += f"Correct answer: {
                    question.correct_answer}\n\n"
                file.write(question_block)

        return quiz_file

    def load_quiz(self, quiz_name: str) -> Optional[List[Dict]]:
        """Load a quiz from a file."""
        quiz_file = self._get_quiz_file_path(quiz_name)

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
