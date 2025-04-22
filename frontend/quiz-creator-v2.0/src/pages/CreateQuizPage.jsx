import React, { useState } from "react";
import bg from "/src/assets/bg.png";
import "../index.css";
import QuestionForm from "../components/QuestionForm";
import InputField from "../components/InputField";
import Message from "../components/MessageComponent";

const apiUrl = "https://quiz-maker-taker-v2-0.onrender.com";

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
    const updatedQuestions = questions.map((question, idx) =>
      idx === questionIndex ? { ...question, [field]: value } : question
    );
    setQuestions(updatedQuestions);
  };

  const resetForm = () => {
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
      const response = await fetch(`${apiUrl}/quizzes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quiz_name: quizName, questions }),
      });

      const contentType = response.headers.get("content-type");
      const data = contentType?.includes("application/json")
        ? await response.json()
        : { detail: "Server did not return JSON" };

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create quiz");
      }

      // Success handling
      setIsSuccess(true);
      setTimeout(() => {
        setIsSuccess(false);
        resetForm();
      }, 3000);
    } catch (err) {
      console.error("Error:", err);
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

          {/* Success and Error Messages */}
          {isSuccess && (
            <Message type="success" message="Quiz created successfully!" />
          )}
          {error && <Message type="error" message={error} />}

          <form onSubmit={createQuiz}>
            <div className="mb-4">
              <InputField
                label="Quiz Name"
                value={quizName}
                onChange={handleQuizNameChange}
                placeholder="Enter Quiz Name"
              />
            </div>

            {/* Questions */}
            {questions.map((question, questionIndex) => (
              <QuestionForm
                key={questionIndex}
                question={question}
                questionIndex={questionIndex}
                handleQuestionChange={handleQuestionChange}
              />
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
