import React from "react";

const NoQuestionsScreen = ({ onReset }) => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-[#c3d5d4]">
      <div className="w-full max-w-sm p-6 bg-white rounded-md shadow-md text-center">
        <p className="text-red-600 mb-4">No questions found for this quiz.</p>
        <button
          className="px-4 py-2 bg-[#1B191D] text-white rounded-md"
          onClick={onReset}
        >
          Back to Quiz Selection
        </button>
      </div>
    </div>
  );
};

export default NoQuestionsScreen;
