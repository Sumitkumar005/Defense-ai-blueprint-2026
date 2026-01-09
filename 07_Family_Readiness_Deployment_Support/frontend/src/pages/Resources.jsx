import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Resources() {
  const [resources, setResources] = useState([]);
  const [category, setCategory] = useState('');

  useEffect(() => {
    loadResources();
  }, [category]);

  const loadResources = async () => {
    try {
      const url = category 
        ? `http://localhost:8000/api/resources/by_category/?category=${category}`
        : 'http://localhost:8000/api/resources/';
      const response = await axios.get(url);
      setResources(response.data);
    } catch (error) {
      console.error('Error loading resources:', error);
    }
  };

  const categories = [
    'financial', 'legal', 'childcare', 'mental_health', 'education', 'housing'
  ];

  return (
    <div className="resources">
      <h1>Family Resources</h1>
      <div className="category-filter">
        <button onClick={() => setCategory('')}>All</button>
        {categories.map(cat => (
          <button key={cat} onClick={() => setCategory(cat)}>
            {cat.replace('_', ' ').toUpperCase()}
          </button>
        ))}
      </div>
      <div className="resources-list">
        {resources.map(resource => (
          <div key={resource.id} className="resource-card">
            <h3>{resource.title}</h3>
            <p className="category">{resource.category}</p>
            <p>{resource.description}</p>
            <a href={resource.url} target="_blank" rel="noopener noreferrer">
              Learn More
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
