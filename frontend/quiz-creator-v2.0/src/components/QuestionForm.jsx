import React from "react";
import InputField from "./InputField";

const QuestionForm = ({ question, questionIndex, handleQuestionChange }) => (
  <div className="mb-6 p-4 bg-white/50 rounded-lg border border-gray-200">
    <h2 className="font-semibold mb-3">Question {questionIndex + 1}</h2>

    <InputField
      label="Question Text"
      value={question.question}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "question", e.target.value)
      }
      placeholder="Enter a Question"
    />

    <InputField
      label="Option A"
      value={question.option_a}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_a", e.target.value)
      }
      placeholder="Enter Option A"
    />

    <InputField
      label="Option B"
      value={question.option_b}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_b", e.target.value)
      }
      placeholder="Enter Option B"
    />

    <InputField
      label="Option C"
      value={question.option_c}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_c", e.target.value)
      }
      placeholder="Enter Option C"
    />

    <InputField
      label="Option D"
      value={question.option_d}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "option_d", e.target.value)
      }
      placeholder="Enter Option D"
    />

    <p className="mb-1">Correct Answer:</p>
    <select
      value={question.correct_answer}
      onChange={(e) =>
        handleQuestionChange(questionIndex, "correct_answer", e.target.value)
      }
      className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
      required
    >
      <option value="">Select Correct Answer</option>
      <option value="a">Option A</option>
      <option value="b">Option B</option>
      <option value="c">Option C</option>
      <option value="d">Option D</option>
    </select>
  </div>
);

export default QuestionForm;
