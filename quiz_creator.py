"""Quiz creator application for generating quiz files."""


def main():
    """Create and save quizzes with multiple choice questions."""
    # Ask the user for a quiz name
    quiz_name = input("\nEnter the name of the quiz: ")
    quiz_file = f"{quiz_name}.txt"

    questions = []

    while True:
        question = input("\nEnter the question: ")
        option_a = input("\n\tEnter answer a: ")
        option_b = input("\tEnter answer b: ")
        option_c = input("\tEnter answer c: ")
        option_d = input("\tEnter answer d: ")

        # Validate correct answer input
        while True:
            correct_answer = input(
                "Enter the correct answer (a/b/c/d): "
            ).lower()
            if correct_answer in ["a", "b", "c", "d"]:
                break
            else:
                print("Please enter a valid answer (a/b/c/d)")

        # Format question and answers in a readable format
        question_block = f"{question}\n"
        question_block += f"a) {option_a}\n"
        question_block += f"b) {option_b}\n"
        question_block += f"c) {option_c}\n"
        question_block += f"d) {option_d}\n"
        question_block += f"Correct answer: {correct_answer}\n\n"
        questions.append(question_block)

        continue_choice = input(
            "\nDo you want to add another question? (Y/N): "
        ).upper()
        if continue_choice != "Y":
            break

    print("Saving quiz...")

    # Write questions to the file
    try:
        with open(quiz_file, "w") as file:
            for question in questions:
                file.write(question)
        # No need for file.close() when using 'with' statement
        
        print(f"Quiz has been saved successfully as '{quiz_file}'.")
    except IOError as e:
        print(f"Error saving quiz: {e}")


if __name__ == "__main__":
    main()

