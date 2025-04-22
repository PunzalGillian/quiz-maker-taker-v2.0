import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import CreateQuizPage from "./pages/CreateQuizPage";

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<CreateQuizPage />} />
          <Route path="/create" element={<CreateQuizPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
