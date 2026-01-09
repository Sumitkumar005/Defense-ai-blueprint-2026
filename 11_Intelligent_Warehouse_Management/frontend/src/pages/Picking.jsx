import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Picking() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({
    order_number: '',
    part_number: '',
    quantity_requested: 1,
    picker_id: ''
  });

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    // Would load from API
    setTasks([]);
  };

  const createTask = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:8000/api/v1/picking/task',
        newTask
      );
      setTasks([...tasks, response.data]);
      setNewTask({ order_number: '', part_number: '', quantity_requested: 1, picker_id: '' });
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const getARGuidance = async (taskId) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/v1/picking/task/${taskId}/guidance`
      );
      alert(`AR Guidance: ${JSON.stringify(response.data.ar_overlay, null, 2)}`);
    } catch (error) {
      console.error('Error getting guidance:', error);
    }
  };

  return (
    <div className="picking-page">
      <h1>Picking Tasks</h1>
      <form onSubmit={createTask} className="task-form">
        <input
          type="text"
          placeholder="Order Number"
          value={newTask.order_number}
          onChange={(e) => setNewTask({...newTask, order_number: e.target.value})}
          required
        />
        <input
          type="text"
          placeholder="Part Number"
          value={newTask.part_number}
          onChange={(e) => setNewTask({...newTask, part_number: e.target.value})}
          required
        />
        <input
          type="number"
          placeholder="Quantity"
          value={newTask.quantity_requested}
          onChange={(e) => setNewTask({...newTask, quantity_requested: parseInt(e.target.value)})}
          required
        />
        <button type="submit">Create Picking Task</button>
      </form>
      <div className="tasks-list">
        {tasks.map(task => (
          <div key={task.task_id} className="task-card">
            <h3>Order: {task.order_number}</h3>
            <p>Part: {task.part_number}</p>
            <p>Location: {task.location}</p>
            <p>Quantity: {task.quantity}</p>
            {task.ar_guidance?.enabled && (
              <button onClick={() => getARGuidance(task.task_id)}>
                Get AR Guidance
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
