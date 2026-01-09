import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { AlertTriangle, TrendingUp, Activity } from 'lucide-react';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const { data: latestPrediction } = useQuery({
    queryKey: ['latest-prediction'],
    queryFn: async () => {
      const response = await axios.get('http://localhost:8000/api/v1/predictions/latest');
      return response.data;
    },
  });

  const { data: alerts } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const response = await axios.get('http://localhost:8000/api/v1/alerts/', {
        params: { active_only: true },
      });
      return response.data;
    },
  });

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'red':
        return 'bg-red-500';
      case 'yellow':
        return 'bg-yellow-500';
      default:
        return 'bg-green-500';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600">Current Risk Level</p>
                <p className="text-2xl font-bold mt-2">
                  {latestPrediction?.risk_level?.toUpperCase() || 'N/A'}
                </p>
              </div>
              <div className={`w-12 h-12 rounded-full ${getRiskColor(latestPrediction?.risk_level || 'green')} flex items-center justify-center`}>
                <Activity className="text-white" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600">Risk Score</p>
                <p className="text-2xl font-bold mt-2">
                  {(latestPrediction?.risk_score * 100).toFixed(1)}%
                </p>
              </div>
              <TrendingUp className="text-blue-500" size={32} />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600">Active Alerts</p>
                <p className="text-2xl font-bold mt-2">
                  {alerts?.length || 0}
                </p>
              </div>
              <AlertTriangle className="text-orange-500" size={32} />
            </div>
          </div>
        </div>

        {alerts && alerts.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">Recent Alerts</h2>
            <div className="space-y-4">
              {alerts.slice(0, 5).map((alert: any) => (
                <div
                  key={alert.id}
                  className={`border-l-4 ${
                    alert.severity === 'red'
                      ? 'border-red-500'
                      : alert.severity === 'yellow'
                      ? 'border-yellow-500'
                      : 'border-green-500'
                  } p-4 bg-gray-50 rounded`}
                >
                  <h3 className="font-semibold">{alert.title}</h3>
                  <p className="text-gray-600 text-sm mt-1">{alert.message}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Welcome, {user?.username}</h2>
          <p className="text-gray-600">
            This dashboard provides an overview of your mental health risk assessment
            and any active alerts. Use the navigation to explore detailed predictions,
            alerts, and analytics.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

