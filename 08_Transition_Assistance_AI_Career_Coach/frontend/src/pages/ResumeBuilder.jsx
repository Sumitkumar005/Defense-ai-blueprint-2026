import React, { useState } from 'react';
import axios from 'axios';

export default function ResumeBuilder() {
  const [targetJob, setTargetJob] = useState('');
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateResume = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/resume/generate', {
        target_job_title: targetJob
      });
      setResume(response.data);
    } catch (error) {
      console.error('Error generating resume:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-builder">
      <h1>AI Resume Builder</h1>
      <form onSubmit={generateResume} className="resume-form">
        <input
          type="text"
          placeholder="Target Job Title (e.g., Project Manager)"
          value={targetJob}
          onChange={(e) => setTargetJob(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Resume'}
        </button>
      </form>
      {resume && (
        <div className="resume-preview">
          <h2>Generated Resume</h2>
          <pre className="resume-content">{resume.content}</pre>
          <button onClick={() => navigator.clipboard.writeText(resume.content)}>
            Copy Resume
          </button>
        </div>
      )}
    </div>
  );
}
