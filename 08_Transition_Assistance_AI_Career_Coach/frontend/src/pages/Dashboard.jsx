import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [skills, setSkills] = useState([]);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const [skillsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/v1/career/skills/1')
      ]);
      setSkills(skillsRes.data.skills || []);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Transition Assistance AI Career Coach</h1>
      <div className="quick-actions">
        <Link to="/resume" className="action-card">
          <h2>Build Resume</h2>
          <p>AI-powered resume builder</p>
        </Link>
        <Link to="/jobs" className="action-card">
          <h2>Find Jobs</h2>
          <p>Match with civilian jobs</p>
        </Link>
        <Link to="/interview" className="action-card">
          <h2>Practice Interview</h2>
          <p>AI interview coach</p>
        </Link>
      </div>
      <div className="skills-section">
        <h2>Your Skills</h2>
        <div className="skills-list">
          {skills.map((skill, index) => (
            <span key={index} className="skill-tag">{skill}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
