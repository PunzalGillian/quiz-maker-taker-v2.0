import React, { useState, useEffect } from "react";
import "../index.css";
import bgPlain from "/src/assets/bg-Plain.png";
import QuizPicker from "../components/QuizPicker";
import QuizResults from "../components/QuizResults";

const apiUrl = "https://quiz-maker-taker-v2-0.onrender.com";

const TakeQuizPage = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  // Fetch available quizzes
  useEffect(() => {
    const fetchQuizzes = async () => {
      setIsLoading(true);
      setError("");

      try {
        const response = await fetch(`${apiUrl}/quizzes/`);

        if (!response.ok) {
          throw new Error(`Failed to fetch quizzes: ${response.status}`);
        }

        const data = await response.json();
        setQuizzes(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Error fetching quizzes:", err);
        setError("Failed to load quizzes. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuizzes();
  }, []);

  const handleSelectQuiz = async (quizName) => {
    if (!quizName) {
      setError("Cannot load quiz: Missing quiz name");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await fetch(`${apiUrl}/quizzes/name/${quizName}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch quiz: ${response.status}`);
      }

      const data = await response.json();

      setCurrentQuiz(data);
      setCurrentQuestionIndex(0);
      setSelectedAnswers({});
      setShowResults(false);
    } catch (err) {
      console.error("Error fetching quiz details:", err);
      setError("Failed to load quiz details. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectAnswer = (questionIndex, option) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: option,
    });
  };

  const handleNextQuestion = () => {
    if (!currentQuiz?.questions) return;

    if (currentQuestionIndex < currentQuiz.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // Calculate score and show results
      calculateScore();
      setShowResults(true);
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const calculateScore = () => {
    if (!currentQuiz?.questions) return 0;

    let correctCount = 0;
    currentQuiz.questions.forEach((question, index) => {
      if (selectedAnswers[index] === question.correct_answer) {
        correctCount++;
      }
    });

    setScore(correctCount);
    return correctCount;
  };

  const resetQuiz = () => {
    setCurrentQuiz(null);
    setCurrentQuestionIndex(0);
    setSelectedAnswers({});
    setShowResults(false);
  };

  // Loading screen
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#c3d5d4]">
        <div className="w-full max-w-sm p-6 bg-white rounded-md shadow-md text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1B191D] mx-auto mb-4"></div>
          <p className="text-xl font-bold">Loading...</p>
        </div>
      </div>
    );
  }

  // Error screen
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#c3d5d4]">
        <div className="w-full max-w-sm p-6 bg-white rounded-md shadow-md text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            className="px-4 py-2 bg-[#1B191D] text-white rounded-md"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Quiz selection screen
  if (!currentQuiz) {
    return <QuizPicker quizzes={quizzes} onSelectQuiz={handleSelectQuiz} />;
  }

  // Show results screen
  if (showResults) {
    return (
      <QuizResults
        quiz={currentQuiz}
        score={score}
        selectedAnswers={selectedAnswers}
        onReset={resetQuiz}
      />
    );
  }

  // Quiz taking screen
  const currentQuestion = currentQuiz?.questions?.[currentQuestionIndex];

  if (!currentQuestion) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#c3d5d4]">
        <div className="w-full max-w-sm p-6 bg-white rounded-md shadow-md text-center">
          <p className="text-red-600 mb-4">No questions found for this quiz.</p>
          <button
            className="px-4 py-2 bg-[#1B191D] text-white rounded-md"
            onClick={resetQuiz}
          >
            Back to Quiz Selection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <div
        className="w-full bg-[#C3D5D4] lg:h-[60vh] h-[50vh] flex items-center justify-center"
        style={{ backgroundImage: `url(${bgPlain})` }}
      >
        <div className="container mx-auto px-4 text-center">
          <h1 className="lg:text-4xl text-2xl font-bold">
            {currentQuestion.question}
          </h1>
          <p className="mt-4 text-lg font-medium">
            Question {currentQuestionIndex + 1} of{" "}
            {currentQuiz.questions.length}
          </p>
        </div>
      </div>

      <div className="py-7 px-4 flex flex-col lg:py-15">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-[85vw] max-w-[85vw] mx-auto">
          <button
            className={`rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200 ${
              selectedAnswers[currentQuestionIndex] === "a"
                ? "bg-[#213547] text-white"
                : "bg-[#EFEFEF]"
            }`}
            onClick={() => handleSelectAnswer(currentQuestionIndex, "a")}
          >
            A: {currentQuestion.option_a}
          </button>

          <button
            className={`rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200 ${
              selectedAnswers[currentQuestionIndex] === "b"
                ? "bg-[#213547] text-white"
                : "bg-[#EFEFEF]"
            }`}
            onClick={() => handleSelectAnswer(currentQuestionIndex, "b")}
          >
            B: {currentQuestion.option_b}
          </button>

          <button
            className={`rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200 ${
              selectedAnswers[currentQuestionIndex] === "c"
                ? "bg-[#213547] text-white"
                : "bg-[#EFEFEF]"
            }`}
            onClick={() => handleSelectAnswer(currentQuestionIndex, "c")}
          >
            C: {currentQuestion.option_c}
          </button>

          <button
            className={`rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200 ${
              selectedAnswers[currentQuestionIndex] === "d"
                ? "bg-[#213547] text-white"
                : "bg-[#EFEFEF]"
            }`}
            onClick={() => handleSelectAnswer(currentQuestionIndex, "d")}
          >
            D: {currentQuestion.option_d}
          </button>
        </div>

        <div className="flex justify-between mt-8 w-[85vw] max-w-[85vw] mx-auto">
          <button
            className={`px-6 py-2 rounded-lg ${
              currentQuestionIndex === 0
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-gray-800 text-white"
            }`}
            onClick={handlePrevQuestion}
            disabled={currentQuestionIndex === 0}
          >
            Previous
          </button>

          <button
            className="px-6 py-2 bg-[#1B191D] text-white rounded-lg"
            onClick={handleNextQuestion}
          >
            {currentQuestionIndex === currentQuiz.questions.length - 1
              ? "Finish"
              : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TakeQuizPage;
