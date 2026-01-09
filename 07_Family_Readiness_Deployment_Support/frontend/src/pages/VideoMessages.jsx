import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function VideoMessages() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState({
    title: '',
    scheduled_date: '',
    recipient_type: 'family'
  });

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/video-messages/');
      setMessages(response.data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const scheduleMessage = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/video-messages/schedule_delivery/', newMessage);
      loadMessages();
      setNewMessage({ title: '', scheduled_date: '', recipient_type: 'family' });
    } catch (error) {
      console.error('Error scheduling message:', error);
    }
  };

  return (
    <div className="video-messages">
      <h1>Video Messages</h1>
      <form onSubmit={scheduleMessage} className="message-form">
        <input
          type="text"
          placeholder="Message Title"
          value={newMessage.title}
          onChange={(e) => setNewMessage({...newMessage, title: e.target.value})}
        />
        <input
          type="date"
          value={newMessage.scheduled_date}
          onChange={(e) => setNewMessage({...newMessage, scheduled_date: e.target.value})}
        />
        <select
          value={newMessage.recipient_type}
          onChange={(e) => setNewMessage({...newMessage, recipient_type: e.target.value})}
        >
          <option value="spouse">Spouse</option>
          <option value="child">Child</option>
          <option value="family">Family</option>
        </select>
        <button type="submit">Schedule Message</button>
      </form>
      <div className="messages-list">
        {messages.map(message => (
          <div key={message.id} className="message-card">
            <h3>{message.title}</h3>
            <p>Scheduled: {message.scheduled_delivery_date}</p>
            <p>Recipient: {message.recipient_type}</p>
            {message.delivered && <span className="delivered">✓ Delivered</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
