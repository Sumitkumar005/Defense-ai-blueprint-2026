import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const Alerts: React.FC = () => {
  const { data: alerts } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const response = await axios.get('http://localhost:8000/api/v1/alerts/');
      return response.data;
    },
  });

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'red':
        return 'border-red-500 bg-red-50';
      case 'yellow':
        return 'border-yellow-500 bg-yellow-50';
      default:
        return 'border-green-500 bg-green-50';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Alerts</h1>

        <div className="space-y-4">
          {alerts?.map((alert: any) => (
            <div
              key={alert.id}
              className={`border-l-4 ${getSeverityColor(alert.severity)} rounded-lg p-6 shadow`}
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-semibold">{alert.title}</h2>
                  <p className="text-sm text-gray-600 mt-1">
                    {new Date(alert.created_at).toLocaleString()}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    alert.severity === 'red'
                      ? 'bg-red-200 text-red-800'
                      : alert.severity === 'yellow'
                      ? 'bg-yellow-200 text-yellow-800'
                      : 'bg-green-200 text-green-800'
                  }`}
                >
                  {alert.severity.toUpperCase()}
                </span>
              </div>
              <p className="text-gray-700 mb-4">{alert.message}</p>
              {alert.intervention_recommendations && (
                <div className="mt-4 p-4 bg-white rounded">
                  <h3 className="font-semibold mb-2">Intervention Recommendations:</h3>
                  <pre className="whitespace-pre-wrap text-sm text-gray-700">
                    {alert.intervention_recommendations}
                  </pre>
                </div>
              )}
              <div className="mt-4 text-sm text-gray-500">
                Status: {alert.status} | Active: {alert.is_active ? 'Yes' : 'No'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Alerts;

