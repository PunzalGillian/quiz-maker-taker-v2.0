import React from "react";

const QuizResults = ({ quiz, score, selectedAnswers, onReset }) => {
  const totalQuestions = quiz.questions.length;
  const percentage = Math.round((score / totalQuestions) * 100);

  return (
    <div className="min-h-screen flex flex-col bg-[#c3d5d4]">
      <div className="container mx-auto max-w-2xl py-8 px-4">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h1 className="text-3xl font-bold text-center mb-6">Quiz Results</h1>
          <h2 className="text-xl font-semibold mb-4 text-center">
            {quiz.quiz_name}
          </h2>

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

          <h3 className="font-medium mb-4">Question Summary:</h3>
          <div className="space-y-4 mb-6">
            {quiz.questions.map((question, index) => {
              const userAnswer = selectedAnswers[index] || "-";
              const correctAnswer = question.correct_answer;
              const isCorrect = userAnswer === correctAnswer;

              return (
                <div
                  key={index}
                  className={`p-4 rounded-md ${
                    isCorrect ? "bg-green-100" : "bg-red-100"
                  }`}
                >
                  <p className="font-medium mb-2">
                    Q{index + 1}: {question.question}
                  </p>
                  <div className="flex flex-wrap justify-between text-sm">
                    <span>Your answer: {userAnswer.toUpperCase()}</span>
                    {!isCorrect && (
                      <span>Correct answer: {correctAnswer.toUpperCase()}</span>
                    )}
                  </div>
                </div>
              );
            })}
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
