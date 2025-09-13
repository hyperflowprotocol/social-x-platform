import React, { useState, useEffect } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import './Launch.css';

// Force update: 2025-09-13T12:27:02.165Z

const Launch = () => {
  const { ready, authenticated, user, logout } = usePrivy();
  const [isLaunching, setIsLaunching] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  
  // Get Twitter/X account info
  const twitterAccount = user?.linkedAccounts?.find(account => 
    (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider)) ||
    ['twitter', 'twitter_oauth', 'oauth_twitter'].includes(account?.type)
  );
  
  const hasTwitter = !!twitterAccount || !!user?.twitter;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || 
                          user?.twitter?.username || user?.twitter?.handle || 
                          twitterAccount?.name;
  
  const handleLaunch = async () => {
    if (!authenticated || !hasTwitter) {
      alert('Please connect your Twitter/X account first');
      return;
    }
    
    setIsLaunching(true);
    
    try {
      // Simulate launch process
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log(`Launching token for @${twitterUsername}`);
      alert(`Token launch initiated for @${twitterUsername}!`);
    } catch (error) {
      console.error('Launch error:', error);
      alert('Failed to launch token. Please try again.');
    } finally {
      setIsLaunching(false);
    }
  };

  const handleDisconnect = () => {
    logout();
    setShowDropdown(false);
  };

  if (!ready) {
    return (
      <div className="launch-page">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="launch-page">
      <div className="container">
        {authenticated && hasTwitter ? (
          <>
            {/* Twitter Account Card */}
            <div className="twitter-account-card">
              <div className="account-avatar">
                <div className="avatar-placeholder">
                  {twitterUsername ? twitterUsername[0].toUpperCase() : 'X'}
                </div>
              </div>
              <div className="account-username">@{twitterUsername || 'username'}</div>
              <div className="dropdown-container">
                <button 
                  className="dropdown-toggle"
                  onClick={() => setShowDropdown(!showDropdown)}
                >
                  ⋮
                </button>
                {showDropdown && (
                  <div className="dropdown-menu">
                    <button onClick={handleDisconnect}>Disconnect</button>
                  </div>
                )}
              </div>
            </div>

            {/* Launch Section */}
            <div className="launch-section">
              <h1>Launch Your Account</h1>
              <p className="launch-description">
                Create a tradeable token for your Twitter account on HyperEVM
              </p>
              
              <button 
                className="launch-button"
                onClick={handleLaunch}
                disabled={isLaunching}
              >
                {isLaunching ? 'Launching...' : 'Launch Token'}
              </button>
              
              {user?.wallet?.address && (
                <div className="wallet-status">
                  ✅ Wallet connected: {user.wallet.address.slice(0, 6)}...{user.wallet.address.slice(-4)}
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="connect-prompt">
            <h1>Launch Your Token</h1>
            <p>Connect your Twitter/X account and wallet to launch your social token</p>
            <div className="connect-status">
              {!hasTwitter && <p>❌ Twitter/X account not connected</p>}
              {!user?.wallet && <p>❌ Wallet not connected</p>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Launch;