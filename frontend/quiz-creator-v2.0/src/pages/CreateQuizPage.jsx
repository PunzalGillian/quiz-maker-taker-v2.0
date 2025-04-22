import React from "react";
import "../index.css";

const CreateQuizPage = () => {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center">
      <div className="QuizContainer">
        <p className="Question">Question</p>
      </div>
      <button className="bg-[#d9d9d9] rounded-lg px-6 py-2.5 w-[85vw] sm:w-[70vw] md:w-[60vw] lg:w-[50vw] max-w-[700px] my-5 text-[#213547] font-medium cursor-pointer transition-colors duration-200">
        Option A
      </button>
    </div>
  );
};

export default CreateQuizPage;
