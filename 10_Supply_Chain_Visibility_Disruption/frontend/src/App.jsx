import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SupplyChainMap from './pages/SupplyChainMap';
import Disruptions from './pages/Disruptions';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/map" element={<SupplyChainMap />} />
        <Route path="/disruptions" element={<Disruptions />} />
      </Routes>
    </Router>
  );
}

export default App;
