import React from "react";
import "../index.css";

const CreateQuizPage = () => {
  return (
    <div>
      <div className="min-h-screen flex justify-center bg-[#C3D5D4] py-20 lg:py-8">
        <div className="w-[85vw] px-4 lg:max-w-[450px]">
          <h1 className="font-bold text-xl mb-4">Quiz Maker</h1>
          <p>Quiz Name:</p>
          <input
            placeholder="Enter Quiz Name:"
            className="w-full px-4 py-3 mb-3 rounded-md border border-gray-300 bg-white"
          ></input>
          <p>Add a Question:</p>
          <input
            placeholder="Enter a Question:"
            className="w-full px-4 py-3 mb-3 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option A:</p>
          <input
            placeholder="Enter Option A:"
            className="w-full px-4 py-3 mb-3 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option B:</p>
          <input
            placeholder="Enter Option B:"
            className="w-full px-4 py-3 mb-3 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option C:</p>
          <input
            placeholder="Enter Option C:"
            className="w-full px-4 py-3 mb-3 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option D:</p>
          <input
            placeholder="Enter Option D:"
            className="w-full px-4 py-3 mb-6 rounded-md border border-gray-300  bg-white"
          ></input>
          <button className="w-full px-4 py-3 mb-6 rounded-md border border-gray-300  bg-white font-bold text-2xl">
            +
          </button>
          <button className="w-full px-4 py-3 mb-3 rounded-md border border-gray-300 text-white bg-[#1B191D]">
            Create Quiz
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateQuizPage;
