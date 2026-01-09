import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ResumeBuilder from './pages/ResumeBuilder';
import JobSearch from './pages/JobSearch';
import InterviewPractice from './pages/InterviewPractice';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/resume" element={<ResumeBuilder />} />
        <Route path="/jobs" element={<JobSearch />} />
        <Route path="/interview" element={<InterviewPractice />} />
      </Routes>
    </Router>
  );
}

export default App;
