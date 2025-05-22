import random
from copy import deepcopy
import logging
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from bson import ObjectId

logger = logging.getLogger(__name__)


class QuizShuffler:
    """Class responsible for shuffling quiz questions and options"""

    def __init__(self, shuffle_questions: bool = True, shuffle_options: bool = True):
        """Initialize with shuffling preferences"""
        self._shuffle_questions = shuffle_questions
        self._shuffle_options = shuffle_options

    def shuffle(self, quiz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Shuffles quiz questions and options."""
        logger.info(
            f"Shuffling quiz: questions={self._shuffle_questions}, options={self._shuffle_options}")

        # Make a deep copy to avoid modifying the original
        result = deepcopy(quiz_data)

        # Convert ObjectId to string if present
        self._handle_object_id(result)

        # Check if quiz has questions
        if 'questions' not in result or not result['questions']:
            logger.warning("Quiz has no questions to shuffle")
            return result

        questions = result['questions']

        # Shuffle questions if requested
        if self._shuffle_questions:
            self._shuffle_questions_list(questions)

        # Shuffle options if requested
        if self._shuffle_options:
            self._shuffle_options_in_questions(questions)

        return result

    def _handle_object_id(self, quiz_data: Dict[str, Any]) -> None:
        """Convert MongoDB ObjectId to string ID"""
        if "_id" in quiz_data and isinstance(quiz_data["_id"], ObjectId):
            quiz_data["id"] = str(quiz_data["_id"])
            del quiz_data["_id"]

    def _shuffle_questions_list(self, questions: List[Dict]) -> None:
        """Shuffle the list of questions"""
        logger.info(
            f"Original question order: {[q.get('question_text', '')[:20] for q in questions[:3]]}...")

        # Force shuffle multiple times to ensure randomness
        for _ in range(3):
            random.shuffle(questions)

        logger.info(
            f"New question order: {[q.get('question_text', '')[:20] for q in questions[:3]]}...")

    def _shuffle_options_in_questions(self, questions: List[Dict]) -> None:
        """Shuffle options within each question and update correct answer"""
        for i, question in enumerate(questions):
            try:
                # Skip questions without required fields
                required_fields = ['option_a', 'option_b',
                                   'option_c', 'option_d', 'correct_answer']
                if not all(field in question for field in required_fields):
                    logger.warning(f"Question {i} missing required fields")
                    continue

                # Log original options
                logger.debug(
                    f"Q{i} original: A={question['option_a'][:10]}, correct={question['correct_answer']}")

                # Get correct answer letter and text
                correct_letter = question['correct_answer'].lower()
                if correct_letter not in ['a', 'b', 'c', 'd']:
                    logger.warning(f"Invalid correct_answer: {correct_letter}")
                    continue

                correct_option_key = f'option_{correct_letter}'
                correct_option_text = question.get(correct_option_key)

                # Create options for shuffling
                options = [
                    {'letter': 'a', 'text': question['option_a']},
                    {'letter': 'b', 'text': question['option_b']},
                    {'letter': 'c', 'text': question['option_c']},
                    {'letter': 'd', 'text': question['option_d']}
                ]

                # Force shuffle multiple times
                for _ in range(3):
                    random.shuffle(options)

                # Update question with shuffled options
                question['option_a'] = options[0]['text']
                question['option_b'] = options[1]['text']
                question['option_c'] = options[2]['text']
                question['option_d'] = options[3]['text']

                # Update correct answer letter
                for j, option in enumerate(options):
                    if option['text'] == correct_option_text:
                        new_letter = chr(97 + j)  # 'a' + offset
                        question['correct_answer'] = new_letter
                        logger.debug(
                            f"Q{i} shuffled: correct now {new_letter}")
                        break
            except Exception as e:
                logger.error(f"Error shuffling options for question {i}: {e}")


# For backward compatibility
def shuffle_quiz(quiz_data: Dict[str, Any], shuffle_questions: bool = True, shuffle_options: bool = True) -> Dict[str, Any]:
    """Legacy function that maintains the original interface"""
    shuffler = QuizShuffler(shuffle_questions, shuffle_options)
    return shuffler.shuffle(quiz_data)
