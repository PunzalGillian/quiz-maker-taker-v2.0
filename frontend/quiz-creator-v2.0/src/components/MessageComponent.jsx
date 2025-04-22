import React from "react";

const MessageComponent = ({ type, message }) => {
  const styles =
    type === "success"
      ? "bg-green-100 border-green-400 text-green-700"
      : "bg-red-100 border-red-400 text-red-700";

  return (
    <div className={`${styles} border px-4 py-3 rounded relative mb-4`}>
      {message}
    </div>
  );
};

export default MessageComponent;
