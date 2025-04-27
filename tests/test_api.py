import requests
import json
import time
import sys

# API Configuration
API_URL = "https://quiz-maker-taker-v2-0.onrender.com/"
TEST_QUIZ_NAME = "Test Quiz API"

# Test data
sample_quiz = {
    "quiz_name": TEST_QUIZ_NAME,
    "questions": [
        {
            "question": "What is the capital of France?",
            "option_a": "Paris",
            "option_b": "London",
            "option_c": "Berlin",
            "option_d": "Madrid",
            "correct_answer": "a"
        },
        {
            "question": "What is 2+2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "b"
        }
    ]
}

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.WARNING}! {text}{Colors.END}")

def print_request(method, url):
    print(f"{Colors.BLUE}→ {method} {url}{Colors.END}")

def print_response(status_code, data=None):
    color = Colors.GREEN if status_code < 400 else Colors.FAIL
    print(f"{color}← Status: {status_code}{Colors.END}")
    if data:
        print(f"{Colors.CYAN}Response: {json.dumps(data, indent=2)}{Colors.END}")

def check_api_running():
    print_header("CHECKING API STATUS")
    print_request("GET", API_URL)
    
    try:
        response = requests.get(API_URL)
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            print_success("API is running!")
            return True
        else:
            print_error(f"API returned status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error connecting to API: {e}")
        return False

def delete_test_quiz():
    print_header("CLEANUP: DELETING TEST QUIZ IF IT EXISTS")
    print_request("DELETE", f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
    
    try:
        response = requests.delete(f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
        if response.status_code == 200:
            print_success(f"Test quiz '{TEST_QUIZ_NAME}' deleted")
        elif response.status_code == 404:
            print_warning(f"Test quiz '{TEST_QUIZ_NAME}' not found (this is OK)")
        else:
            print_error(f"Unexpected response: {response.status_code}")
        
        print_response(response.status_code, response.json())
    except Exception as e:
        print_error(f"Error deleting test quiz: {e}")

def test_list_quizzes():
    print_header("TEST: LISTING QUIZZES")
    print_request("GET", f"{API_URL}/quizzes")
    
    try:
        response = requests.get(f"{API_URL}/quizzes")
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            print_success("Successfully retrieved quiz list")
            return True
        else:
            print_error(f"Failed to get quiz list: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error listing quizzes: {e}")
        return False

def test_create_quiz():
    print_header("TEST: CREATING A QUIZ")
    print_request("POST", f"{API_URL}/quizzes")
    print(f"Payload: {json.dumps(sample_quiz, indent=2)}")
    
    try:
        response = requests.post(f"{API_URL}/quizzes", json=sample_quiz)
        print_response(response.status_code, response.json())
        
        if response.status_code == 201:
            print_success(f"Quiz '{TEST_QUIZ_NAME}' created successfully")
            return True
        else:
            print_error(f"Failed to create quiz: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error creating quiz: {e}")
        return False

def test_get_quiz():
    print_header(f"TEST: RETRIEVING QUIZ '{TEST_QUIZ_NAME}'")
    print_request("GET", f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
    
    try:
        response = requests.get(f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            data = response.json()
            if data["quiz_name"] == TEST_QUIZ_NAME and len(data["questions"]) == 2:
                print_success("Quiz retrieved correctly")
                
                # Check that correct_answer is not included
                if "correct_answer" not in data["questions"][0]:
                    print_success("Correct answers are properly hidden")
                else:
                    print_error("Correct answers are exposed in the response!")
                return True
            else:
                print_error("Quiz data doesn't match expected values")
                return False
        else:
            print_error(f"Failed to retrieve quiz: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving quiz: {e}")
        return False

def test_submit_quiz_answers():
    print_header("TEST: SUBMITTING QUIZ ANSWERS")
    
    # Test with all correct answers
    correct_submission = {
        "answers": [
            {"answer": "a"},  # Paris
            {"answer": "b"}   # 4
        ]
    }
    
    print_request("POST", f"{API_URL}/quizzes/{TEST_QUIZ_NAME}/submit")
    print(f"Payload (all correct): {json.dumps(correct_submission, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_URL}/quizzes/{TEST_QUIZ_NAME}/submit", 
            json=correct_submission
        )
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            result = response.json()
            if result["score"] == 2 and result["total_questions"] == 2 and result["percentage"] == 100.0:
                print_success("Perfect score calculation is correct")
            else:
                print_error("Score calculation issue with perfect submission")
        else:
            print_error(f"Failed to submit answers: {response.status_code}")
            return False
        
        # Test with some wrong answers
        mixed_submission = {
            "answers": [
                {"answer": "c"},  # Wrong - Berlin
                {"answer": "b"}   # Correct - 4
            ]
        }
        
        print("\n")
        print_request("POST", f"{API_URL}/quizzes/{TEST_QUIZ_NAME}/submit")
        print(f"Payload (mixed answers): {json.dumps(mixed_submission, indent=2)}")
        
        response = requests.post(
            f"{API_URL}/quizzes/{TEST_QUIZ_NAME}/submit", 
            json=mixed_submission
        )
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            result = response.json()
            if result["score"] == 1 and result["percentage"] == 50.0:
                print_success("Partial score calculation is correct")
                return True
            else:
                print_error("Score calculation issue with partial submission")
                return False
        else:
            print_error(f"Failed to submit answers: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error submitting answers: {e}")
        return False

def test_delete_quiz():
    print_header(f"TEST: DELETING QUIZ '{TEST_QUIZ_NAME}'")
    print_request("DELETE", f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
    
    try:
        response = requests.delete(f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            print_success(f"Quiz '{TEST_QUIZ_NAME}' deleted successfully")
            
            # Verify it's gone
            print_request("GET", f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
            verify_response = requests.get(f"{API_URL}/quizzes/{TEST_QUIZ_NAME}")
            print_response(verify_response.status_code)
            
            if verify_response.status_code == 404:
                print_success("Deletion verified - quiz no longer exists")
                return True
            else:
                print_error("Quiz still exists after deletion")
                return False
        else:
            print_error(f"Failed to delete quiz: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error deleting quiz: {e}")
        return False

def run_tests():
    print_header("QUIZ API TESTING")
    
    # Check if API is running
    if not check_api_running():
        print_error("API is not running. Please start the API first.")
        sys.exit(1)
    
    # Initial cleanup
    delete_test_quiz()
    
    # Track test results
    results = {}
    
    # Run tests in sequence
    results["List Quizzes"] = test_list_quizzes()
    results["Create Quiz"] = test_create_quiz()
    results["Get Quiz"] = test_get_quiz()
    results["Submit Answers"] = test_submit_quiz_answers()
    results["Delete Quiz"] = test_delete_quiz()
    
    # Print summary
    print_header("TEST RESULTS SUMMARY")
    
    all_passed = True
    for test_name, passed in results.items():
        if passed:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
            all_passed = False
    
    if all_passed:
        print("\n" + Colors.GREEN + Colors.BOLD + "ALL TESTS PASSED! Your Quiz API is working perfectly." + Colors.END)
    else:
        print("\n" + Colors.FAIL + Colors.BOLD + "SOME TESTS FAILED. Please check the errors above." + Colors.END)

if __name__ == "__main__":
    run_tests()