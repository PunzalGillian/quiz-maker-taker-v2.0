import random
from copy import deepcopy

def shuffle_quiz():
    result = deepcopy(quiz_data)

    if 'questions' not in result or not result['questions']:
        return result
    
    questions = result['questions']

    if shuffle_questions:
        random.shuffle(questions)
    
    if shuffle_options:
        for questions in questions:
            if not all(key in questions for key in ['option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']):
                continue
        
        correct_letter = question['correct_answer'].lower()
        if correct_letter not in ['a', 'b' 'c', 'd']:
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