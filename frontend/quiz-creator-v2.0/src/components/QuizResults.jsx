import React from "react";

// Helper function moved outside the component
const normalizeAnswer = (answer) => {
  if (!answer) return "";
  const normalized = answer.trim().toLowerCase();
  return normalized.length > 0 ? normalized[0] : "";
};

// Score summary component
const ScoreSummary = ({ score, totalQuestions }) => {
  const percentage =
    totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;

  return (
    <div className="bg-gray-100 p-6 rounded-lg mb-6">
      <div className="flex justify-between mb-2">
        <span>Score:</span>
        <span className="font-bold">
          {score} / {totalQuestions}
        </span>
      </div>
      <div className="flex justify-between mb-4">
        <span>Percentage:</span>
        <span className="font-bold">{percentage}%</span>
      </div>

      <div className="h-4 w-full bg-gray-200 rounded-full">
        <div
          className={`h-full rounded-full ${
            percentage >= 70
              ? "bg-green-500"
              : percentage >= 40
              ? "bg-yellow-500"
              : "bg-red-500"
          }`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

// Question result item component
const QuestionResultItem = ({ question, index, userAnswer, correctAnswer }) => {
  // Try different properties where correct answer might be stored
  const actualCorrectAnswer =
    question.correct_answer || question.correctAnswer || question.answer;

  // Flag to track if we're missing the correct answer
  const missingAnswer = !actualCorrectAnswer;

  // Use normalized comparison to determine if answer is correct
  const normalizedUserAnswer = normalizeAnswer(userAnswer);
  const normalizedCorrectAnswer = normalizeAnswer(actualCorrectAnswer);

  const isCorrect =
    normalizedUserAnswer &&
    normalizedCorrectAnswer &&
    normalizedUserAnswer === normalizedCorrectAnswer;

  // Map answer letter to the corresponding option text
  const getAnswerText = (answerLetter) => {
    if (!answerLetter) return "Not answered";
    const letter = normalizeAnswer(answerLetter);

    switch (letter) {
      case "a":
        return question.option_a || "Option A";
      case "b":
        return question.option_b || "Option B";
      case "c":
        return question.option_c || "Option C";
      case "d":
        return question.option_d || "Option D";
      default:
        return `Option ${answerLetter.toUpperCase()}`;
    }
  };

  return (
    <div
      className={`p-4 rounded-md ${
        missingAnswer
          ? "bg-gray-100"
          : isCorrect && userAnswer
          ? "bg-green-100"
          : "bg-red-100"
      }`}
    >
      <p className="font-medium mb-2">
        Q{index + 1}: {question.question || "Question text not available"}
      </p>
      <div className="flex flex-col md:flex-row md:justify-between text-sm">
        <div className="mb-2 md:mb-0">
          <span className="font-semibold">Your answer: </span>
          {userAnswer ? (
            <>
              {normalizeAnswer(userAnswer).toUpperCase()}:{" "}
              {getAnswerText(userAnswer)}
            </>
          ) : (
            "Not answered"
          )}
        </div>

        {missingAnswer ? (
          <div className="mt-2 md:mt-0 text-orange-500">
            <span className="font-semibold">Correct answer not available</span>
          </div>
        ) : !isCorrect || !userAnswer ? (
          <div className="mt-2 md:mt-0">
            <span className="font-semibold">Correct answer: </span>
            {normalizeAnswer(actualCorrectAnswer).toUpperCase()}:{" "}
            {getAnswerText(actualCorrectAnswer)}
          </div>
        ) : null}
      </div>
    </div>
  );
};

// Error fallback component
const ErrorFallback = ({ onReset }) => (
  <div className="min-h-screen flex items-center justify-center bg-[#c3d5d4]">
    <div className="bg-white p-6 rounded-lg shadow-md text-center">
      <h1 className="text-xl font-bold mb-4">Error Loading Results</h1>
      <button
        className="px-6 py-2 bg-[#1B191D] text-white rounded-lg"
        onClick={onReset}
      >
        Back to Quiz List
      </button>
    </div>
  </div>
);

// Main QuizResults component
const QuizResults = ({ quiz, score, selectedAnswers, onReset }) => {
  if (!quiz || !quiz.questions) {
    return <ErrorFallback onReset={onReset} />;
  }

  const totalQuestions = quiz.questions.length;

  return (
    <div className="min-h-screen flex flex-col bg-[#c3d5d4]">
      <div className="container mx-auto max-w-2xl py-8 px-4">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h1 className="text-3xl font-bold text-center mb-6">Quiz Results</h1>
          <h2 className="text-xl font-semibold mb-4 text-center">
            {quiz.quiz_name || "Quiz"}
          </h2>

          <ScoreSummary score={score} totalQuestions={totalQuestions} />

          <h3 className="font-medium mb-4">Question Summary:</h3>
          <div className="space-y-4 mb-6">
            {quiz.questions.map((question, index) =>
              question ? (
                <QuestionResultItem
                  key={index}
                  question={question}
                  index={index}
                  userAnswer={selectedAnswers[index] || ""}
                  correctAnswer={question.correct_answer || ""}
                />
              ) : null
            )}
          </div>

          <div className="flex justify-center space-x-4">
            <button
              className="px-6 py-2 bg-[#1B191D] text-white rounded-lg"
              onClick={onReset}
            >
              Back to Quiz List
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizResults;
