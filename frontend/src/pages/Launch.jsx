import React from 'react';
import { usePrivy } from '@privy-io/react-auth';
import './Launch.css';

const Launch = () => {
  const { ready, authenticated, user } = usePrivy();

  return (
    <div className="launch-page">
      <div className="container">
        <div className="launch-content">
          <h1>Launch</h1>
          <p>Token launch coming soon</p>
        </div>
      </div>
    </div>
  );
};

export default Launch;