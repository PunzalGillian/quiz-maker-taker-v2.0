import random
from copy import deepcopy
from typing import Dict, Any


def shuffle_quiz(quiz_data: Dict[str, Any], shuffle_questions: bool = True, shuffle_options: bool = True) -> Dict[str, Any]:
    result = deepcopy(quiz_data)

    if 'questions' not in result or not result['questions']:
        return result

    questions = result['questions']

    if shuffle_questions:
        random.shuffle(questions)

    if shuffle_options:
        for question in questions:
            if not all(key in question for key in ['option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']):
                continue

            correct_letter = question['correct_answer'].lower()
            if correct_letter not in ['a', 'b', 'c', 'd']:
                continue

            correct_option_key = f'option_{correct_letter}'
            correct_option_text = question.get(correct_option_key)

            options = [
                {'letter': 'a', 'text': question['option_a']},
                {'letter': 'b', 'text': question['option_b']},
                {'letter': 'c', 'text': question['option_c']},
                {'letter': 'd', 'text': question['option_d']}
            ]

            random.shuffle(options)

            # Update question with shuffled options
            question['option_a'] = options[0]['text']
            question['option_b'] = options[1]['text']
            question['option_c'] = options[2]['text']
            question['option_d'] = options[3]['text']

            # Find new correct answer position
            for count, option in enumerate(options):
                if option['text'] == correct_option_text:
                    question['correct_answer'] = chr(
                        97 + count)  # Fixed the spacing around =
                    break

    return result
