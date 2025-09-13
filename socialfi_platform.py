#!/usr/bin/env python3

import http.server
import socketserver
import json
import time
from urllib.parse import urlparse, parse_qs

PORT = 5000  # Main SocialFi platform port

# Arena-style SocialFi platform for HyperFlow
# Similar to Arena on Avalanche with X integration and influence-to-earn

# Live platform data
LEADERBOARD_DATA = [
    {"rank": 1, "username": "CryptoKing", "score": 4520, "followers": 12500, "shares_available": 15, "share_price": 85},
    {"rank": 2, "username": "NFTWhale", "score": 3890, "followers": 9800, "shares_available": 8, "share_price": 72},
    {"rank": 3, "username": "DeFiMaster", "score": 3420, "followers": 8200, "shares_available": 22, "share_price": 58},
    {"rank": 4, "username": "SocialTrader", "score": 2980, "followers": 6900, "shares_available": 35, "share_price": 45},
    {"rank": 5, "username": "InfluenceGuru", "score": 2650, "followers": 5400, "shares_available": 12, "share_price": 38},
    {"rank": 6, "username": "TrendSetter", "score": 2340, "followers": 4800, "shares_available": 28, "share_price": 32},
    {"rank": 7, "username": "ViralMeme", "score": 2100, "followers": 4200, "shares_available": 45, "share_price": 28},
    {"rank": 8, "username": "BlockchainBull", "score": 1890, "followers": 3600, "shares_available": 18, "share_price": 24},
    {"rank": 9, "username": "CommunityChamp", "score": 1650, "followers": 3100, "shares_available": 52, "share_price": 20},
    {"rank": 10, "username": "HypeBuilder", "score": 1420, "followers": 2800, "shares_available": 38, "share_price": 16}
]

USER_BALANCE = 127  # Starting demo balance

class SocialFiHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_main_page()
        elif self.path == '/rewards':
            self.send_rewards_page()
        elif self.path == '/trading':
            self.send_trading_page()
        elif self.path == '/economics':
            self.send_economics_page()
        elif self.path == '/api/leaderboard':
            self.send_leaderboard_api()
        elif self.path == '/api/influence-shares':
            self.send_influence_shares_api()
        elif self.path.startswith('/api/social-action'):
            self.handle_social_action()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/buy-share':
            self.handle_buy_share()
        elif self.path == '/api/social-action':
            self.handle_social_action()
        else:
            self.send_error(404, "Endpoint not found")
    
    def send_main_page(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>HyperFlow SocialFi Platform</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }
        .header {
            padding: 2rem;
            text-align: center;
            background: rgba(30,41,59,0.8);
            border-bottom: 2px solid #2dd4bf;
        }
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #2dd4bf, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .subtitle {
            color: #94a3b8;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .nav {
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .nav-btn {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: white;
            text-decoration: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(45, 212, 191, 0.3);
        }
        .nav-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(45, 212, 191, 0.4);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .feature-card {
            background: rgba(30, 41, 59, 0.8);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid rgba(45, 212, 191, 0.3);
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(45, 212, 191, 0.6);
        }
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        .feature-title {
            font-size: 1.5rem;
            color: #2dd4bf;
            margin-bottom: 1rem;
        }
        .feature-desc {
            color: #94a3b8;
            line-height: 1.6;
        }
        .cta-section {
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(139, 92, 246, 0.1);
            border-top: 2px solid #8b5cf6;
        }
        .cta-title {
            font-size: 2rem;
            color: #8b5cf6;
            margin-bottom: 1rem;
        }
        .cta-text {
            font-size: 1.1rem;
            color: #94a3b8;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .twitter-btn {
            background: linear-gradient(135deg, #1d9bf0, #1a91da);
            color: white;
            text-decoration: none;
            padding: 1.2rem 3rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .twitter-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(29, 155, 240, 0.4);
        }
        .action-btn {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
        }
        .modal-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border: 2px solid #2dd4bf;
            border-radius: 16px;
            padding: 2rem;
            max-width: 90vw;
            max-height: 90vh;
            overflow-y: auto;
            color: white;
        }
        .close-btn {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            font-size: 1.2rem;
        }
        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }
        .leaderboard-table th,
        .leaderboard-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid rgba(45, 212, 191, 0.2);
        }
        .leaderboard-table th {
            background: rgba(45, 212, 191, 0.1);
            color: #2dd4bf;
            font-weight: 700;
        }
        .buy-share-btn {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }
        .buy-share-btn:hover {
            transform: scale(1.05);
        }
        .buy-share-btn:disabled {
            background: #6b7280;
            cursor: not-allowed;
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .features { grid-template-columns: 1fr; padding: 2rem 1rem; }
            .nav { flex-direction: column; align-items: center; }
            .modal-content { padding: 1rem; }
            .leaderboard-table { font-size: 0.8rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>HyperFlow SocialFi</h1>
        <p class="subtitle">Arena-style social trading platform with X integration and influence-to-earn mechanics</p>
        <div class="nav">
            <a href="/rewards" class="nav-btn">Rewards System</a>
            <a href="/trading" class="nav-btn">Social Trading</a>
            <a href="/economics" class="nav-btn">Platform Economics</a>
            <a href="#" class="nav-btn" onclick="connectTwitter()">Connect X Account</a>
        </div>
    </div>
    
    <div class="features">
        <div class="feature-card" onclick="showLiveLeaderboard()">
            <div class="feature-icon">🏆</div>
            <h3 class="feature-title">Live Influence Leaderboards</h3>
            <p class="feature-desc">Real-time rankings of top social traders. Click to see current standings and available influence shares for investment.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Social Challenges</h3>
            <p class="feature-desc">Complete quests like sharing NFTs on X, building community, and diamond hands holding for exclusive rewards and badges.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <h3 class="feature-title">Viral Share Rewards</h3>
            <p class="feature-desc">Earn HYPE tokens for every NFT or collection you share on X. Build your social influence while earning trading capital.</p>
        </div>
        
        <div class="feature-card" onclick="showTradingInterface()">
            <div class="feature-icon">💎</div>
            <h3 class="feature-title">Social Influence Trading</h3>
            <p class="feature-desc">Buy and sell social influence shares from top performers. Click to open the live trading interface and start investing.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3 class="feature-title">Zero Investment Start</h3>
            <p class="feature-desc">New users earn their first HYPE tokens through social actions. Connect X account for 50 HYPE welcome bonus!</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Real-Time Analytics</h3>
            <p class="feature-desc">Track your social influence score, trading performance, and community impact with detailed analytics dashboard.</p>
        </div>
    </div>
    
    <div class="cta-section">
        <h2 class="cta-title">Start Earning Today</h2>
        <p class="cta-text">Connect your X account and start earning HYPE tokens through social engagement. No investment required to begin your SocialFi journey.</p>
        <div style="margin-bottom: 2rem;">
            <div style="background: rgba(45, 212, 191, 0.1); border: 1px solid #2dd4bf; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; font-family: monospace;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #2dd4bf;">Your Balance: <span id="user-balance">127</span> HYPE</div>
                <div style="font-size: 0.9rem; color: #94a3b8;">Earned through social engagement</div>
            </div>
        </div>
        
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem;">
            <button onclick="performSocialAction('share')" class="action-btn">Share on X (+0.5 HYPE)</button>
            <button onclick="performSocialAction('like')" class="action-btn">Like Content (+0.3 HYPE)</button>
            <button onclick="performSocialAction('connect')" class="action-btn">Connect X (+2 HYPE)</button>
        </div>
        
        <a href="#" class="twitter-btn" onclick="connectTwitter()">Open Live Trading Interface</a>
    </div>
    
    <!-- Live Leaderboard Modal -->
    <div id="leaderboard-modal" class="modal">
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal('leaderboard-modal')">&times;</button>
            <h2 style="color: #2dd4bf; margin-bottom: 1rem;">🏆 Live Influence Leaderboard</h2>
            <div id="leaderboard-content">Loading...</div>
        </div>
    </div>
    
    <!-- Trading Interface Modal -->
    <div id="trading-modal" class="modal">
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal('trading-modal')">&times;</button>
            <h2 style="color: #8b5cf6; margin-bottom: 1rem;">💎 Social Influence Trading</h2>
            <div style="background: rgba(45, 212, 191, 0.1); border: 1px solid #2dd4bf; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="font-weight: 700; color: #2dd4bf;">Your Balance: <span id="trading-balance">127</span> HYPE</div>
            </div>
            <div id="trading-content">Loading available shares...</div>
        </div>
    </div>
    
    <script>
        let userBalance = 127;
        
        function updateBalance(amount) {
            userBalance += amount;
            document.getElementById('user-balance').textContent = userBalance;
            const tradingBalance = document.getElementById('trading-balance');
            if (tradingBalance) tradingBalance.textContent = userBalance;
        }
        
        function performSocialAction(action) {
            const rewards = { share: 0.5, like: 0.3, connect: 2 };
            const messages = { 
                share: 'Shared on X! +0.5 HYPE earned', 
                like: 'Content liked! +0.3 HYPE earned',
                connect: 'X Account connected! +2 HYPE earned'
            };
            
            updateBalance(rewards[action]);
            showNotification(messages[action]);
            
            // Simulate API call
            fetch('/api/social-action?action=' + action)
                .catch(e => console.log('Demo mode - action recorded'));
        }
        
        function showLiveLeaderboard() {
            document.getElementById('leaderboard-modal').style.display = 'block';
            loadLeaderboard();
        }
        
        function showTradingInterface() {
            document.getElementById('trading-modal').style.display = 'block';
            loadTradingInterface();
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        function loadLeaderboard() {
            fetch('/api/leaderboard')
                .then(response => response.json())
                .then(data => {
                    const content = document.getElementById('leaderboard-content');
                    content.innerHTML = \`
                        <table class="leaderboard-table">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>User</th>
                                    <th>Score</th>
                                    <th>Followers</th>
                                    <th>Shares Available</th>
                                    <th>Price per Share</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                \${data.map(user => \`
                                    <tr>
                                        <td>#\${user.rank}</td>
                                        <td>\${user.username}</td>
                                        <td>\${user.score}</td>
                                        <td>\${user.followers.toLocaleString()}</td>
                                        <td>\${user.shares_available}</td>
                                        <td>\${user.share_price} HYPE</td>
                                        <td>
                                            <button class="buy-share-btn" onclick="buyShare('\${user.username}', \${user.share_price})" 
                                                \${userBalance < user.share_price ? 'disabled' : ''}>
                                                \${userBalance < user.share_price ? 'Insufficient Funds' : 'Buy Share'}
                                            </button>
                                        </td>
                                    </tr>
                                \`).join('')}
                            </tbody>
                        </table>
                    \`;
                })
                .catch(e => {
                    document.getElementById('leaderboard-content').innerHTML = 'Error loading leaderboard';
                });
        }
        
        function loadTradingInterface() {
            fetch('/api/influence-shares')
                .then(response => response.json())
                .then(data => {
                    const content = document.getElementById('trading-content');
                    content.innerHTML = \`
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                            \${data.map(share => \`
                                <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #2dd4bf; border-radius: 8px; padding: 1rem;">
                                    <h4 style="color: #2dd4bf; margin-bottom: 0.5rem;">\${share.username}</h4>
                                    <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 1rem;">
                                        <div>Rank: #\${share.rank}</div>
                                        <div>Monthly Earnings: \${share.monthly_earnings} HYPE</div>
                                        <div>Share Price: \${share.price} HYPE</div>
                                        <div>Returns: \${share.returns}% of earnings</div>
                                    </div>
                                    <button class="buy-share-btn" onclick="buyInfluenceShare('\${share.username}', \${share.price}, '\${share.returns}%')"
                                        \${userBalance < share.price ? 'disabled' : ''}>
                                        \${userBalance < share.price ? 'Insufficient Funds' : \`Buy \${share.returns}% Share\`}
                                    </button>
                                </div>
                            \`).join('')}
                        </div>
                    \`;
                })
                .catch(e => {
                    document.getElementById('trading-content').innerHTML = 'Error loading trading data';
                });
        }
        
        function buyShare(username, price) {
            if (userBalance >= price) {
                updateBalance(-price);
                showNotification(\`Purchased share of \${username} for \${price} HYPE!\\nYou now own part of their future earnings.\`);
                loadLeaderboard(); // Refresh the leaderboard
            }
        }
        
        function buyInfluenceShare(username, price, returns) {
            if (userBalance >= price) {
                updateBalance(-price);
                showNotification(\`Purchased \${returns} influence share of \${username}!\\nCost: \${price} HYPE\\nYou'll receive \${returns} of their monthly earnings.\`);
                loadTradingInterface(); // Refresh trading interface
            }
        }
        
        function connectTwitter() {
            const tweetText = \`Just joined HyperFlow SocialFi! 🚀\\n\\nEarning HYPE tokens through social trading and community engagement 💎\\n\\nArena-style leaderboards and Social Influence trading on HyperEVM blockchain ⚡\\n\\n#HyperFlow #SocialFi #DeFi #InfluenceTrading\`;
            const tweetUrl = \`https://twitter.com/intent/tweet?text=\${encodeURIComponent(tweetText)}&url=\${encodeURIComponent(window.location.origin)}\`;
            window.open(tweetUrl, '_blank');
            
            showTradingInterface();
        }
        
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = \`
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
                padding: 1rem 2rem;
                border-radius: 12px;
                box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
                z-index: 10000;
                font-weight: 600;
                white-space: pre-line;
                animation: slideIn 0.3s ease-out;
            \`;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => notification.remove(), 300);
            }, 4000);
        }
        
        const style = document.createElement('style');
        style.textContent = \`
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        \`;
        document.head.appendChild(style);
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }
        
        console.log('HyperFlow SocialFi Platform loaded');
        console.log('Live leaderboards and trading interface ready');
        console.log('Interactive social actions enabled');
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_rewards_page(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Rewards System - HyperFlow SocialFi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }
        .header {
            padding: 2rem;
            text-align: center;
            background: rgba(30,41,59,0.8);
            border-bottom: 2px solid #22c55e;
        }
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #22c55e, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .back-btn {
            background: #2dd4bf;
            color: #0f172a;
            text-decoration: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 1rem;
        }
        .start-guide {
            background: rgba(139, 92, 246, 0.1);
            border: 2px solid #8b5cf6;
            margin: 2rem;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
        }
        .guide-title {
            color: #8b5cf6;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        .demo-wallet {
            background: rgba(45, 212, 191, 0.1);
            border: 2px solid #2dd4bf;
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 1.2rem;
            font-weight: 700;
            color: #2dd4bf;
        }
        .rewards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .reward-category {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #2dd4bf;
            border-radius: 16px;
            padding: 2rem;
        }
        .category-title {
            color: #2dd4bf;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .reward-item {
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.7);
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid rgba(45, 212, 191, 0.3);
        }
        .reward-amount {
            color: #22c55e;
            font-weight: 700;
            font-size: 1.1rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="back-btn">← Back to SocialFi</a>
        <h1>How to Earn HYPE Tokens</h1>
        <p>Multiple ways to start earning without any investment</p>
    </div>
    
    <div class="start-guide">
        <h2 class="guide-title">Start With Zero Money</h2>
        <p>New users can earn their first HYPE tokens through social actions!</p>
        
        <div class="demo-wallet">
            Demo: After 1 week of social activity → 15-20 HYPE earned
        </div>
        
        <p>Start small, build reputation, earn more as you contribute to the community!</p>
    </div>
    
    <div class="rewards-grid">
        <div class="reward-category">
            <h3 class="category-title">💰 Social Actions</h3>
            <div class="reward-item">
                <span>Connect X Account (verified)</span>
                <span class="reward-amount">+2 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Share NFT on X (with engagement)</span>
                <span class="reward-amount">+0.5 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Share Collection (verified shares)</span>
                <span class="reward-amount">+0.3 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Daily check-in</span>
                <span class="reward-amount">+0.1 HYPE</span>
            </div>
        </div>
        
        <div class="reward-category">
            <h3 class="category-title">🎯 Weekly Challenges</h3>
            <div class="reward-item">
                <span>NFT Influencer (10 verified shares)</span>
                <span class="reward-amount">+5 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Community Builder (5 active referrals)</span>
                <span class="reward-amount">+10 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Diamond Hands (30 days hold)</span>
                <span class="reward-amount">+3 HYPE</span>
            </div>
        </div>
        
        <div class="reward-category">
            <h3 class="category-title">🏆 Leaderboard Bonuses</h3>
            <div class="reward-item">
                <span>Top 10 Weekly (proven activity)</span>
                <span class="reward-amount">+20 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Top 50 Weekly</span>
                <span class="reward-amount">+5 HYPE</span>
            </div>
            <div class="reward-item">
                <span>First NFT Purchase</span>
                <span class="reward-amount">+1 HYPE</span>
            </div>
        </div>
        
        <div class="reward-category">
            <h3 class="category-title">🔄 Trading Rewards</h3>
            <div class="reward-item">
                <span>Successful Sale (platform takes 2.5%)</span>
                <span class="reward-amount">0.5% cashback</span>
            </div>
            <div class="reward-item">
                <span>Active Trading (5+ trades)</span>
                <span class="reward-amount">+1 HYPE</span>
            </div>
            <div class="reward-item">
                <span>Market Maker (consistent listings)</span>
                <span class="reward-amount">+2 HYPE weekly</span>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_trading_page(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Social Influence Trading - HyperFlow SocialFi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }
        .header {
            padding: 2rem;
            text-align: center;
            background: rgba(30,41,59,0.8);
            border-bottom: 2px solid #8b5cf6;
        }
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #8b5cf6, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .back-btn {
            background: #2dd4bf;
            color: #0f172a;
            text-decoration: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 1rem;
        }
        .trading-steps {
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        .step {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #2dd4bf;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .step-number {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .step-title {
            color: #2dd4bf;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .step-desc {
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        .example {
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid #2dd4bf;
            padding: 1rem;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.9rem;
        }
        .price-examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            padding: 2rem;
            max-width: 1000px;
            margin: 0 auto;
        }
        .price-card {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #2dd4bf;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }
        .price-tier {
            color: #2dd4bf;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .hype-price {
            color: #22c55e;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="back-btn">← Back to SocialFi</a>
        <h1>How Social Influence Trading Works</h1>
        <p>Users buy and sell social influence points, reputation tokens, and creator shares</p>
    </div>
    
    <div class="trading-steps">
        <div class="step">
            <div class="step-number">1</div>
            <h3 class="step-title">Influencers List Social Shares</h3>
            <p class="step-desc">Top performers can tokenize their social influence and sell shares to investors. Buyers get a portion of future rewards earned by that influencer.</p>
            <div class="example">
User "CryptoKing" (Rank #5, 2.5K social score) lists 10% of future rewards
Price: 25 HYPE for 10% of monthly earnings → Listed on social marketplace
            </div>
        </div>
        
        <div class="step">
            <div class="step-number">2</div>
            <h3 class="step-title">Investors Buy Social Shares</h3>
            <p class="step-desc">Users can invest in promising creators by buying their social influence shares. Think of it like buying stock in someone's social media success.</p>
            <div class="example">
User "SmartInvestor" has 30 HYPE (earned from trading)
Sees CryptoKing's 10% share for 25 HYPE → Buys investment → Now owns 10% of his rewards
            </div>
        </div>
        
        <div class="step">
            <div class="step-number">3</div>
            <h3 class="step-title">Automatic Profit Sharing</h3>
            <p class="step-desc">When the influencer earns rewards, investors automatically receive their percentage. Smart contracts handle all distributions transparently.</p>
            <div class="example">
CryptoKing earns 20 HYPE this month from social activities
SmartInvestor automatically receives: 2 HYPE (10% of 20 HYPE)
Platform takes small fee, influencer keeps majority
            </div>
        </div>
        
        <div class="step">
            <div class="step-number">4</div>
            <h3 class="step-title">Secondary Market Trading</h3>
            <p class="step-desc">Investors can sell their influence shares to others if they think someone else will perform better, creating a dynamic social stock market.</p>
            <div class="example">
SmartInvestor's 10% CryptoKing share increased in value to 35 HYPE
Lists for sale → "TrendSpotter" buys it → SmartInvestor profits 10 HYPE
            </div>
        </div>
    </div>
    
    <h2 style="text-align: center; color: #8b5cf6; margin: 2rem 0;">Social Influence Share Prices</h2>
    <div class="price-examples">
        <div class="price-card">
            <div class="price-tier">Rising Creator</div>
            <p>Rank #100-500, growing fast</p>
            <div class="hype-price">5-15 HYPE</div>
            <p style="font-size: 0.9rem; color: #94a3b8;">10% share of future earnings</p>
        </div>
        
        <div class="price-card">
            <div class="price-tier">Solid Performer</div>
            <p>Rank #25-100, consistent</p>
            <div class="hype-price">20-40 HYPE</div>
            <p style="font-size: 0.9rem; color: #94a3b8;">10% share of proven earner</p>
        </div>
        
        <div class="price-card">
            <div class="price-tier">Top Influencer</div>
            <p>Rank #5-25, high social score</p>
            <div class="hype-price">50-100 HYPE</div>
            <p style="font-size: 0.9rem; color: #94a3b8;">5% share of top performer</p>
        </div>
        
        <div class="price-card">
            <div class="price-tier">Platform Whale</div>
            <p>Rank #1-5, legendary status</p>
            <div class="hype-price">150+ HYPE</div>
            <p style="font-size: 0.9rem; color: #94a3b8;">1% share of platform royalty</p>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_economics_page(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Platform Economics - HyperFlow SocialFi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }
        .header {
            padding: 2rem;
            text-align: center;
            background: rgba(30,41,59,0.8);
            border-bottom: 2px solid #f59e0b;
        }
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #f59e0b, #eab308);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .back-btn {
            background: #2dd4bf;
            color: #0f172a;
            text-decoration: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 1rem;
        }
        .revenue-summary {
            background: rgba(251, 191, 36, 0.1);
            border: 2px solid #f59e0b;
            margin: 2rem;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
        }
        .summary-title {
            color: #f59e0b;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        .total-revenue {
            font-size: 3rem;
            font-weight: 700;
            color: #22c55e;
            margin: 1rem 0;
        }
        .revenue-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .revenue-category {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #f59e0b;
            border-radius: 16px;
            padding: 2rem;
        }
        .category-title {
            color: #f59e0b;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .fee-item {
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.7);
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid rgba(251, 191, 36, 0.3);
        }
        .fee-amount {
            color: #22c55e;
            font-weight: 700;
            font-size: 1.1rem;
        }
        .example-box {
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid #2dd4bf;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-family: monospace;
            font-size: 0.9rem;
        }
        .profit-example {
            background: rgba(34, 197, 94, 0.1);
            border: 2px solid #22c55e;
            margin: 2rem;
            padding: 2rem;
            border-radius: 16px;
        }
        .profit-title {
            color: #22c55e;
            font-size: 1.8rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        .calculation {
            background: rgba(15, 23, 42, 0.8);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            font-family: monospace;
        }
        .highlight {
            color: #f59e0b;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="back-btn">← Back to SocialFi</a>
        <h1>Platform Economics</h1>
        <p>Transparent fee structure - Platform benefits first, users benefit second</p>
    </div>
    
    <div class="revenue-summary">
        <h2 class="summary-title">Platform Revenue Share</h2>
        <div class="total-revenue">60-80%</div>
        <p>Platform keeps majority of value generated, ensuring sustainability before rewarding users</p>
    </div>
    
    <div class="revenue-grid">
        <div class="revenue-category">
            <h3 class="category-title">💰 Trading Fees</h3>
            <div class="fee-item">
                <span>Social Influence Share Trade</span>
                <span class="fee-amount">2.5% platform fee</span>
            </div>
            <div class="fee-item">
                <span>User Cashback</span>
                <span class="fee-amount">0.5% to trader</span>
            </div>
            <div class="fee-item">
                <span>Net Platform Profit</span>
                <span class="fee-amount">2.0% per trade</span>
            </div>
            <div class="example-box">
Example: 100 HYPE trade
• Platform gets: 2.5 HYPE
• User cashback: 0.5 HYPE  
• Platform net: 2.0 HYPE profit
            </div>
        </div>
        
        <div class="revenue-category">
            <h3 class="category-title">📊 Profit Distribution Fees</h3>
            <div class="fee-item">
                <span>Monthly Influence Payouts</span>
                <span class="fee-amount">10% platform cut</span>
            </div>
            <div class="fee-item">
                <span>Processing & Smart Contracts</span>
                <span class="fee-amount">2% operational fee</span>
            </div>
            <div class="fee-item">
                <span>Total Platform Take</span>
                <span class="fee-amount">12% of all payouts</span>
            </div>
            <div class="example-box">
Example: Influencer earns 50 HYPE
• Platform fee: 6 HYPE (12%)
• Available for distribution: 44 HYPE
• Shareholders split the 44 HYPE
            </div>
        </div>
        
        <div class="revenue-category">
            <h3 class="category-title">⚡ Social Action Revenue</h3>
            <div class="fee-item">
                <span>User Reward (per share)</span>
                <span class="fee-amount">0.5 HYPE (~$0.10)</span>
            </div>
            <div class="fee-item">
                <span>Generated Value</span>
                <span class="fee-amount">~$1.00 total</span>
            </div>
            <div class="fee-item">
                <span>Platform Keeps</span>
                <span class="fee-amount">$0.90 (90%)</span>
            </div>
            <div class="example-box">
1000 social shares daily:
• Users earn: 500 HYPE ($100)
• Platform keeps: $900
• Platform profit margin: 90%
            </div>
        </div>
        
        <div class="revenue-category">
            <h3 class="category-title">🔥 Premium Features</h3>
            <div class="fee-item">
                <span>Advanced Analytics</span>
                <span class="fee-amount">5 HYPE/month</span>
            </div>
            <div class="fee-item">
                <span>Priority Listings</span>
                <span class="fee-amount">2 HYPE per listing</span>
            </div>
            <div class="fee-item">
                <span>Verified Creator Badge</span>
                <span class="fee-amount">10 HYPE one-time</span>
            </div>
            <div class="fee-item">
                <span>Custom Profile Themes</span>
                <span class="fee-amount">3 HYPE/month</span>
            </div>
        </div>
    </div>
    
    <div class="profit-example">
        <h2 class="profit-title">Monthly Revenue Example</h2>
        
        <div class="calculation">
            <div><span class="highlight">Trading Volume:</span> 10,000 HYPE/month</div>
            <div><span class="highlight">Platform Trading Fees:</span> 250 HYPE (2.5%)</div>
        </div>
        
        <div class="calculation">
            <div><span class="highlight">Social Actions:</span> 5,000 shares/month</div>
            <div><span class="highlight">Platform Social Revenue:</span> ~$4,500 (90% of value)</div>
        </div>
        
        <div class="calculation">
            <div><span class="highlight">Influence Payouts:</span> 2,000 HYPE distributed</div>
            <div><span class="highlight">Platform Distribution Fees:</span> 240 HYPE (12%)</div>
        </div>
        
        <div class="calculation">
            <div><span class="highlight">Premium Subscriptions:</span> 100 users × 8 HYPE average</div>
            <div><span class="highlight">Premium Revenue:</span> 800 HYPE/month</div>
        </div>
        
        <div class="calculation" style="border: 2px solid #22c55e; background: rgba(34, 197, 94, 0.2);">
            <div style="font-size: 1.2rem;"><span class="highlight">TOTAL MONTHLY PLATFORM PROFIT:</span></div>
            <div style="font-size: 1.5rem; color: #22c55e; font-weight: 700;">1,290 HYPE + $4,500 USD</div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 0.5rem;">
                Platform keeps 70-80% of all value generated, ensuring sustainable growth
            </div>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_leaderboard_api(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(LEADERBOARD_DATA).encode())
    
    def send_influence_shares_api(self):
        # Generate influence shares for trading
        shares_data = [
            {
                "username": "CryptoKing",
                "rank": 1,
                "monthly_earnings": 45,
                "price": 85,
                "returns": 10,
                "available": 15
            },
            {
                "username": "NFTWhale", 
                "rank": 2,
                "monthly_earnings": 38,
                "price": 72,
                "returns": 10,
                "available": 8
            },
            {
                "username": "DeFiMaster",
                "rank": 3,
                "monthly_earnings": 32,
                "price": 58,
                "returns": 15,
                "available": 22
            },
            {
                "username": "SocialTrader",
                "rank": 4,
                "monthly_earnings": 28,
                "price": 45,
                "returns": 12,
                "available": 35
            },
            {
                "username": "InfluenceGuru",
                "rank": 5,
                "monthly_earnings": 24,
                "price": 38,
                "returns": 20,
                "available": 12
            },
            {
                "username": "TrendSetter",
                "rank": 6,
                "monthly_earnings": 20,
                "price": 32,
                "returns": 15,
                "available": 28
            }
        ]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(shares_data).encode())
    
    def handle_social_action(self):
        # Handle social action rewards
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"status": "success", "message": "Social action recorded"}
        self.wfile.write(json.dumps(response).encode())
    
    def handle_buy_share(self):
        # Handle influence share purchases
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"status": "success", "message": "Share purchased"}
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    print("🚀 HyperFlow SocialFi Platform Starting...")
    print("🌐 Arena-style social trading ready")  
    print("💰 X integration for viral rewards")
    print(f"🔗 Starting server on port {PORT}")
    
    try:
        # Allow port reuse to avoid conflicts
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("0.0.0.0", PORT), SocialFiHandler) as httpd:
            print(f"✅ Server running: http://localhost:{PORT}")
            print("🎯 Interactive social trading platform ready")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Port {PORT} in use, trying {PORT+1}...")
            PORT += 1
            try:
                with socketserver.TCPServer(("0.0.0.0", PORT), SocialFiHandler) as httpd:
                    print(f"✅ Server running: http://localhost:{PORT}")
                    httpd.serve_forever()
            except Exception as e2:
                print(f"❌ Failed to start on {PORT}: {e2}")
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("\n🔄 Server stopped")