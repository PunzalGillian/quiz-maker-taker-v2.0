import React from "react";

const QuizPicker = ({ quizzes, onSelectQuiz }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#c3d5d4]">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Select a Quiz</h1>

        {quizzes.length > 0 ? (
          <div className="space-y-4">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id || quiz._id}
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer"
                onClick={() => onSelectQuiz(quiz.id || quiz._id)} // Use ID instead of name
              >
                <h3 className="text-lg font-medium">{quiz.quiz_name}</h3>
                <p className="text-sm text-gray-600">
                  {quiz.total_questions || 0} questions
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-gray-500">No quizzes available</p>
        )}
      </div>
    </div>
  );
};

export default QuizPicker;
