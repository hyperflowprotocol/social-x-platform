import React, { useState, useRef, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { PrivyProvider, usePrivy } from '@privy-io/react-auth';
// import { Analytics } from '@vercel/analytics/react';
import Markets from './pages/Markets';
import Portfolio from './pages/Portfolio';
import Launch from './pages/Launch';
import PrivyCallback from './components/PrivyCallback';
import './App.css';

// Get Privy App ID from environment or use the actual production ID
const PRIVY_APP_ID = import.meta.env.VITE_PRIVY_APP_ID || 'cmf0n2ra100qzl20b4gxr8ql0';

// Top Header Component
const TopHeader = () => {
  const { ready, authenticated, login, logout, user } = usePrivy();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  
  // Check if user has Twitter/X linked - correct Privy OAuth detection  
  const twitterAccount = user?.linkedAccounts?.find(account => 
    (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider)) ||
    ['twitter', 'twitter_oauth', 'oauth_twitter'].includes(account?.type)
  );
  
  const hasTwitter = !!twitterAccount || !!user?.twitter;
  const twitterUsername = twitterAccount?.username || twitterAccount?.handle || user?.twitter?.username || user?.twitter?.handle || twitterAccount?.name;
  
  const handleConnectWallet = () => {
    if (!authenticated) {
      login();
    }
  };

  const handleDropdownToggle = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const handleLogout = () => {
    console.log('🔴 Logout clicked from dropdown');
    logout();
    setDropdownOpen(false);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);


  return (
    <div className="top-header">
      <div className="container">
        <div className="header-content">
          {/* Left side - Logo */}
          <div className="logo-section">
            <h1 className="logo">Social X</h1>
          </div>
          
          {/* Right side - Wallet/Auth */}
          <div className="wallet-section" style={{marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '12px'}}>
            {!ready && (
              <button className="btn btn-primary" disabled>
                Loading...
              </button>
            )}
            
            {ready && !authenticated && (
              <button className="btn btn-primary" onClick={handleConnectWallet}>
                Connect Wallet
              </button>
            )}
            
            {ready && authenticated && (hasTwitter || user?.wallet) && (
              <div className="user-dropdown" ref={dropdownRef}>
                <button 
                  className={hasTwitter ? "x-connected dropdown-trigger" : "wallet-connected dropdown-trigger"}
                  onClick={handleDropdownToggle}
                >
                  {hasTwitter ? `@${twitterUsername} x` : `${user?.wallet?.address?.slice(0, 6)}...${user?.wallet?.address?.slice(-4)}`}
                  <span className="dropdown-arrow">▼</span>
                </button>
                
                {dropdownOpen && (
                  <div className="dropdown-menu">
                    <button className="dropdown-item" onClick={handleLogout}>
                      Disconnect
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Bottom Navigation Component  
const BottomNav = () => {
  const location = useLocation();
  
  return (
    <nav className="bottom-nav">
      <div className="container">
        <div className="nav-menu">
          <a href="/markets" className={`nav-link ${location.pathname === '/markets' ? 'active' : ''}`}>
            <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"></polyline>
            </svg>
            <span>Markets</span>
          </a>
          <a href="/portfolio" className={`nav-link ${location.pathname === '/portfolio' ? 'active' : ''}`}>
            <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <span>Portfolio</span>
          </a>
          <a href="/launch" className={`nav-link ${location.pathname === '/launch' ? 'active' : ''}`}>
            <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="7.5,4.21 12,6.81 16.5,4.21"></polyline>
              <polyline points="7.5,19.79 7.5,14.6 3,12"></polyline>
              <polyline points="21,12 16.5,14.6 16.5,19.79"></polyline>
            </svg>
            <span>Launch</span>
          </a>
        </div>
      </div>
    </nav>
  );
};

// App Layout Component
const AppLayout = () => {
  return (
    <div className="app-layout">
      <TopHeader />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/markets" replace />} />
          <Route path="/markets" element={<Markets />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/launch" element={<Launch />} />
          <Route path="/auth/privy-callback" element={<PrivyCallback />} />
        </Routes>
      </main>
      <BottomNav />
    </div>
  );
};

function App() {
  return (
    <PrivyProvider
      appId={PRIVY_APP_ID}
      config={{
        appearance: {
          theme: 'dark',
          accentColor: '#1DA1F2',
          showWalletLoginFirst: true,
          logo: 'https://gateway.pinata.cloud/ipfs/bafybeias4cbtyswqin32bdw6ncuw7m5j2ltdei4q5is6tipr4gqok5h53q',
          loginMessage: 'Connect your wallet or sign in with Twitter to start trading social tokens',
          // Configure wallet display order - OKX, MetaMask, and detected wallets (includes Bitget)
          walletList: [
            'okx_wallet',
            'metamask',
            'detected_wallets',
          ],
        },
        // Enable only wallet and Twitter login
        loginMethods: [
          'wallet',
          'twitter'
        ],
        // Safari compatibility fixes
        storage: {
          type: 'localStorage'
        },
        // Better Safari popup handling
        externalWallets: {
          coinbaseWallet: {
            connectionOptions: 'all',
          },
        },
        // Safari-specific OAuth fixes
        oauth: {
          disableSignups: false,
          forceTouchId: false,
        },
        // Configure supported chains - HyperEVM and Ethereum
        defaultChain: {
          id: 999,
          name: 'HyperEVM',
          network: 'hyperevm',
          nativeCurrency: {
            decimals: 18,
            name: 'HYPE',
            symbol: 'HYPE',
          },
          rpcUrls: {
            default: {
              http: ['https://rpc.hyperliquid.xyz/evm'],
            },
          },
        },
        supportedChains: [
          {
            id: 999,
            name: 'HyperEVM',
            network: 'hyperevm',
            nativeCurrency: {
              decimals: 18,
              name: 'HYPE',
              symbol: 'HYPE',
            },
            rpcUrls: {
              default: {
                http: ['https://rpc.hyperliquid.xyz/evm'],
              },
            },
          },
          {
            id: 8453,
            name: 'Base',
            network: 'base',
            nativeCurrency: {
              decimals: 18,
              name: 'Ether',
              symbol: 'ETH',
            },
            rpcUrls: {
              default: {
                http: ['https://mainnet.base.org'],
              },
            },
            blockExplorers: {
              default: {
                name: 'BaseScan',
                url: 'https://basescan.org',
              },
            },
          },
          {
            id: 1,
            name: 'Ethereum',
            network: 'mainnet',
            nativeCurrency: {
              decimals: 18,
              name: 'Ether',
              symbol: 'ETH',
            },
            rpcUrls: {
              default: {
                http: ['https://cloudflare-eth.com'],
              },
            },
          },
        ],
        // Embedded wallet configuration - only create for users without any wallet
        embeddedWallets: {
          createOnLogin: 'off', // Don't auto-create embedded wallets
          requireUserPasswordOnCreate: false,
          showWalletUIs: false, // Don't show embedded wallet UI, use external wallets
        },
        mfa: {
          noPromptOnMfaRequired: false,
        },
      }}
    >
      <Router>
        <AppLayout />
      </Router>
      {/* <Analytics /> */}
    </PrivyProvider>
  );
}

export default App;