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
    return <LoadingScreen />;
  }

  // Error screen
  if (error) {
    return (
      <ErrorScreen message={error} onRetry={() => window.location.reload()} />
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
    return <NoQuestionsScreen onReset={resetQuiz} />;
  }

  return (
    <QuizQuestion
      currentQuestion={currentQuestion}
      currentQuestionIndex={currentQuestionIndex}
      totalQuestions={currentQuiz.questions.length}
      selectedAnswers={selectedAnswers}
      handleSelectAnswer={handleSelectAnswer}
      handlePrevQuestion={handlePrevQuestion}
      handleNextQuestion={handleNextQuestion}
      bgImage={bgPlain}
    />
  );
};

export default TakeQuizPage;
