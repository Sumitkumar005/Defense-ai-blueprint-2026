import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function Dashboard() {
  const [parts, setParts] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    lowStock: 0,
    expired: 0
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/inventory/parts');
      const partsData = response.data.parts || [];
      setParts(partsData);
      
      setStats({
        total: partsData.length,
        lowStock: partsData.filter(p => p.quantity < p.min_quantity).length,
        expired: partsData.filter(p => {
          if (!p.expiration_date) return false;
          return new Date(p.expiration_date) < new Date();
        }).length
      });
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Intelligent Warehouse Management</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h2>Total Parts</h2>
          <p className="stat-value">{stats.total}</p>
        </div>
        <div className="stat-card alert">
          <h2>Low Stock</h2>
          <p className="stat-value">{stats.lowStock}</p>
        </div>
        <div className="stat-card expired">
          <h2>Expired Items</h2>
          <p className="stat-value">{stats.expired}</p>
        </div>
      </div>
      <div className="actions">
        <Link to="/inventory" className="action-button">Manage Inventory</Link>
        <Link to="/picking" className="action-button">Picking Tasks</Link>
      </div>
      <div className="recent-parts">
        <h2>Recent Parts</h2>
        <div className="parts-grid">
          {parts.slice(0, 6).map(part => (
            <div key={part.id} className="part-card">
              <h3>{part.part_number}</h3>
              <p>{part.name}</p>
              <p>Location: {part.location}</p>
              <p>Quantity: {part.quantity}</p>
              {part.quantity < part.min_quantity && (
                <span className="low-stock-badge">Low Stock</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
