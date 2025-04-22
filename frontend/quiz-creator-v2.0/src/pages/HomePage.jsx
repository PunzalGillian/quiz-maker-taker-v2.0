import React from "react";
import bg from "/src/assets/bg.png";
import quizCreatorIcon from "/src/assets/quiz-creator.png";
import quizTakerIcon from "/src/assets/quiz-taker.png";

const HomePage = () => {
  return (
    <div>
      <div
        className="min-h-screen bg-cover bg-center flex flex-col items-center justify-center text-white"
        style={{ backgroundImage: `url(${bg})` }}
      >
        <a href="/create" className="mt-60 py-5">
          <img
            src={quizCreatorIcon}
            alt="Create a Quiz"
            className="h-auto w-auto md:h-auto md:w-auto hover:opacity-90 transition"
          />
        </a>
        <a href="/take" className="-py-5">
          <img
            src={quizTakerIcon}
            alt="Take a Quiz"
            className="h-auto w-auto md:h-auto md:w-auto hover:opacity-90 transition"
          />
        </a>
      </div>
    </div>
  );
};

export default HomePage;
