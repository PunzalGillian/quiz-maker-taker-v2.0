import React from "react";
import bg from "/src/assets/bg.png";
import "../index.css";

const apiURL =
  window.ENV?.VITE_API_URL ||
  import.meta.env.VITE_API_URL ||
  "https://fast-api-quiz-creator.onrender.com";

const CreateQuizPage = () => {
  const [quizName, setQuizName] = useState("");
  const [questions, setQuestions] = useState("");

  return (
    <div className="relative min-h-screen">
      {/* Background image with blur effect */}
      <img
        src={bg}
        alt=""
        className="absolute inset-0 h-full w-full object-cover blur-md brightness-75"
      />

      {/* Content overlay */}
      <div className="relative min-h-screen flex justify-center py-8 lg:py-8">
        <div
          className="w-[85vw] px-8 lg:max-w-[600px] rounded-lg shadow-lg p-6"
          style={{ backgroundColor: "rgba(255, 255, 255, 0.75)" }}
        >
          <h1 className="font-bold text-2xl mb-4">Quiz Maker</h1>
          <p>Quiz Name:</p>
          <input
            placeholder="Enter Quiz Name:"
            className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
          ></input>
          <p>Add a Question:</p>
          <input
            placeholder="Enter a Question:"
            className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
          ></input>
          <p>Option A:</p>
          <input
            placeholder="Enter Option A:"
            className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
          ></input>
          <p>Option B:</p>
          <input
            placeholder="Enter Option B:"
            className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
          ></input>
          <p>Option C:</p>
          <input
            placeholder="Enter Option C:"
            className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
          ></input>
          <p>Option D:</p>
          <input
            placeholder="Enter Option D:"
            className="w-full px-4 py-2.5 mb-6 rounded-md border border-gray-300 bg-[#EFEFEF]"
          ></input>
          <button className="w-full px-4 py-2.5 mb-6 rounded-md border border-gray-300 bg-[#EFEFEF] font-bold text-2xl">
            +
          </button>
          <button className="w-full px-4 py-2.5 ;g:mb-6 rounded-md border border-black text-white bg-[#1B191D]">
            Create Quiz
          </button>
        </div>
      </div>

      <script>function</script>
    </div>
  );
};

export default CreateQuizPage;
