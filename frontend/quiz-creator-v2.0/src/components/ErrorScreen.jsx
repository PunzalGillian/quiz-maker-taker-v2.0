import React from "react";

const ErrorScreen = ({ message, onRetry }) => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-[#c3d5d4]">
      <div className="w-full max-w-sm p-6 bg-white rounded-md shadow-md text-center">
        <p className="text-red-600 mb-4">{message}</p>
        <button
          className="px-4 py-2 bg-[#1B191D] text-white rounded-md"
          onClick={onRetry}
        >
          Try Again
        </button>
      </div>
    </div>
  );
};

export default ErrorScreen;
