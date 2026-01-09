import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function VehicleDetail() {
  const { id } = useParams();
  const [vehicle, setVehicle] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [telematics, setTelematics] = useState([]);

  useEffect(() => {
    loadVehicleData();
    loadPredictions();
    loadTelematics();
  }, [id]);

  const loadVehicleData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/vehicles/${id}`);
      setVehicle(response.data);
    } catch (error) {
      console.error('Error loading vehicle:', error);
    }
  };

  const loadPredictions = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/predictions/${id}`);
      setPredictions(response.data.predictions || []);
    } catch (error) {
      console.error('Error loading predictions:', error);
    }
  };

  const loadTelematics = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/vehicles/${id}/telematics`, {
        params: { hours: 24 }
      });
      setTelematics(response.data.telematics || []);
    } catch (error) {
      console.error('Error loading telematics:', error);
    }
  };

  const generatePrediction = async (component) => {
    try {
      await axios.post(`http://localhost:8000/api/v1/predictions/generate/${id}`, null, {
        params: { component }
      });
      loadPredictions();
    } catch (error) {
      console.error('Error generating prediction:', error);
    }
  };

  if (!vehicle) {
    return <div>Loading...</div>;
  }

  const telematicsChartData = telematics.slice(-20).map(t => ({
    time: new Date(t.timestamp).toLocaleTimeString(),
    temp: t.engine_temp,
    pressure: t.oil_pressure
  }));

  return (
    <div className="vehicle-detail">
      <h1>Vehicle: {vehicle.vehicle_id}</h1>
      <div className="vehicle-info">
        <p><strong>Type:</strong> {vehicle.type}</p>
        <p><strong>Status:</strong> {vehicle.status}</p>
        <p><strong>Mileage:</strong> {vehicle.mileage?.toLocaleString()}</p>
        <p><strong>Engine Hours:</strong> {vehicle.engine_hours?.toLocaleString()}</p>
      </div>
      
      <div className="predictions-section">
        <h2>Failure Predictions</h2>
        <button onClick={() => generatePrediction('engine')}>Predict Engine Failure</button>
        <div className="predictions-list">
          {predictions.map(pred => (
            <div key={pred.id} className="prediction-card">
              <h3>{pred.component}</h3>
              <p>Failure Probability: {(pred.failure_probability * 100).toFixed(1)}%</p>
              <p>Timeframe: {pred.timeframe}</p>
              <p>Confidence: {(pred.confidence_score * 100).toFixed(1)}%</p>
            </div>
          ))}
        </div>
      </div>

      {telematicsChartData.length > 0 && (
        <div className="telematics-chart">
          <h2>Telematics Data (Last 24 Hours)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={telematicsChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="temp" stroke="#8884d8" name="Engine Temp" />
              <Line type="monotone" dataKey="pressure" stroke="#82ca9d" name="Oil Pressure" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
