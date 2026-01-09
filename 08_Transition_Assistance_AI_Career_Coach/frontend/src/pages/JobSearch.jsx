import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function JobSearch() {
  const [jobs, setJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);

  const searchJobs = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/v1/jobs/search', {
        params: {
          job_title: searchTerm || undefined,
          location: location || undefined
        }
      });
      setJobs(response.data.jobs || []);
    } catch (error) {
      console.error('Error searching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    searchJobs();
  }, []);

  return (
    <div className="job-search">
      <h1>Job Search</h1>
      <div className="search-form">
        <input
          type="text"
          placeholder="Job Title"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <button onClick={searchJobs} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
      <div className="jobs-list">
        {jobs.map((job, index) => (
          <div key={index} className="job-card">
            <h3>{job.title}</h3>
            <p className="company">{job.company}</p>
            <p className="location">{job.location}</p>
            {job.match_score && (
              <div className="match-score">
                Match: {job.match_score}%
              </div>
            )}
            <a href={job.url} target="_blank" rel="noopener noreferrer">
              View Job
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
