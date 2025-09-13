import React, { useState } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import './Launch.css';

const Launch = () => {
  const { ready, authenticated, user } = usePrivy();
  const [tokenName, setTokenName] = useState('');
  const [tokenSymbol, setTokenSymbol] = useState('');
  const [description, setDescription] = useState('');
  const [twitter, setTwitter] = useState('');
  const [telegram, setTelegram] = useState('');
  const [website, setWebsite] = useState('');
  const [isLaunching, setIsLaunching] = useState(false);

  const handleLaunch = async (e) => {
    e.preventDefault();
    
    if (!authenticated) {
      alert('Please connect your wallet first');
      return;
    }

    if (!tokenName || !tokenSymbol) {
      alert('Please fill in all required fields');
      return;
    }

    setIsLaunching(true);
    
    try {
      // Token launch logic here
      console.log('Launching token:', {
        name: tokenName,
        symbol: tokenSymbol,
        description,
        socials: { twitter, telegram, website }
      });
      
      alert('Token launch feature coming soon!');
    } catch (error) {
      console.error('Launch error:', error);
      alert('Failed to launch token. Please try again.');
    } finally {
      setIsLaunching(false);
    }
  };

  return (
    <div className="launch-page">
      <div className="container">
        <div className="launch-header">
          <h1>Launch Your Token</h1>
          <p>Create and launch your social token on HyperEVM</p>
        </div>

        <div className="launch-form-container">
          <form onSubmit={handleLaunch} className="launch-form">
            <div className="form-section">
              <h3>Token Details</h3>
              
              <div className="form-group">
                <label>Token Name *</label>
                <input
                  type="text"
                  value={tokenName}
                  onChange={(e) => setTokenName(e.target.value)}
                  placeholder="e.g., Social Token"
                  required
                />
              </div>

              <div className="form-group">
                <label>Token Symbol *</label>
                <input
                  type="text"
                  value={tokenSymbol}
                  onChange={(e) => setTokenSymbol(e.target.value)}
                  placeholder="e.g., SOCIAL"
                  maxLength="10"
                  required
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe your token and its purpose..."
                  rows="4"
                />
              </div>
            </div>

            <div className="form-section">
              <h3>Social Links</h3>
              
              <div className="form-group">
                <label>Twitter/X</label>
                <input
                  type="text"
                  value={twitter}
                  onChange={(e) => setTwitter(e.target.value)}
                  placeholder="@username"
                />
              </div>

              <div className="form-group">
                <label>Telegram</label>
                <input
                  type="text"
                  value={telegram}
                  onChange={(e) => setTelegram(e.target.value)}
                  placeholder="t.me/groupname"
                />
              </div>

              <div className="form-group">
                <label>Website</label>
                <input
                  type="url"
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                  placeholder="https://yourwebsite.com"
                />
              </div>
            </div>

            <div className="tokenomics-info">
              <h3>Tokenomics</h3>
              <ul>
                <li>Total Supply: 100,000,000 tokens</li>
                <li>Presale: 1 HYPE = 20,000 tokens</li>
                <li>Initial Liquidity: 10%</li>
                <li>Team Allocation: 15% (vested)</li>
                <li>Beta Testers: 2.5M tokens airdrop</li>
              </ul>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary launch-btn"
              disabled={isLaunching || !authenticated}
            >
              {isLaunching ? 'Launching...' : 'Launch Token'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Launch;