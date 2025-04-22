import React, { useState } from "react";
import bg from "/src/assets/bg.png";
import "../index.css";

const apiUrl =
  window.ENV?.VITE_API_URL ||
  import.meta.env.VITE_API_URL ||
  "https://quiz-maker-taker-v2-0.onrender.com/";

const CreateQuizPage = () => {
  const [quizName, setQuizName] = useState("");
  const [questions, setQuestions] = useState([
    {
      question: "",
      option_a: "",
      option_b: "",
      option_c: "",
      option_d: "",
      correct_answer: "",
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleQuizNameChange = (e) => {
    setQuizName(e.target.value);
  };

  const handleQuestionChange = (questionIndex, field, value) => {
    const updatedQuestions = [...questions];
    updatedQuestions[questionIndex][field] = value;
    setQuestions(updatedQuestions);
  };

  const addQuestion = () => {
    setQuestions([
      ...questions,
      {
        question: "",
        option_a: "",
        option_b: "",
        option_c: "",
        option_d: "",
        correct_answer: "",
      },
    ]);
  };

  const createQuiz = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const response = await fetch(`${apiUrl}/quizzes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quiz_name: quizName, questions }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create quiz");
      }

      // Success!
      setIsSuccess(true);
      setTimeout(() => setIsSuccess(false), 3000);

      // Reset form
      setQuizName("");
      setQuestions([
        {
          question: "",
          option_a: "",
          option_b: "",
          option_c: "",
          option_d: "",
          correct_answer: "",
        },
      ]);
    } catch (err) {
      setError(err.message || "Error creating quiz. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen">
      {/* Background image with blur effect */}
      <img
        src={bg}
        alt=""
        className="absolute inset-0 h-full w-full object-cover blur-md brightness-75"
      />

      {/* Content overlay */}
      <div className="relative min-h-screen flex justify-center py-8 overflow-auto">
        <div
          className="w-[85vw] px-6 lg:max-w-[600px] rounded-lg shadow-lg p-6 mb-8"
          style={{ backgroundColor: "rgba(255, 255, 255, 0.75)" }}
        >
          <h1 className="font-bold text-2xl mb-4 text-center">Quiz Maker</h1>

          {/* Success message */}
          {isSuccess && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
              Quiz created successfully!
            </div>
          )}

          {/* Error message */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
              {error}
            </div>
          )}

          <form onSubmit={createQuiz}>
            <div className="mb-4">
              <p className="mb-1">Quiz Name:</p>
              <input
                placeholder="Enter Quiz Name"
                value={quizName}
                onChange={handleQuizNameChange}
                className="w-full px-4 py-2.5 mb-5 rounded-md border border-gray-300 bg-[#EFEFEF]"
                required
              />
            </div>

            {/* Questions */}
            {questions.map((question, questionIndex) => (
              <div
                key={questionIndex}
                className="mb-6 p-4 bg-white/50 rounded-lg border border-gray-200"
              >
                <h2 className="font-semibold mb-3">
                  Question {questionIndex + 1}
                </h2>

                <p className="mb-1">Question Text:</p>
                <input
                  placeholder="Enter a Question"
                  value={question.question}
                  onChange={(e) =>
                    handleQuestionChange(
                      questionIndex,
                      "question",
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
                  required
                />

                <p className="mb-1">Option A:</p>
                <input
                  placeholder="Enter Option A"
                  value={question.option_a}
                  onChange={(e) =>
                    handleQuestionChange(
                      questionIndex,
                      "option_a",
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
                  required
                />

                <p className="mb-1">Option B:</p>
                <input
                  placeholder="Enter Option B"
                  value={question.option_b}
                  onChange={(e) =>
                    handleQuestionChange(
                      questionIndex,
                      "option_b",
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
                  required
                />

                <p className="mb-1">Option C:</p>
                <input
                  placeholder="Enter Option C"
                  value={question.option_c}
                  onChange={(e) =>
                    handleQuestionChange(
                      questionIndex,
                      "option_c",
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
                  required
                />

                <p className="mb-1">Option D:</p>
                <input
                  placeholder="Enter Option D"
                  value={question.option_d}
                  onChange={(e) =>
                    handleQuestionChange(
                      questionIndex,
                      "option_d",
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
                  required
                />

                <p className="mb-1">Correct Answer:</p>
                <select
                  value={question.correct_answer}
                  onChange={(e) =>
                    handleQuestionChange(
                      questionIndex,
                      "correct_answer",
                      e.target.value
                    )
                  }
                  className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
                  required
                >
                  <option value="">Select Correct Answer</option>
                  <option value="a">Option A</option>
                  <option value="b">Option B</option>
                  <option value="c">Option C</option>
                  <option value="d">Option D</option>
                </select>
              </div>
            ))}

            {/* Add Question Button */}
            <button
              type="button"
              onClick={addQuestion}
              className="w-full px-4 py-2.5 mb-6 rounded-md border border-gray-300 bg-[#EFEFEF] font-bold text-2xl"
            >
              +
            </button>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-4 py-2.5 rounded-md border border-black text-white bg-[#1B191D] disabled:opacity-70"
            >
              {isLoading ? "Creating Quiz..." : "Create Quiz"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CreateQuizPage;
