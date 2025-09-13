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
      // Token launch will be implemented with smart contract integration
      console.log('Launching token:', {
        name: tokenName,
        symbol: tokenSymbol,
        description,
        socials: { twitter, telegram, website }
      });
      
      // For now, show success message
      alert(`Token "${tokenName}" (${tokenSymbol}) launch initiated! Feature coming soon.`);
      
      // Reset form
      setTokenName('');
      setTokenSymbol('');
      setDescription('');
      setTwitter('');
      setTelegram('');
      setWebsite('');
    } catch (error) {
      console.error('Launch error:', error);
      alert('Failed to launch token. Please try again.');
    } finally {
      setIsLaunching(false);
    }
  };

  return (
    <div className="launch-page" style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <div className="launch-header" style={{ marginBottom: '30px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '10px' }}>Launch Your Token</h1>
        <p style={{ color: '#666' }}>Create and launch your social token on HyperEVM</p>
      </div>

      <form onSubmit={handleLaunch} style={{ background: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
        <div style={{ marginBottom: '25px' }}>
          <h3 style={{ marginBottom: '15px', fontSize: '1.2rem' }}>Token Details</h3>
          
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
              Token Name *
            </label>
            <input
              type="text"
              value={tokenName}
              onChange={(e) => setTokenName(e.target.value)}
              placeholder="e.g., Social Token"
              required
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
              Token Symbol *
            </label>
            <input
              type="text"
              value={tokenSymbol}
              onChange={(e) => setTokenSymbol(e.target.value.toUpperCase())}
              placeholder="e.g., SOCIAL"
              maxLength="10"
              required
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe your token and its purpose..."
              rows="4"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px',
                resize: 'vertical'
              }}
            />
          </div>
        </div>

        <div style={{ marginBottom: '25px' }}>
          <h3 style={{ marginBottom: '15px', fontSize: '1.2rem' }}>Social Links</h3>
          
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
              Twitter/X
            </label>
            <input
              type="text"
              value={twitter}
              onChange={(e) => setTwitter(e.target.value)}
              placeholder="@username"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
              Telegram
            </label>
            <input
              type="text"
              value={telegram}
              onChange={(e) => setTelegram(e.target.value)}
              placeholder="t.me/groupname"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
              Website
            </label>
            <input
              type="url"
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
              placeholder="https://yourwebsite.com"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>
        </div>

        <div style={{ 
          marginBottom: '25px', 
          padding: '15px', 
          background: '#fff', 
          borderRadius: '4px',
          border: '1px solid #e0e0e0'
        }}>
          <h3 style={{ marginBottom: '15px', fontSize: '1.2rem' }}>Tokenomics</h3>
          <ul style={{ margin: 0, paddingLeft: '20px', color: '#555' }}>
            <li>Total Supply: 100,000,000 tokens</li>
            <li>Presale: 1 HYPE = 20,000 tokens</li>
            <li>Initial Liquidity: 10%</li>
            <li>Team Allocation: 15% (vested)</li>
            <li>Beta Testers: 2.5M tokens airdrop</li>
          </ul>
        </div>

        <button 
          type="submit" 
          disabled={isLaunching || !authenticated}
          style={{
            width: '100%',
            padding: '12px',
            background: authenticated ? (isLaunching ? '#999' : '#1DA1F2') : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            fontWeight: 'bold',
            cursor: authenticated && !isLaunching ? 'pointer' : 'not-allowed',
            transition: 'background 0.3s'
          }}
        >
          {!authenticated ? 'Connect Wallet First' : isLaunching ? 'Launching...' : 'Launch Token'}
        </button>
      </form>
    </div>
  );
};

export default Launch;