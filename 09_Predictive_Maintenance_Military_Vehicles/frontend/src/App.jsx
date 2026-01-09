import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import VehicleDetail from './pages/VehicleDetail';
import Predictions from './pages/Predictions';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/vehicle/:id" element={<VehicleDetail />} />
        <Route path="/predictions" element={<Predictions />} />
      </Routes>
    </Router>
  );
}

export default App;
