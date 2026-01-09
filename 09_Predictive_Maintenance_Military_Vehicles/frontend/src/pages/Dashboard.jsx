import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [vehicles, setVehicles] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    operational: 0,
    maintenance: 0,
    out_of_service: 0
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/vehicles/');
      const vehiclesData = response.data.vehicles || [];
      setVehicles(vehiclesData);
      
      setStats({
        total: vehiclesData.length,
        operational: vehiclesData.filter(v => v.status === 'operational').length,
        maintenance: vehiclesData.filter(v => v.status === 'maintenance').length,
        out_of_service: vehiclesData.filter(v => v.status === 'out_of_service').length
      });
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Predictive Maintenance Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h2>Total Vehicles</h2>
          <p className="stat-value">{stats.total}</p>
        </div>
        <div className="stat-card operational">
          <h2>Operational</h2>
          <p className="stat-value">{stats.operational}</p>
        </div>
        <div className="stat-card maintenance">
          <h2>In Maintenance</h2>
          <p className="stat-value">{stats.maintenance}</p>
        </div>
        <div className="stat-card out-of-service">
          <h2>Out of Service</h2>
          <p className="stat-value">{stats.out_of_service}</p>
        </div>
      </div>
      <div className="vehicles-list">
        <h2>Vehicles</h2>
        <div className="vehicles-grid">
          {vehicles.map(vehicle => (
            <Link key={vehicle.id} to={`/vehicle/${vehicle.vehicle_id}`} className="vehicle-card">
              <h3>{vehicle.vehicle_id}</h3>
              <p>Type: {vehicle.type}</p>
              <p>Status: <span className={`status ${vehicle.status}`}>{vehicle.status}</span></p>
              <p>Mileage: {vehicle.mileage?.toLocaleString()}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
