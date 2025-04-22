import React from "react";
import bg from "/src/assets/bg.png";

const QuizPicker = ({ quizzes, onSelectQuiz }) => {
  return (
    <div className="relative min-h-screen">
      {/* Background image with blur effect */}
      <img
        src={bg}
        alt=""
        className="absolute inset-0 h-full w-full object-cover blur-md brightness-75"
      />

      {/* Content overlay */}
      <div className="relative z-10 min-h-screen flex flex-col">
        <div className="container mx-auto py-8 px-4">
          <h1 className="text-3xl font-bold text-center mb-8 text-white">
            Select a Quiz
          </h1>

          {quizzes.length === 0 ? (
            <div className="text-center p-6 bg-white rounded-lg shadow-md">
              <p className="text-xl">No quizzes available.</p>
              <p className="mt-2 mb-4">Create a quiz first!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {quizzes.map((quiz, index) => {
                // Check if questions count exists in different ways
                const questionCount =
                  quiz.questions?.length ||
                  quiz.question_count ||
                  quiz.questionCount ||
                  "?";

                return (
                  <div
                    key={index}
                    className="bg-white/75 p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
                    onClick={() => onSelectQuiz(quiz.quiz_name)}
                  >
                    <h2 className="text-xl font-bold mb-2">{quiz.quiz_name}</h2>
                    <p className="text-gray-600 mb-4">
                      {questionCount} questions
                    </p>
                    <button className="w-full py-2 bg-[#1B191D] text-white rounded-md hover:bg-opacity-90 transition-colors">
                      Take Quiz
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuizPicker;
