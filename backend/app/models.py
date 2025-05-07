from typing import List, Optional
from pydantic import BaseModel


class Question(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

    def is_correct(self, answer: str) -> bool:
        """Check if the provided answer is correct."""
        return answer.lower() == self.correct_answer.lower()


class QuizCreate(BaseModel):
    quiz_name: str
    questions: List[Question]

    def total_questions(self) -> int:
        """Return the total number of questions in the quiz."""
        return len(self.questions)


class Answer(BaseModel):
    answer: str  # Single answer (a, b, c, or d)


class QuizSubmission(BaseModel):
    answers: List[Answer]

    def validate_submission(self, questions: List[Question]) -> List[dict]:
        """Validate the submission against the quiz questions."""
        results = []
        for question, answer in zip(questions, self.answers):
            is_correct = question.is_correct(answer.answer)
            results.append({
                "question": question.question,
                "user_answer": answer.answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
            })
        return results


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

    @classmethod
    def calculate(cls, quiz_name: str, results: List[dict]) -> "QuizResult":
        """Calculate the quiz result from the submission results."""
        total_questions = len(results)
        score = sum(1 for result in results if result["is_correct"])
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        result_items = [
            QuizResultItem(
                question=result["question"],
                user_answer=result["user_answer"],
                correct_answer=result["correct_answer"],
                is_correct=result["is_correct"],
            )
            for result in results
        ]
        return cls(
            quiz_name=quiz_name,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            results=result_items,
        )


class QuizInfo(BaseModel):
    quiz_name: str
    id: Optional[str] = None
    total_questions: int = 0


class Quiz(BaseModel):
    id: Optional[str] = None
    quiz_name: str
    questions: List[Question]

    def add_question(self, question: Question):
        """Add a question to the quiz."""
        self.questions.append(question)

    def remove_question(self, question_text: str):
        """Remove a question from the quiz by its text."""
        self.questions = [q for q in self.questions if q.question != question_text]

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
                        "correct_answer": "a",
                    }
                ],
            }
        }