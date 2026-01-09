import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function SupplyChainMap() {
  const [selectedComponent, setSelectedComponent] = useState('');
  const [supplyChain, setSupplyChain] = useState(null);

  useEffect(() => {
    if (selectedComponent) {
      loadSupplyChain();
    }
  }, [selectedComponent]);

  const loadSupplyChain = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/v1/supply-chain/visibility/${selectedComponent}`
      );
      setSupplyChain(response.data);
    } catch (error) {
      console.error('Error loading supply chain:', error);
    }
  };

  return (
    <div className="supply-chain-map">
      <h1>Supply Chain Visibility Map</h1>
      <div className="component-selector">
        <select 
          value={selectedComponent} 
          onChange={(e) => setSelectedComponent(e.target.value)}
        >
          <option value="">Select Component</option>
          {/* Would load from API */}
        </select>
      </div>
      {supplyChain && (
        <div className="map-container">
          <p>Supply Chain Tiers: {supplyChain.supply_chain_tiers}</p>
          <div className="graph-placeholder">
            <p>Graph visualization would appear here</p>
            <p>Using Neo4j graph database to show multi-tier supply chain relationships</p>
          </div>
        </div>
      )}
    </div>
  );
}
