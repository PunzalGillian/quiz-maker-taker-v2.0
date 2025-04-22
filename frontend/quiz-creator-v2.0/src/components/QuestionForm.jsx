import React from "react";
import InputField from "./InputField";

const QuestionForm = ({ question, questionIndex, handleQuestionChange, onRemove }) => (
  <div className="mb-6 p-4 bg-white/50 rounded-lg border border-gray-200">
    <div className="flex justify-between items-center mb-3">
      <h2 className="font-semibold">Question {questionIndex + 1}</h2>
      {onRemove && (
        <button 
          type="button" 
          onClick={() => onRemove(questionIndex)}
          className="text-red-600 hover:text-red-800"
        >
          Remove
        </button>
      )}
    </div>

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
      onChange={(e)// filepath: c:\Users\Gil\Desktop\quiz-creator-v2.0\quiz_creator\frontend\quiz-creator-v2.0\src\components\QuestionForm.jsx
import React from "react";
import InputField from "./InputField";

const QuestionForm = ({ question, questionIndex, handleQuestionChange, onRemove }) => (
  <div className="mb-6 p-4 bg-white/50 rounded-lg border border-gray-200">
    <div className="flex justify-between items-center mb-3">
      <h2 className="font-semibold">Question {questionIndex + 1}</h2>
      {onRemove && (
        <button 
          type="button" 
          onClick={() => onRemove(questionIndex)}
          className="text-red-600 hover:text-red-800"
        >
          Remove
        </button>
      )}
    </div>

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
      onChange={(e)