import React, { useState, useEffect } from "react";
import "../index.css";
import bgPlain from "/src/assets/bg-Plain.png";
import QuizPicker from "../components/QuizPicker";
import QuizResults from "../components/QuizResults";
import QuizQuestion from "../components/QuizQuestion";
import LoadingScreen from "../components/LoadingScreen";
import ErrorScreen from "../components/ErrorScreen";
import NoQuestionsScreen from "../components/NoQuestionsScreen";

const apiUrl = "https://quiz-maker-taker-v2-0.onrender.com";

// Helper function moved outside component
const normalizeAnswer = (answer) => {
  if (!answer) return "";
  const normalized = answer.trim().toLowerCase();
  return normalized.length > 0 ? normalized[0] : "";
};

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
    fetchQuizzes();
  }, []);

  // API methods
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

  // Quiz interaction methods
  const handleSelectAnswer = (questionIndex, option) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: option,
    });
  };

  const calculateScore = () => {
    if (!currentQuiz?.questions) return 0;

    console.log("--- Score Calculation Debug ---");
    console.log("All selected answers:", selectedAnswers);

    let correctCount = 0;
    currentQuiz.questions.forEach((question, index) => {
      const userAnswer = selectedAnswers[index];
      const correctAnswer = question.correct_answer;

      console.log(`Q${index + 1}:`);
      console.log(`  Question: ${question.question}`);
      console.log(`  User answer (raw): "${userAnswer}"`);
      console.log(`  Correct answer (raw): "${correctAnswer}"`);
      console.log(
        `  User answer (normalized): "${normalizeAnswer(userAnswer)}"`
      );
      console.log(
        `  Correct answer (normalized): "${normalizeAnswer(correctAnswer)}"`
      );

      const isCorrect =
        userAnswer &&
        correctAnswer &&
        normalizeAnswer(userAnswer) === normalizeAnswer(correctAnswer);

      console.log(`  Is correct: ${isCorrect}`);

      if (isCorrect) {
        correctCount++;
      }
    });

    console.log(
      `Total correct: ${correctCount}/${currentQuiz.questions.length}`
    );

    setScore(correctCount);
    return correctCount;
  };

  const handleNextQuestion = () => {
    if (!currentQuiz?.questions) return;

    if (currentQuestionIndex < currentQuiz.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      handleFinishQuiz();
    }
  };

  const handleFinishQuiz = () => {
    calculateScore();
    setShowResults(true);
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const resetQuiz = () => {
    setCurrentQuiz(null);
    setCurrentQuestionIndex(0);
    setSelectedAnswers({});
    setShowResults(false);
  };

  // Conditional rendering based on quiz state
  if (isLoading) {
    return <LoadingScreen />;
  }

  if (error) {
    return (
      <ErrorScreen message={error} onRetry={() => window.location.reload()} />
    );
  }

  if (!currentQuiz) {
    return <QuizPicker quizzes={quizzes} onSelectQuiz={handleSelectQuiz} />;
  }

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

  const currentQuestion = currentQuiz?.questions?.[currentQuestionIndex];

  if (!currentQuestion) {
    return <NoQuestionsScreen onReset={resetQuiz} />;
  }

  const isLastQuestion =
    currentQuestionIndex === currentQuiz.questions.length - 1;

  return (
    <QuizQuestion
      currentQuestion={currentQuestion}
      currentQuestionIndex={currentQuestionIndex}
      totalQuestions={currentQuiz.questions.length}
      selectedAnswers={selectedAnswers}
      handleSelectAnswer={handleSelectAnswer}
      handlePrevQuestion={handlePrevQuestion}
      handleNextQuestion={handleNextQuestion}
      isLastQuestion={isLastQuestion}
      bgImage={bgPlain}
    />
  );
};

export default TakeQuizPage;
