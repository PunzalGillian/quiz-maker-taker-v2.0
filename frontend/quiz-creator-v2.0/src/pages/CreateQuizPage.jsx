import React from "react";
import "../index.css";

const CreateQuizPage = () => {
  return (
    <div className>
      <div className="w-[100%] bg-pink-100 h-[60vh]">
        <p className="content-center">Question</p>
      </div>
      <div className="OptionsContainer">
        <button className="mx-auto block bg-[#d9d9d9] rounded-xl px-6 py-4 w-[85vw] sm:w-[70vw] md:w-[60vw] lg:w-[50vw] max-w-[700px] my-4 text-[#213547] font-medium cursor-pointer transition-colors duration-200">
          Option A
        </button>
        <button className="mx-auto block bg-[#d9d9d9] rounded-xl px-6 py-4 w-[85vw] sm:w-[70vw] md:w-[60vw] lg:w-[50vw] max-w-[700px] my-4 text-[#213547] font-medium cursor-pointer transition-colors duration-200">
          Option B
        </button>
        <button className="mx-auto block bg-[#d9d9d9] rounded-xl px-6 py-4 w-[85vw] sm:w-[70vw] md:w-[60vw] lg:w-[50vw] max-w-[700px] my-4 text-[#213547] font-medium cursor-pointer transition-colors duration-200">
          Option C
        </button>
        <button className="mx-auto block bg-[#d9d9d9] rounded-xl px-6 py-4 w-[85vw] sm:w-[70vw] md:w-[60vw] lg:w-[50vw] max-w-[700px] my-4 text-[#213547] font-medium cursor-pointer transition-colors duration-200">
          Option D
        </button>
      </div>
    </div>
  );
};

export default CreateQuizPage;
