import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Analytics: React.FC = () => {
  const { data: analytics } = useQuery({
    queryKey: ['unit-analytics'],
    queryFn: async () => {
      const response = await axios.get('http://localhost:8000/api/v1/analytics/unit');
      return response.data;
    },
  });

  if (!analytics) {
    return <div>Loading...</div>;
  }

  const riskData = [
    { name: 'Green', value: analytics.risk_distribution.green },
    { name: 'Yellow', value: analytics.risk_distribution.yellow },
    { name: 'Red', value: analytics.risk_distribution.red },
  ];

  const alertData = [
    { name: 'Green', value: analytics.active_alerts.green },
    { name: 'Yellow', value: analytics.active_alerts.yellow },
    { name: 'Red', value: analytics.active_alerts.red },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Unit Analytics</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">Total Soldiers</h2>
            <p className="text-3xl font-bold text-blue-600">{analytics.total_soldiers}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">Average Risk Score</h2>
            <p className="text-3xl font-bold text-orange-600">
              {(analytics.average_risk_score * 100).toFixed(1)}%
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">Unit ID</h2>
            <p className="text-3xl font-bold text-gray-600">{analytics.unit_id}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Risk Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={riskData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Active Alerts</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={alertData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;

