import React, { useState, useEffect } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { useNavigate } from 'react-router-dom';
import WalletFundTransfer from '../components/WalletFundTransfer';
import './Portfolio.css';

const Portfolio = () => {
  const { ready, authenticated, user, login, logout } = usePrivy();
  const navigate = useNavigate();
  
  // State for balance tracking
  const [hypeBalance, setHypeBalance] = useState('0.00');
  const [isLoadingBalance, setIsLoadingBalance] = useState(false);
  const [balanceError, setBalanceError] = useState(null);
  const [hypePrice, setHypePrice] = useState(null);
  const [isPriceLoading, setIsPriceLoading] = useState(false);

  // Function to fetch current HYPE price from CoinGecko
  const fetchHypePrice = async () => {
    setIsPriceLoading(true);
    try {
      console.log('💰 Fetching HYPE price from CoinGecko...');
      
      const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=hyperliquid&vs_currencies=usd&include_24hr_change=true');
      
      if (!response.ok) {
        throw new Error(`Price API failed: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.hyperliquid && data.hyperliquid.usd) {
        const price = data.hyperliquid.usd;
        setHypePrice(price);
        console.log('💰 HYPE price fetched:', price);
        return price;
      } else {
        throw new Error('Invalid price data received');
      }
    } catch (error) {
      console.error('❌ Failed to fetch HYPE price:', error);
      setHypePrice(null);
      return null;
    } finally {
      setIsPriceLoading(false);
    }
  };

  // Function to fetch HYPE balance from HyperEVM blockchain
  const fetchHypeBalance = async (walletAddress) => {
    if (!walletAddress) {
      setHypeBalance('0.00');
      return;
    }

    setIsLoadingBalance(true);
    setBalanceError(null);

    try {
      console.log('🔍 Fetching HYPE balance for:', walletAddress);
      
      // HyperEVM RPC endpoints (official working endpoints)
      const rpcUrls = [
        'https://rpc.hyperliquid.xyz/evm',
        'https://1rpc.io/hyperevm',
        'https://hyperevm.g.alchemy.com/v2/demo'
      ];

      let balance = null;
      
      // Try each RPC endpoint until one works
      for (const rpcUrl of rpcUrls) {
        try {
          console.log('🌐 Trying RPC:', rpcUrl);
          
          // Make RPC request to get balance
          const response = await fetch(rpcUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              jsonrpc: '2.0',
              method: 'eth_getBalance',
              params: [walletAddress, 'latest'],
              id: 1
            })
          });

          if (!response.ok) {
            console.log('❌ RPC request failed:', response.status);
            continue;
          }

          const data = await response.json();
          
          if (data.error) {
            console.log('❌ RPC error:', data.error);
            continue;
          }

          if (data.result) {
            // Convert from wei to HYPE (18 decimals)
            const balanceWei = BigInt(data.result);
            const balanceHype = Number(balanceWei) / Math.pow(10, 18);
            balance = balanceHype.toFixed(4);
            
            console.log('✅ Balance fetched:', balance, 'HYPE');
            break;
          }
        } catch (rpcError) {
          console.log('❌ RPC failed:', rpcUrl, rpcError.message);
          continue;
        }
      }

      if (balance !== null) {
        setHypeBalance(balance);
      } else {
        throw new Error('All RPC endpoints failed');
      }

    } catch (error) {
      console.error('❌ Failed to fetch HYPE balance:', error);
      setBalanceError('Failed to load balance');
      setHypeBalance('--');
    } finally {
      setIsLoadingBalance(false);
    }
  };

  // Get wallet address and fetch balance when it changes
  const walletAddress = user?.wallet?.address || user?.embeddedWallet?.address;
  
  useEffect(() => {
    console.log('📊 Portfolio page loaded, checking conditions:', { 
      authenticated, 
      walletAddress,
      userHasWallet: user?.wallet?.address || user?.embeddedWallet?.address 
    });
    
    // Always fetch HYPE price when page loads
    fetchHypePrice();
    
    if (authenticated && walletAddress) {
      console.log('🔄 Wallet address detected, fetching balance for:', walletAddress);
      fetchHypeBalance(walletAddress);
    } else {
      console.log('⚠️ Not fetching balance - missing:', { 
        authenticated: !authenticated ? 'NO AUTH' : 'OK',
        walletAddress: !walletAddress ? 'NO WALLET' : 'OK'
      });
    }
  }, [authenticated, walletAddress]);

  if (!authenticated) {
    return (
      <div className="portfolio-page">
        <div className="container">
          <div className="auth-required">
            <h2>Authentication Required</h2>
            <p>Please connect your wallet to view your portfolio.</p>
            <button className="btn btn-primary" onClick={login}>
              Connect Wallet
            </button>
            <button className="btn btn-secondary" onClick={() => navigate('/markets')}>
              Back to Markets
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Check if user has Twitter/X linked
  const twitterAccount = user?.linkedAccounts?.find(account => 
    ['twitter', 'twitter_oauth', 'twitter_oauth_1', 'x', 'x_oauth'].includes(account.type)
  );
  
  const hasTwitter = !!twitterAccount || !!user?.twitter;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || user?.twitter?.username || user?.twitter?.handle || twitterAccount?.name;

  return (
    <div className="portfolio-page">
      <header className="portfolio-header">
        <div className="container">
          <h1>My Portfolio</h1>
          <button className="btn btn-secondary" onClick={() => navigate('/markets')}>
            Back to Markets
          </button>
        </div>
      </header>
      <main className="portfolio-main">
        <div className="container">
          {/* Wallet + X Fund Transfer */}
          <WalletFundTransfer 
            onTransferComplete={() => {
              console.log('🎉 Fund transfer completed successfully!');
              // Refresh balance after transfer
              if (walletAddress) {
                fetchHypeBalance(walletAddress);
              }
            }}
          />

          {/* Account Overview */}
          <section className="account-overview">
            <h2>Account Overview</h2>
            <div className="overview-grid">
              <div className="overview-card">
                <h3>Wallet Address</h3>
                <p className="wallet-address">
                  {walletAddress ? `${walletAddress.slice(0, 6)}...${walletAddress.slice(-4)}` : 'Not connected'}
                </p>
              </div>
              <div className="overview-card">
                <h3>Connected Accounts</h3>
                <div className="connected-accounts">
                  {hasTwitter ? (
                    <div className="connected-item">
                      <span className="platform">𝕏 Twitter</span>
                      <span className="username">@{twitterUsername}</span>
                    </div>
                  ) : (
                    <p className="no-accounts">No social accounts connected</p>
                  )}
                </div>
              </div>
            </div>
          </section>

          {/* Your Holdings */}
          <section className="holdings-section">
            <h2>Your Holdings</h2>
            <div className="holdings-grid">
              <div className="holding-card">
                <h3>HyperEVM (HYPE)</h3>
                <div className="token-info">
                  <span className="balance">
                    {isLoadingBalance ? 'Loading...' : `${hypeBalance} HYPE`}
                  </span>
                  <span className="value">
                    {balanceError ? balanceError : (
                      isPriceLoading ? 'Loading price...' : (
                        hypePrice ? `$${(parseFloat(hypeBalance || 0) * hypePrice).toFixed(2)}` : '$0.00'
                      )
                    )}
                  </span>
                  {isLoadingBalance && (
                    <div className="loading-indicator">
                      <span className="spinner">⟳</span> Fetching from blockchain...
                    </div>
                  )}
                </div>
              </div>
            </div>
          </section>

          {/* Your Social Tokens */}
          <section className="social-tokens-section">
            <h2>Your Social Tokens</h2>
            <div className="tokens-grid">
              <div className="no-tokens">
                <p>No social tokens yet</p>
                <p className="help-text">Buy tokens from trending accounts to get started</p>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default Portfolio;