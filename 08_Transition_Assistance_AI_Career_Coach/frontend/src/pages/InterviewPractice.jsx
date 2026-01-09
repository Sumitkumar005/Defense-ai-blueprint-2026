import React, { useState } from 'react';
import axios from 'axios';

export default function InterviewPractice() {
  const [jobTitle, setJobTitle] = useState('');
  const [session, setSession] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);

  const startSession = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/v1/interview/practice/start', null, {
        params: { job_title: jobTitle }
      });
      setSession(response.data);
      setCurrentQuestion(response.data.questions[0]);
    } catch (error) {
      console.error('Error starting session:', error);
    }
  };

  const submitAnswer = async () => {
    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1/interview/practice/${session.session_id}/answer`,
        {
          question: currentQuestion,
          answer: answer
        }
      );
      setFeedback(response.data);
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  return (
    <div className="interview-practice">
      <h1>Interview Practice</h1>
      {!session ? (
        <div className="start-session">
          <input
            type="text"
            placeholder="Job Title"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
          />
          <button onClick={startSession}>Start Practice Session</button>
        </div>
      ) : (
        <div className="interview-session">
          <h2>Question:</h2>
          <p className="question">{currentQuestion}</p>
          <textarea
            placeholder="Your answer..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={6}
          />
          <button onClick={submitAnswer}>Submit Answer</button>
          {feedback && (
            <div className="feedback">
              <h3>Feedback</h3>
              <p>Score: {feedback.score}/100</p>
              <p>{feedback.feedback}</p>
              <div className="strengths">
                <strong>Strengths:</strong>
                <ul>
                  {feedback.strengths?.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              <div className="improvements">
                <strong>Improvements:</strong>
                <ul>
                  {feedback.improvements?.map((i, idx) => <li key={idx}>{i}</li>)}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
