import React from "react";
import bg from "/src/assets/bg.png";
import titleIcon from "/src/assets/title.png";
import quizCreatorIcon from "/src/assets/quiz-creator.png";
import quizTakerIcon from "/src/assets/quiz-taker.png";

const HomePage = () => {
  return (
    <div>
      <div
        className="min-h-screen bg-cover bg-center flex flex-col items-center justify-center text-white"
        style={{ backgroundImage: `url(${bg})` }}
      >
        <div>
          <img
            src={titleIcon}
            alt="quiz title"
            className="w-[85vw] md:h-auto md:w-auto"
          />
        </div>
        <a href="/create" className="py-5">
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
