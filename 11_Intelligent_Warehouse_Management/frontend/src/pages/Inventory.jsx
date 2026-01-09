import React, { useState } from 'react';
import axios from 'axios';

export default function Inventory() {
  const [shelfLocation, setShelfLocation] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [file, setFile] = useState(null);

  const handleScan = async (e) => {
    e.preventDefault();
    if (!file || !shelfLocation) {
      alert('Please select image and enter shelf location');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('shelf_location', shelfLocation);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/v1/inventory/scan',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      setScanResult(response.data);
    } catch (error) {
      console.error('Error scanning:', error);
    }
  };

  return (
    <div className="inventory-page">
      <h1>Inventory Management</h1>
      <div className="scan-section">
        <h2>Computer Vision Scan</h2>
        <form onSubmit={handleScan} className="scan-form">
          <input
            type="text"
            placeholder="Shelf Location (e.g., A-12-3)"
            value={shelfLocation}
            onChange={(e) => setShelfLocation(e.target.value)}
            required
          />
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
          <button type="submit">Scan Shelf</button>
        </form>
        {scanResult && (
          <div className="scan-result">
            <h3>Scan Results</h3>
            <p>Parts Detected: {scanResult.scans}</p>
            <div className="detections">
              {scanResult.detections?.map((det, index) => (
                <div key={index} className="detection-item">
                  <p>Part: {det.part_number}</p>
                  <p>Quantity: {det.quantity}</p>
                  <p>Confidence: {(det.confidence * 100).toFixed(1)}%</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
