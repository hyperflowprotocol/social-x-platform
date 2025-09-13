import React, { useState } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import './Launch.css';

const Launch = () => {
  const { ready, authenticated, user, login, logout } = usePrivy();
  const [isLaunching, setIsLaunching] = useState(false);
  
  // Get Twitter/X account info from Privy authentication
  const twitterAccount = user?.linkedAccounts?.find(account => 
    account?.type === 'twitter_oauth' || 
    (account?.type === 'oauth' && account?.provider === 'twitter')
  );
  
  const hasTwitter = !!twitterAccount;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle;
  const twitterAvatar = twitterAccount?.profilePictureUrl;
  
  const hasWallet = !!user?.wallet?.address;

  const handleConnectWallet = () => {
    login();
  };

  const handleLaunch = async () => {
    if (!hasTwitter || !hasWallet) {
      alert('Please connect both Twitter and wallet first');
      return;
    }
    
    setIsLaunching(true);
    
    try {
      // Real token launch will integrate with smart contracts
      await new Promise(resolve => setTimeout(resolve, 2000));
      alert(`Launching token for @${twitterUsername}!`);
    } catch (error) {
      console.error('Launch error:', error);
      alert('Failed to launch token. Please try again.');
    } finally {
      setIsLaunching(false);
    }
  };

  if (!ready) {
    return (
      <div className="launch-page">
        <div className="container">
          <h1 className="page-title">Launch Your Account</h1>
          <div className="loading-card">
            <div className="loading">Loading...</div>
          </div>
        </div>
      </div>
    );
  }

  // When not connected at all
  if (!authenticated) {
    return (
      <div className="launch-page">
        <div className="container">
          <h1 className="page-title">Launch Your Account</h1>
          
          <div className="connect-card">
            <h2>Connect Wallet</h2>
            <p>Connect your wallet to get started</p>
            <button 
              className="connect-button"
              onClick={handleConnectWallet}
            >
              Connect Wallet
            </button>
          </div>
        </div>
      </div>
    );
  }

  // When wallet connected, show Twitter section and Launch section
  return (
    <div className="launch-page">
      <div className="container">
        {/* Twitter Connection Card */}
        <div className="twitter-card">
          <h2>Connect Your Twitter</h2>
          {hasTwitter ? (
            <div className="twitter-connected">
              <div className="twitter-avatar">
                {twitterAvatar ? (
                  <img src={twitterAvatar} alt={twitterUsername} />
                ) : (
                  <div className="avatar-placeholder">
                    {twitterUsername?.[0]?.toUpperCase() || 'T'}
                  </div>
                )}
              </div>
              <div className="twitter-username">@{twitterUsername}</div>
              <button 
                className="disconnect-button"
                onClick={() => logout()}
              >
                Disconnect
              </button>
            </div>
          ) : (
            <div className="twitter-not-connected">
              <p>Connect your Twitter account to launch your token</p>
              <button 
                className="connect-twitter-button"
                onClick={handleConnectWallet}
              >
                Connect Twitter
              </button>
            </div>
          )}
        </div>

        {/* Launch Account Card */}
        <div className="launch-card">
          <h2>Launch Your Account</h2>
          <p>Create a tradeable token for your Twitter account on HyperEVM</p>
          
          <button 
            className="launch-button"
            onClick={handleLaunch}
            disabled={!hasTwitter || !hasWallet || isLaunching}
          >
            {isLaunching ? 'Launching...' : 'Launch Token'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Launch;