import React from "react";

const QuizQuestion = ({
  currentQuestion,
  currentQuestionIndex,
  totalQuestions,
  selectedAnswers,
  handleSelectAnswer,
  handlePrevQuestion,
  handleNextQuestion,
  bgImage,
}) => {
  return (
    <div className="min-h-screen flex flex-col">
      <div
        className="w-full bg-[#C3D5D4] lg:h-[60vh] h-[50vh] flex items-center justify-center"
        style={{ backgroundImage: `url(${bgImage})` }}
      >
        <div className="container mx-auto px-4 text-center">
          <h1 className="lg:text-4xl text-2xl font-bold">
            {currentQuestion.question}
          </h1>
          <p className="mt-4 text-lg font-medium">
            Question {currentQuestionIndex + 1} of {totalQuestions}
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
            {currentQuestionIndex === totalQuestions - 1 ? "Finish" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizQuestion;
