import React from "react";

const LoadingScreen = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-[#c3d5d4]">
      <div className="w-full max-w-sm p-6 bg-white rounded-md shadow-md text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1B191D] mx-auto mb-4"></div>
        <p className="text-xl font-bold">Loading...</p>
      </div>
    </div>
  );
};

export default LoadingScreen;
