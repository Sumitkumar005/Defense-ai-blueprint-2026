import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { format, differenceInDays } from 'date-fns';

export default function DeploymentTimeline() {
  const { id } = useParams();
  const [deployment, setDeployment] = useState(null);
  const [timeline, setTimeline] = useState(null);

  useEffect(() => {
    loadDeployment();
    loadTimeline();
  }, [id]);

  const loadDeployment = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/deployments/${id}/`);
      setDeployment(response.data);
    } catch (error) {
      console.error('Error loading deployment:', error);
    }
  };

  const loadTimeline = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/deployments/${id}/timeline/`);
      setTimeline(response.data);
    } catch (error) {
      console.error('Error loading timeline:', error);
    }
  };

  if (!deployment || !timeline) {
    return <div>Loading...</div>;
  }

  const daysRemaining = differenceInDays(new Date(deployment.end_date), new Date());

  return (
    <div className="deployment-timeline">
      <h1>Deployment Timeline</h1>
      <div className="timeline-header">
        <h2>{deployment.location}</h2>
        <p className="status">{timeline.status}</p>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${timeline.progress_percentage}%` }}
          ></div>
        </div>
        <p>{daysRemaining} days remaining</p>
      </div>
      <div className="timeline-dates">
        <div className="date-item">
          <strong>Start Date:</strong> {format(new Date(deployment.start_date), 'MMM dd, yyyy')}
        </div>
        <div className="date-item">
          <strong>End Date:</strong> {format(new Date(deployment.end_date), 'MMM dd, yyyy')}
        </div>
      </div>
    </div>
  );
}
