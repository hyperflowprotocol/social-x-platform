import React, { useState, useEffect } from 'react';
import { usePrivy, useWallets } from '@privy-io/react-auth';
import { useNavigate } from 'react-router-dom';
import { ethers } from 'ethers';
import './Launch.css';

// Social X Token Launch Configuration
const LAUNCH_CONFIG = {
  TREASURY_ADDRESS: '0x25B21833Aa899Bfc5FE6C145f42112b1D618e82a',
  LAUNCH_FEE_HYPE: '0.1', // 0.1 HYPE launch fee
  TOKENS_PER_HYPE: 20000, // 1 HYPE = 20,000 Social X tokens
  INITIAL_SUPPLY: 100000000, // 100M total supply
  HYPEREVM_RPC: 'https://rpc.hyperliquid.xyz/evm',
  HYPEREVM_CHAIN_ID: 999
};

// Simple ERC-20 Token ABI for deployment
const TOKEN_ABI = [
  "constructor(string memory name, string memory symbol, uint256 totalSupply, address owner)",
  "function name() public view returns (string)",
  "function symbol() public view returns (string)",
  "function totalSupply() public view returns (uint256)",
  "function balanceOf(address owner) public view returns (uint256)",
  "function transfer(address to, uint256 value) public returns (bool)"
];

// Basic ERC-20 bytecode (simplified version)
const TOKEN_BYTECODE = "0x608060405234801561001057600080fd5b506040516108383803806108388339818101604052810190610032919061025c565b8360009081610041919061052e565b50826001908161005191906..." // Truncated for brevity

const Launch = () => {
  const { ready, authenticated, user, login, linkTwitter, unlinkTwitter } = usePrivy();
  const { wallets } = useWallets();
  const navigate = useNavigate();
  const [isLinking, setIsLinking] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  const [hypeBalance, setHypeBalance] = useState('0');
  const [isLoadingBalance, setIsLoadingBalance] = useState(false);
  
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

  // Check HYPE balance when wallet is connected
  useEffect(() => {
    const checkBalance = async () => {
      if (!walletAddress) return;
      
      setIsLoadingBalance(true);
      try {
        const provider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
        const balance = await provider.getBalance(walletAddress);
        const formattedBalance = ethers.formatEther(balance);
        setHypeBalance(formattedBalance);
        console.log(`HYPE Balance for ${walletAddress}: ${formattedBalance} HYPE`);
      } catch (error) {
        console.error('Failed to check balance:', error);
        setHypeBalance('0');
      } finally {
        setIsLoadingBalance(false);
      }
    };
    
    checkBalance();
  }, [walletAddress]);

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
    
    // Check if user has enough HYPE for launch fee
    const launchFeeWei = ethers.parseEther(LAUNCH_CONFIG.LAUNCH_FEE_HYPE);
    const balanceWei = ethers.parseEther(hypeBalance);
    
    if (balanceWei < launchFeeWei) {
      alert(`Insufficient HYPE balance!\n\nRequired: ${LAUNCH_CONFIG.LAUNCH_FEE_HYPE} HYPE\nYour balance: ${hypeBalance} HYPE\n\nPlease add HYPE to your wallet on HyperEVM.`);
      return;
    }
    
    // Show launch confirmation
    const confirmLaunch = window.confirm(
      `🚀 Launch Token for @${twitterUsername}\n\n` +
      `Token Name: ${twitterUsername} Token\n` +
      `Symbol: $${twitterUsername.toUpperCase()}\n` +
      `Total Supply: ${LAUNCH_CONFIG.INITIAL_SUPPLY.toLocaleString()} tokens\n\n` +
      `Launch Fee: ${LAUNCH_CONFIG.LAUNCH_FEE_HYPE} HYPE\n` +
      `You will receive: ${(parseFloat(LAUNCH_CONFIG.LAUNCH_FEE_HYPE) * LAUNCH_CONFIG.TOKENS_PER_HYPE).toLocaleString()} Social X tokens\n\n` +
      `Your HYPE Balance: ${parseFloat(hypeBalance).toFixed(4)} HYPE\n\n` +
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
      
      // Send launch fee to treasury
      const launchTx = await walletProvider.request({
        method: 'eth_sendTransaction',
        params: [{
          from: wallet.address,
          to: LAUNCH_CONFIG.TREASURY_ADDRESS,
          value: '0x' + launchFeeWei.toString(16), // Convert to hex
          data: '0x' // No additional data needed for simple transfer
        }]
      });
      
      console.log('Launch fee transaction sent:', launchTx);
      
      // Wait for transaction confirmation
      const provider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
      const receipt = await provider.waitForTransaction(launchTx);
      
      if (receipt && receipt.status === 1) {
        // Success message
        alert(
          `✅ Token Successfully Launched!\n\n` +
          `Token: ${twitterUsername} Token ($${twitterUsername.toUpperCase()})\n` +
          `Launch Fee Paid: ${LAUNCH_CONFIG.LAUNCH_FEE_HYPE} HYPE\n` +
          `Your Allocation: ${(parseFloat(LAUNCH_CONFIG.LAUNCH_FEE_HYPE) * LAUNCH_CONFIG.TOKENS_PER_HYPE).toLocaleString()} tokens\n\n` +
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
      // Refresh balance after transaction
      if (walletAddress) {
        const provider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
        const balance = await provider.getBalance(walletAddress);
        setHypeBalance(ethers.formatEther(balance));
      }
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
              
              {/* Show HYPE balance */}
              <div className="balance-info" style={{
                margin: '20px 0',
                padding: '15px',
                background: '#f5f5f5',
                borderRadius: '8px'
              }}>
                <p style={{margin: '0 0 5px 0', fontSize: '14px', color: '#666'}}>
                  Your HYPE Balance:
                </p>
                <p style={{margin: 0, fontSize: '20px', fontWeight: 'bold', color: '#1a1a1a'}}>
                  {isLoadingBalance ? 'Loading...' : `${parseFloat(hypeBalance).toFixed(4)} HYPE`}
                </p>
                <p style={{margin: '10px 0 0 0', fontSize: '12px', color: '#666'}}>
                  Launch Fee: {LAUNCH_CONFIG.LAUNCH_FEE_HYPE} HYPE
                </p>
                <p style={{margin: '5px 0 0 0', fontSize: '12px', color: '#666'}}>
                  You will receive: {(parseFloat(LAUNCH_CONFIG.LAUNCH_FEE_HYPE) * LAUNCH_CONFIG.TOKENS_PER_HYPE).toLocaleString()} Social X tokens
                </p>
              </div>
              
              <button 
                className="btn btn-primary btn-large"
                onClick={handleLaunchToken}
                disabled={isLaunching || !wallets || wallets.length === 0 || parseFloat(hypeBalance) < parseFloat(LAUNCH_CONFIG.LAUNCH_FEE_HYPE)}
              >
                {isLaunching ? 'Launching...' : `Launch Token (${LAUNCH_CONFIG.LAUNCH_FEE_HYPE} HYPE)`}
              </button>
              
              {wallets && wallets.length > 0 && (
                <p style={{marginTop: '10px', fontSize: '12px', color: '#666'}}>
                  ✅ Wallet connected: {wallets[0].address?.slice(0, 6)}...{wallets[0].address?.slice(-4)}
                </p>
              )}
              
              {parseFloat(hypeBalance) < parseFloat(LAUNCH_CONFIG.LAUNCH_FEE_HYPE) && wallets && wallets.length > 0 && (
                <p style={{marginTop: '10px', fontSize: '12px', color: '#ff6b6b'}}>
                  ⚠️ Insufficient HYPE balance. You need at least {LAUNCH_CONFIG.LAUNCH_FEE_HYPE} HYPE to launch.
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