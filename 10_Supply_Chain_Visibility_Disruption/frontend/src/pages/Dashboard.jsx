import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function Dashboard() {
  const [components, setComponents] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [activeDisruptions, setActiveDisruptions] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [componentsRes, suppliersRes, disruptionsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/v1/supply-chain/components'),
        axios.get('http://localhost:8000/api/v1/suppliers/'),
        axios.get('http://localhost:8000/api/v1/disruptions/active')
      ]);
      setComponents(componentsRes.data.components || []);
      setSuppliers(suppliersRes.data.suppliers || []);
      setActiveDisruptions(disruptionsRes.data.disruptions || []);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const highRiskComponents = components.filter(c => c.risk_score > 0.7);

  return (
    <div className="dashboard">
      <h1>Supply Chain Visibility Dashboard</h1>
      <div className="quick-stats">
        <div className="stat-card">
          <h2>Components</h2>
          <p className="stat-value">{components.length}</p>
        </div>
        <div className="stat-card">
          <h2>Suppliers</h2>
          <p className="stat-value">{suppliers.length}</p>
        </div>
        <div className="stat-card alert">
          <h2>Active Disruptions</h2>
          <p className="stat-value">{activeDisruptions.length}</p>
        </div>
        <div className="stat-card high-risk">
          <h2>High Risk Components</h2>
          <p className="stat-value">{highRiskComponents.length}</p>
        </div>
      </div>
      <div className="actions">
        <Link to="/map" className="action-button">View Supply Chain Map</Link>
        <Link to="/disruptions" className="action-button">View Disruptions</Link>
      </div>
      {activeDisruptions.length > 0 && (
        <div className="disruptions-alert">
          <h2>⚠️ Active Disruption Predictions</h2>
          <div className="disruptions-list">
            {activeDisruptions.slice(0, 5).map(disruption => (
              <div key={disruption.id} className="disruption-card">
                <h3>{disruption.disruption_type}</h3>
                <p>Probability: {(disruption.disruption_probability * 100).toFixed(1)}%</p>
                <p>Impact: {disruption.impact_severity}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
