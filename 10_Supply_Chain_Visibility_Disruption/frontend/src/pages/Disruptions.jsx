import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Disruptions() {
  const [disruptions, setDisruptions] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState('');
  const [selectedSupplier, setSelectedSupplier] = useState('');

  useEffect(() => {
    loadDisruptions();
  }, []);

  const loadDisruptions = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/disruptions/active');
      setDisruptions(response.data.disruptions || []);
    } catch (error) {
      console.error('Error loading disruptions:', error);
    }
  };

  const predictDisruption = async () => {
    if (!selectedComponent || !selectedSupplier) {
      alert('Please select component and supplier');
      return;
    }
    try {
      await axios.post('http://localhost:8000/api/v1/disruptions/predict', null, {
        params: {
          component_id: selectedComponent,
          supplier_id: selectedSupplier
        }
      });
      loadDisruptions();
    } catch (error) {
      console.error('Error predicting disruption:', error);
    }
  };

  return (
    <div className="disruptions-page">
      <h1>Disruption Predictions</h1>
      <div className="prediction-form">
        <select value={selectedComponent} onChange={(e) => setSelectedComponent(e.target.value)}>
          <option value="">Select Component</option>
          {/* Would load from API */}
        </select>
        <select value={selectedSupplier} onChange={(e) => setSelectedSupplier(e.target.value)}>
          <option value="">Select Supplier</option>
          {/* Would load from API */}
        </select>
        <button onClick={predictDisruption}>Predict Disruption</button>
      </div>
      <div className="disruptions-grid">
        {disruptions.map(disruption => (
          <div 
            key={disruption.id} 
            className={`disruption-card ${disruption.impact_severity}`}
          >
            <h3>{disruption.disruption_type}</h3>
            <p className="probability">
              Probability: {(disruption.disruption_probability * 100).toFixed(1)}%
            </p>
            <p>Impact: {disruption.impact_severity}</p>
            <p>Predicted Date: {new Date(disruption.predicted_disruption_date).toLocaleDateString()}</p>
            {disruption.mitigation_strategies && (
              <div className="mitigation">
                <strong>Mitigation Strategies:</strong>
                <ul>
                  {disruption.mitigation_strategies.map((strategy, i) => (
                    <li key={i}>{strategy}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
