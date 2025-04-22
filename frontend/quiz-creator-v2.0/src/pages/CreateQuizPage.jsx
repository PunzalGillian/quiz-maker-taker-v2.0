import React from "react";
import "../index.css";

const CreateQuizPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <div className="w-[100%] bg-[#C3D5D4] h-[50vh] flex items-center justify-center">
        <p className="text-xl font-medium">Question</p>
      </div>

      <div className="py-3.5 px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-[900px] mx-auto">
          <button className="bg-[#EFEFEF] rounded-xl px-6 py-5 w-full text-[#213547] font-medium cursor-pointer transition-colors duration-200">
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

export default CreateQuizPage;
