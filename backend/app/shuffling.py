import random
from copy import deepcopy
import logging
from typing import Dict, Any
from bson import ObjectId

logger = logging.getLogger(__name__)


def shuffle_quiz(quiz_data: Dict[str, Any], shuffle_questions: bool = True, shuffle_options: bool = True) -> Dict[str, Any]:
    """Shuffles quiz questions and options."""
    logger.info(
        f"Shuffling quiz: questions={shuffle_questions}, options={shuffle_options}")

    # Make a deep copy to avoid modifying the original
    result = deepcopy(quiz_data)

    # If _id is still in the dict (not removed earlier), convert to string
    if "_id" in result and isinstance(result["_id"], ObjectId):
        result["id"] = str(result["_id"])
        del result["_id"]

    # Check if quiz has questions
    if 'questions' not in result or not result['questions']:
        logger.warning("Quiz has no questions to shuffle")
        return result

    questions = result['questions']

    # Log original question order
    if shuffle_questions:
        logger.info(
            f"Original question order: {[q.get('question_text', '')[:20] for q in questions[:3]]}...")

        # Force shuffle multiple times to ensure randomness
        for _ in range(3):
            random.shuffle(questions)

        logger.info(
            f"New question order: {[q.get('question_text', '')[:20] for q in questions[:3]]}...")

    # Shuffle options if requested
    if shuffle_options:
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

    return result
