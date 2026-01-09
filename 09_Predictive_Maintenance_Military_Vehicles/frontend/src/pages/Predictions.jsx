import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Predictions() {
  const [allPredictions, setAllPredictions] = useState([]);

  useEffect(() => {
    loadAllPredictions();
  }, []);

  const loadAllPredictions = async () => {
    try {
      const vehiclesRes = await axios.get('http://localhost:8000/api/v1/vehicles/');
      const vehicles = vehiclesRes.data.vehicles || [];
      
      const predictionsPromises = vehicles.map(v => 
        axios.get(`http://localhost:8000/api/v1/predictions/${v.vehicle_id}`)
          .then(res => res.data.predictions || [])
          .catch(() => [])
      );
      
      const allPreds = await Promise.all(predictionsPromises);
      setAllPredictions(allPreds.flat());
    } catch (error) {
      console.error('Error loading predictions:', error);
    }
  };

  const highRiskPredictions = allPredictions.filter(p => p.failure_probability > 0.7);

  return (
    <div className="predictions-page">
      <h1>All Failure Predictions</h1>
      {highRiskPredictions.length > 0 && (
        <div className="alert high-risk">
          <h2>⚠️ High Risk Predictions ({highRiskPredictions.length})</h2>
        </div>
      )}
      <div className="predictions-grid">
        {allPredictions.map(pred => (
          <div 
            key={pred.id} 
            className={`prediction-card ${pred.failure_probability > 0.7 ? 'high-risk' : ''}`}
          >
            <h3>{pred.component}</h3>
            <p>Vehicle ID: {pred.vehicle_id}</p>
            <p className="probability">
              Failure Risk: {(pred.failure_probability * 100).toFixed(1)}%
            </p>
            <p>Timeframe: {pred.timeframe}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
