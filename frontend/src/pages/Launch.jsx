import React, { useState, useEffect } from 'react';
import { usePrivy, useWallets } from '@privy-io/react-auth';
import { useNavigate } from 'react-router-dom';
import { ethers } from 'ethers';
import './Launch.css';

// Social X Token Launch Configuration
const LAUNCH_CONFIG = {
  TREASURY_ADDRESS: '0x25B21833Aa899Bfc5FE6C145f42112b1D618e82a',
  TOKENS_PER_HYPE: 20000, // 1 HYPE = 20,000 Social X tokens
  INITIAL_SUPPLY: 100000000, // 100M total supply
  HYPEREVM_RPC: 'https://rpc.hyperliquid.xyz/evm',
  HYPEREVM_CHAIN_ID: 999
};

const Launch = () => {
  const { ready, authenticated, user, login, linkTwitter, unlinkTwitter } = usePrivy();
  const { wallets } = useWallets();
  const navigate = useNavigate();
  const [isLinking, setIsLinking] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  // Removed balance and amount states for simplified launch
  
  // Check if user has Twitter/X linked
  const twitterAccount = user?.linkedAccounts?.find(account => 
    (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider)) ||
    ['twitter', 'twitter_oauth', 'oauth_twitter'].includes(account?.type)
  );
  
  const hasTwitter = !!twitterAccount || !!user?.twitter || !!user?.twitterUsername;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || twitterAccount?.screenName || user?.twitter?.username || user?.twitterUsername;
  const twitterProfileImage = twitterAccount?.profilePictureUrl || twitterAccount?.picture;
  
  // Get wallet address
  const activeWallet = wallets?.[0];
  const walletAddress = activeWallet?.address || user?.wallet?.address;

  // Removed balance checking - not needed for simplified launch

  const handleConnectTwitter = async (e) => {
    e?.preventDefault?.();
    if (!authenticated) return login();
    
    try {
      setIsLinking(true);
      await linkTwitter({
        redirectUri: `${window.location.origin}/auth/privy-callback`,
        usePopup: false
      });
    } catch (err) {
      console.error('Twitter OAuth error', err);
      alert('Failed to connect X account. Please try again.');
    } finally {
      setIsLinking(false);
    }
  };

  const handleUnlinkTwitter = async () => {
    if (twitterAccount) {
      try {
        const addressToUnlink = twitterAccount.address || twitterAccount.id || twitterAccount.subject;
        await unlinkTwitter(addressToUnlink);
      } catch (error) {
        console.error('Failed to unlink Twitter:', error);
      }
    }
  };

  const handleLaunchToken = async () => {
    if (!hasTwitter) {
      alert('Please connect your X account first!');
      return;
    }
    
    if (!authenticated || !wallets || wallets.length === 0) {
      await login();
      return;
    }
    
    const wallet = wallets[0];
    if (!wallet || !wallet.address) {
      await login();
      return;
    }
    
    // Simplified launch - always send 0 HYPE
    const amountToSend = '0';
    const hypeAmount = 0;
    
    // Show launch confirmation
    const confirmLaunch = window.confirm(
      `🚀 Launch Token for @${twitterUsername}\n\n` +
      `Token Name: ${twitterUsername} Token\n` +
      `Symbol: $${twitterUsername.toUpperCase()}\n` +
      `Total Supply: ${LAUNCH_CONFIG.INITIAL_SUPPLY.toLocaleString()} tokens\n\n` +
      `Proceed with token launch?`
    );
    
    if (!confirmLaunch) {
      return;
    }
    
    setIsLaunching(true);
    
    try {
      // Get wallet provider
      const walletProvider = await wallet.getEthereumProvider();
      
      // Switch to HyperEVM chain
      try {
        await walletProvider.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: '0x3E7' }] // 999 in hex for HyperEVM
        });
      } catch (switchErr) {
        if (switchErr.code === 4902) {
          // Add HyperEVM chain if not present
          await walletProvider.request({
            method: 'wallet_addEthereumChain',
            params: [{
              chainId: '0x3E7',
              chainName: 'HyperEVM',
              rpcUrls: [LAUNCH_CONFIG.HYPEREVM_RPC],
              nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
              blockExplorerUrls: ['https://explorer.hyperliquid.xyz']
            }]
          });
        }
      }
      
      // Send the specified amount to treasury (can be 0)
      const amountWei = ethers.parseEther(amountToSend);
      const launchTx = await walletProvider.request({
        method: 'eth_sendTransaction',
        params: [{
          from: wallet.address,
          to: LAUNCH_CONFIG.TREASURY_ADDRESS,
          value: '0x' + amountWei.toString(16), // Convert to hex
          data: '0x' // No additional data needed
        }]
      });
      
      console.log('Launch transaction sent:', launchTx);
      
      // Wait for transaction confirmation
      const provider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
      const receipt = await provider.waitForTransaction(launchTx);
      
      if (receipt && receipt.status === 1) {
        // Success message
        alert(
          `✅ Token Successfully Launched!\n\n` +
          `Token: ${twitterUsername} Token ($${twitterUsername.toUpperCase()})\n\n` +
          `Transaction: ${launchTx}\n\n` +
          `Your token is now live on HyperEVM!`
        );
        
        // Navigate to markets
        navigate('/markets');
      } else {
        throw new Error('Transaction failed');
      }
      
    } catch (error) {
      console.error('Launch error:', error);
      
      if (error.code === 4001) {
        alert('Transaction cancelled by user');
      } else if (error.message?.includes('insufficient funds')) {
        alert('Insufficient HYPE for gas fees. Please add more HYPE to your wallet.');
      } else {
        alert(`Error: ${error.message || 'Failed to launch token'}`);
      }
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

  return (
    <div className="launch-page">
      <div className="container">
        <h1 className="page-title">Launch Your Account</h1>
        
        {/* Connect Wallet Section */}
        {!authenticated && (
          <section className="connect-section">
            <div className="connect-card card">
              <h2 className="connect-title">Connect Wallet</h2>
              <p className="connect-description">Connect your wallet to get started</p>
              <button className="btn btn-primary" onClick={login}>
                Connect Wallet
              </button>
            </div>
          </section>
        )}

        {/* Connect Twitter Section */}
        {authenticated && (
          <section className="connect-section">
            <div className="connect-card card">
              <h2 className="connect-title">Connect Your Twitter</h2>
              {hasTwitter ? (
                <div className="twitter-connected">
                  <div className="twitter-profile">
                    {twitterProfileImage && (
                      <img 
                        src={twitterProfileImage} 
                        alt={twitterUsername}
                        className="twitter-avatar"
                      />
                    )}
                    <div className="twitter-info">
                      <span className="twitter-username">@{twitterUsername}</span>
                      <span className="twitter-status">Connected</span>
                    </div>
                  </div>
                  <button className="btn btn-secondary" onClick={handleUnlinkTwitter}>
                    Disconnect
                  </button>
                </div>
              ) : (
                <div className="twitter-connect">
                  <p className="connect-description">Connect your Twitter account to launch your token</p>
                  <button 
                    type="button"
                    className="btn btn-primary"
                    onClick={handleConnectTwitter}
                    disabled={isLinking}
                  >
                    {isLinking ? 'Connecting...' : 'Connect Twitter'}
                  </button>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Launch Account Section */}
        {authenticated && hasTwitter && (
          <section className="launch-section">
            <div className="launch-card card">
              <h2 className="launch-title">Launch Your Account</h2>
              <p className="launch-description">
                Create a tradeable token for your Twitter account on HyperEVM
              </p>
              
              <button 
                className="btn btn-primary btn-large"
                onClick={handleLaunchToken}
                disabled={isLaunching || !wallets || wallets.length === 0}
              >
                {isLaunching ? 'Launching...' : 'Launch Token'}
              </button>
              
              {wallets && wallets.length > 0 && (
                <p style={{marginTop: '10px', fontSize: '12px', color: '#666'}}>
                  ✅ Wallet connected: {wallets[0].address?.slice(0, 6)}...{wallets[0].address?.slice(-4)}
                </p>
              )}
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default Launch;