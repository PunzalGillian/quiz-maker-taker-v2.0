import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import CreateQuizPage from "./pages/CreateQuizPage";
import TakeQuizPage from "./pages/TakeQuizPage";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreateQuizPage />} />
          <Route path="/take" element={<TakeQuizPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
