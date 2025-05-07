import os
from typing import List, Dict, Optional
from .models import Question


class QuizFileManager:
    """Handles saving and loading quizzes to/from files."""

    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the QuizFileManager with a base directory."""
        self.base_dir = base_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'quizzes')
        os.makedirs(self.base_dir, exist_ok=True)

    def save_quiz(self, quiz_name: str, questions: List[Question]) -> str:
        """Save a quiz to a file."""
        quiz_file = os.path.join(self.base_dir, f"{quiz_name}.txt")

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

    def load_quiz(self, quiz_name: str) -> Optional[List[Dict]]:
        """Load a quiz from a file."""
        quiz_file = os.path.join(self.base_dir, f"{quiz_name}.txt")

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