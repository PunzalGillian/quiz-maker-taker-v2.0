quiz_name = input("\nEnter the name of the quiz to take: ")
quiz_file = f"{quiz_name}.txt"

try:
    with open(quiz_file, "r") as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{quiz_file}' cannot be found")
    exit()

parsed_questions = []
score = 0

question_blocks = content.strip().split("\n\n")

for block in question_blocks:
    lines = block.strip().split("\n")

    question = lines[0]
    options = lines[1:5]

    correct_line = lines[5]
    correct_answer = correct_line.split(": ")[1].strip()

    parsed_questions.append({
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    })

total_questions = len(parsed_questions)
print(f"\nStarting quiz: {quiz_name}...\n")

for count, question in enumerate(parsed_questions, 1):
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
        print("Incorrect!. The answer is:", question["correct_answer"])
    print()

print("\nQuiz completed!\n")
print(f"You scored {score}/{total_questions} questions.\fn")
print("Thank you for taking the quiz!")


take_again = input("Do you want to take the quiz again? (Y/N): ").upper()
if take_again == "Y":
    score = 0
    print("Restarting the quiz........")
    # Restart the quiz logic here if neede
else:
    print("Exiting the quiz. Goodbye!")
