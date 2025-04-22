import React from "react";

const CreateQuizPage = () => {
  return (
    <div>
      <div className="QuizContainer">
        <p className="Question">Question</p>
      </div>
      <div className="OptionsContainer">
        <button className="py-2">Option A</button>
        <button className="py-2 px-4">Option B</button>
        <button className="py-2 px-4">Option C</button>
        <button className="py-2 px-4">Option D</button>
      </div>
    </div>
  );
};

export default CreateQuizPage;
