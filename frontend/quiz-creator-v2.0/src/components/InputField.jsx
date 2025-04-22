import React from "react";

const InputField = ({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
  required = true,
}) => {
  return (
    <>
      <p className="mb-1">{label}:</p>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full px-4 py-2.5 mb-3 rounded-md border border-gray-300 bg-[#EFEFEF]"
        required={required}
      />
    </>
  );
};

export default InputField;
