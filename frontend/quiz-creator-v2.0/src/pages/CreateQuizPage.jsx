import React from "react";
import "../index.css";

const CreateQuizPage = () => {
  return (
    <div>
      <div className="min-h-screen flex items-center justify-center bg-[#C3D5D4] py-10">
        <div classname="w-full px-4 lg:max-w-[700px]">
          <h1 className="font-bold text-xl mb-4">Quiz Maker</h1>
          <p>Quiz Name:</p>
          <input
            placeholder="Enter Quiz Name:"
            className="w-full px-4 py-2 rounded-md border border-gray-300 bg-white"
          ></input>
          <p>Add a Question:</p>
          <input
            placeholder="Enter a Question:"
            className="w-full px-4 py-2 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option A:</p>
          <input
            placeholder="Enter Option A:"
            className="w-full px-4 py-2 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option B:</p>
          <input
            placeholder="Enter Option B:"
            className="w-full px-4 py-2 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option C:</p>
          <input
            placeholder="Enter Option C:"
            className="w-full px-4 py-2 rounded-md border border-gray-300  bg-white"
          ></input>
          <p>Option D:</p>
          <input
            placeholder="Enter Option D:"
            className="w-full px-4 py-2 rounded-md border border-gray-300  bg-white"
          ></input>
        </div>
      </div>
    </div>
  );
};

export default CreateQuizPage;
