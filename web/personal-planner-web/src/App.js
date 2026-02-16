import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import TodoPage from "./TodoPage";
import VacationsPage from "./VacationsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/todo" element={<TodoPage />} />
        <Route path ="/vacations" element={<VacationsPage />}/>
      </Routes>
    </Router>
  );
}

export default App;
