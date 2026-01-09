import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [deployments, setDeployments] = useState([]);

  useEffect(() => {
    loadDeployments();
  }, []);

  const loadDeployments = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/deployments/');
      setDeployments(response.data);
    } catch (error) {
      console.error('Error loading deployments:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Family Readiness Dashboard</h1>
      <div className="deployments-list">
        {deployments.map(deployment => (
          <div key={deployment.id} className="deployment-card">
            <h2>{deployment.location}</h2>
            <p>Start: {deployment.start_date}</p>
            <p>End: {deployment.end_date}</p>
            <p>Status: {deployment.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}


