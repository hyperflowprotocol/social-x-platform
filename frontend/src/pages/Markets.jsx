import React, { useState, useEffect } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import axios from 'axios';
import './Markets.css';

const Markets = () => {
  const { ready, authenticated, user, login, logout } = usePrivy();
  const [trendingAccounts, setTrendingAccounts] = useState([]);
  const [recentTrades, setRecentTrades] = useState([]);
  const [marketOverview, setMarketOverview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMarketData();
    const interval = setInterval(fetchMarketData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchMarketData = async () => {
    try {
      const [overviewRes, trendingRes, tradesRes] = await Promise.all([
        axios.get('/api/market-overview'),
        axios.get('/api/trending-accounts'),
        axios.get('/api/recent-trades')
      ]);

      setMarketOverview(overviewRes.data);
      setTrendingAccounts(trendingRes.data.accounts || []);
      setRecentTrades(tradesRes.data.trades || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching market data:', err);
      setError('Failed to load market data');
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(2)}K`;
    return num?.toFixed(2) || '0';
  };

  const formatPrice = (price) => {
    return `$${price?.toFixed(4) || '0.0000'}`;
  };

  return (
    <div className="markets-page">
      <div className="container">
        <h1 className="page-title">Markets</h1>
        
        {/* Market Overview Card */}
        <section className="market-overview">
          <div className="overview-card card">
            <h2 className="overview-title">Market Overview</h2>
            <div className="overview-stats">
              <div className="stat-item">
                <div className="stat-value">{marketOverview?.active_accounts || 0}</div>
                <div className="stat-label">Total Accounts</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">$0</div>
                <div className="stat-label">Market Cap</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">$0</div>
                <div className="stat-label">24H Volume</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">0</div>
                <div className="stat-label">Active Traders</div>
              </div>
            </div>
          </div>
        </section>

        {/* Trending Accounts */}
        <section className="trending-section">
          <h2 className="section-title">Trending Accounts</h2>
          {loading ? (
            <div className="loading">Loading trending accounts...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : (
            <div className="accounts-grid">
              {trendingAccounts.map((account, index) => (
                <div key={account.handle || index} className="account-card card">
                  <div className="account-header">
                    <img 
                      src={account.avatar || '/default-avatar.png'} 
                      alt={account.name}
                      className="account-avatar"
                    />
                    <div className="account-info">
                      <h3 className="account-name">{account.name}</h3>
                      <span className="account-handle">@{account.handle}</span>
                    </div>
                  </div>
                  
                  <div className="account-stats">
                    <div className="stat">
                      <span className="stat-label">Price</span>
                      <span className="stat-value">{formatPrice(account.price_per_token)}</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Market Cap</span>
                      <span className="stat-value">{formatPrice(account.market_cap)}</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">24h Change</span>
                      <span className={`stat-value ${account.daily_change >= 0 ? 'positive' : 'negative'}`}>
                        {account.daily_change >= 0 ? '+' : ''}{account.daily_change?.toFixed(2)}%
                      </span>
                    </div>
                  </div>

                  <div className="account-actions">
                    <button className="btn btn-primary btn-sm">Trade</button>
                    <button className="btn btn-secondary btn-sm">Details</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Recent Trades */}
        <section className="trades-section">
          <h2 className="section-title">Recent Trades</h2>
          {recentTrades.length > 0 ? (
            <div className="trades-table">
              <div className="table-header">
                <div className="table-cell">Account</div>
                <div className="table-cell">Type</div>
                <div className="table-cell">Amount</div>
                <div className="table-cell">Price</div>
                <div className="table-cell">Time</div>
              </div>
              {recentTrades.map((trade, index) => (
                <div key={trade.id || index} className="table-row">
                  <div className="table-cell">@{trade.account}</div>
                  <div className="table-cell">
                    <span className={`trade-type ${trade.type}`}>{trade.type}</span>
                  </div>
                  <div className="table-cell">{trade.shares} shares</div>
                  <div className="table-cell">{formatPrice(trade.price)}</div>
                  <div className="table-cell">{new Date(trade.timestamp).toLocaleTimeString()}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-trades">No recent trades</div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Markets;