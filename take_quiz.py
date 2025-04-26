"""Quiz taking application that reads quiz files and presents questions to users."""


def load_quiz(quiz_name):
    """Load quiz questions from a file."""
    quiz_file = f"{quiz_name}.txt"

    try:
        with open(quiz_file, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{quiz_file}' cannot be found")
        return None


def parse_questions(content):
    """Parse quiz content into structured questions."""
    parsed_questions = []
    question_blocks = content.strip().split("\n\n")

    for block in question_blocks:
        lines = block.strip().split("\n")
        
        if len(lines) < 6:  # Basic validation
            continue

        question = lines[0]
        options = lines[1:5]

        correct_line = lines[5]
        try:
            correct_answer = correct_line.split(": ")[1].strip()
        except IndexError:
            print(f"Warning: Malformed question block found")
            continue

        parsed_questions.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })
    
    return parsed_questions


def take_quiz(questions):
    """Present questions to the user and calculate score."""
    score = 0
    total_questions = len(questions)

    for count, question in enumerate(questions, 1):
        print(f"Question {count}: {question['question']}")
        print()

        for option in question["options"]:
            print(f"\t{option}")

        while True:
            user_answer = input("\nYour answer: ").lower()
            if user_answer in ["a", "b", "c", "d"]:
                break
            else:
                print("Please enter a valid answer (a/b/c/d)")

        if user_answer == question["correct_answer"]:
            score += 1
            print("Correct!!!\n")
        else:
            print(f"Incorrect! The answer is: {question['correct_answer']}\n")

    print("\nQuiz completed!")
    print(f"You scored {score}/{total_questions} questions.\n")
    print("Thank you for taking the quiz!")
    
    return score


def main():
    """Main program flow."""
    while True:
        quiz_name = input("\nEnter the name of the quiz to take: ")
        
        content = load_quiz(quiz_name)
        if not content:
            retry = input("Do you want to try another quiz? (Y/N): ").upper()
            if retry != "Y":
                break
            continue
            
        questions = parse_questions(content)
        if not questions:
            print("No valid questions found in the quiz file.")
            continue
            
        print(f"\nStarting quiz: {quiz_name}...\n")
        take_quiz(questions)
        
        take_again = input("Do you want to take another quiz? (Y/N): ").upper()
        if take_again != "Y":
            print("Exiting the quiz. Goodbye!")
            break


if __name__ == "__main__":
    main()
