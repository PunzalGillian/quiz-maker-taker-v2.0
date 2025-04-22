import React from "react";
import "../index.css";
import bgPlain from "/src/assets/bg-Plain.png";

const TakeQuizPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <div
        className="w-[100%] bg-[#C3D5D4] lg:h-[60vh] h-[50vh] flex items-center justify-center"
        style={{ backgroundImage: `url(${bgPlain})` }}
      >
        <h1 className="lg:text-5xl text-3xl font-bold">
          QUestiion question questions
        </h1>
      </div>

      <div className="py-7 px-4 flex flex-col lg:py-15">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-[85vw] max-w-[85vw] mx-auto">
          <button className="bg-[#EFEFEF] border-blackrounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200">
            Option A
          </button>
          <button className="bg-[#EFEFEF] rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200">
            Option B
          </button>
          <button className="bg-[#EFEFEF] rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200">
            Option C
          </button>
          <button className="bg-[#EFEFEF] rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200">
            Option D
          </button>
        </div>
      </div>
    </div>
  );
};

export default TakeQuizPage;
