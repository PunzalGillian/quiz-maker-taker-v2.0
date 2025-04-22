import React, { useState } from "react";
import bg from "/src/assets/bg.png";
import "../index.css";

const apiUrl = "https://quiz-maker-taker-v2-0.onrender.com";

// Reusable Input Component
const InputField = ({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
  required = true,
}) => {
  return (
    <>
      <p className="mb-1">{label}:</p>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
        required={required}
      />
    </>
  );
};

// Message Component for Success and Error Messages
const Message = ({ type, message }) => {
  const styles =
    type === "success"
      ? "bg-green-100 border-green-400 text-green-700"
      : "bg-red-100 border-red-400 text-red-700";

  return (
    <div className={`${styles} border px-4 py-3 rounded relative mb-4`}>
      {message}
    </div>
  );
};

// Question Form Component
const QuestionForm = ({ question, questionIndex, handleQuestionChange }) => (
  <div className="mb-6 p-4 bg-white/50 rounded-lg border border-gray-200">
    <h2 className="font-semibold mb-3">Question {questionIndex + 1}</h2>

    <InputField
      label="Question Text"
      value={question.question}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "question", e.target.value)
      }
      placeholder="Enter a Question"
    />

    <InputField
      label="Option A"
      value={question.option_a}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_a", e.target.value)
      }
      placeholder="Enter Option A"
    />

    <InputField
      label="Option B"
      value={question.option_b}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_b", e.target.value)
      }
      placeholder="Enter Option B"
    />

    <InputField
      label="Option C"
      value={question.option_c}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_c", e.target.value)
      }
      placeholder="Enter Option C"
    />

    <InputField
      label="Option D"
      value={question.option_d}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_d", e.target.value)
      }
      placeholder="Enter Option D"
    />

    <p className="mb-1">Correct Answer:</p>
    <select
      value={question.correct_answer}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "correct_answer", e.target.value)
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
);

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
