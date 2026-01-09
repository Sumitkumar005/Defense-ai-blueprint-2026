import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import DeploymentTimeline from './pages/DeploymentTimeline';
import VideoMessages from './pages/VideoMessages';
import Resources from './pages/Resources';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/deployment/:id" element={<DeploymentTimeline />} />
        <Route path="/video-messages" element={<VideoMessages />} />
        <Route path="/resources" element={<Resources />} />
      </Routes>
    </Router>
  );
}

export default App;


