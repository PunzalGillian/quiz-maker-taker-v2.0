import random
from copy import deepcopy
import logging
from typing import Dict, Any, List, Type
from abc import ABC, abstractmethod
from bson import ObjectId

logger = logging.getLogger(__name__)


class ShuffleStrategy(ABC):
    """Abstract strategy for shuffling data"""

    @abstractmethod
    def shuffle(self, data: List[Dict]) -> None:
        """Shuffle the data in place"""
        pass


class QuestionShuffleStrategy(ShuffleStrategy):
    """Strategy for shuffling questions"""

    def shuffle(self, questions: List[Dict]) -> None:
        """Shuffle the list of questions"""
        if not questions or len(questions) < 2:
            logger.info("Not enough questions to shuffle")
            return

        # Log the first few questions before shuffling
        question_key = self._detect_question_key(questions[0])
        if question_key:
            logger.info(
                f"Original question order: {[q.get(question_key, '')[:20] for q in questions[:3]]}...")

        # Store original order to verify shuffle
        original_order = questions.copy()

        # Force shuffle multiple times to ensure randomness
        max_attempts = 5
        for attempt in range(max_attempts):
            random.shuffle(questions)

            # Check if order actually changed for lists with multiple elements
            if len(questions) > 1:
                # If any question moved position, consider it shuffled
                if any(questions[i] is not original_order[i]
                       for i in range(len(questions))):
                    break

            # If on last attempt and no shuffle happened, log warning
            if attempt == max_attempts - 1:
                logger.warning("Questions may not have been properly shuffled")

        # Log the shuffled questions
        if question_key:
            logger.info(
                f"New question order: {[q.get(question_key, '')[:20] for q in questions[:3]]}...")

    def _detect_question_key(self, question: Dict) -> str:
        """Detect which key contains the question text"""
        possible_keys = ['question', 'question_text', 'text', 'content']
        for key in possible_keys:
            if key in question and isinstance(question[key], str):
                return key
        return next(iter(question.keys())) if question else ""


class OptionsShuffleStrategy(ShuffleStrategy):
    """Strategy for shuffling answer options"""

    def shuffle(self, questions: List[Dict]) -> None:
        """Shuffle options within each question"""
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


class QuizShuffler:
    """Class responsible for shuffling quiz questions and options"""

    def __init__(
            self,
            shuffle_questions: bool = True,
            shuffle_options: bool = True):
        """Initialize with shuffling preferences"""
        self._shuffle_questions = shuffle_questions
        self._shuffle_options = shuffle_options
        self._strategies = {
            'questions': QuestionShuffleStrategy(),
            'options': OptionsShuffleStrategy()
        }

    def shuffle(self, quiz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Shuffles quiz questions and options"""
        # Fix the broken f-string
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

        # Apply requested shuffling strategies
        if self._shuffle_questions:
            self._strategies['questions'].shuffle(questions)

        if self._shuffle_options:
            self._strategies['options'].shuffle(questions)

        return result

    def _handle_object_id(self, quiz_data: Dict[str, Any]) -> None:
        """Convert MongoDB ObjectId to string ID"""
        if "_id" in quiz_data and isinstance(quiz_data["_id"], ObjectId):
            quiz_data["id"] = str(quiz_data["_id"])
            del quiz_data["_id"]


# For backward compatibility with better debugging
def shuffle_quiz(
    quiz_data: Dict[str, Any],
    shuffle_questions: bool = True,
    shuffle_options: bool = True
) -> Dict[str, Any]:
    """Legacy function that maintains the original interface"""
    logger.debug(
        f"shuffle_quiz called with: shuffle_questions={shuffle_questions}, shuffle_options={shuffle_options}")

    # Check quiz structure
    if 'questions' in quiz_data:
        question_count = len(quiz_data['questions'])
        logger.debug(f"Quiz has {question_count} questions before shuffling")
    else:
        logger.warning("Quiz has no questions field")

    # Create shuffler and apply
    shuffler = QuizShuffler(shuffle_questions, shuffle_options)
    result = shuffler.shuffle(quiz_data)

    # Verify shuffling
    if 'questions' in result:
        logger.debug(
            f"Quiz has {len(result['questions'])} questions after shuffling")

    return result
