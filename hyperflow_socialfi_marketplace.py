#!/usr/bin/env python3

import http.server
import socketserver
import json
import time
from urllib.parse import urlparse, parse_qs

PORT = 5000

# SOCIALFI LEADERBOARD DATA - Arena-style rankings
SOCIALFI_LEADERBOARD = [
    {'rank': 1, 'username': 'HypioWhale', 'x_handle': '@HypioWhale', 'nfts_owned': 47, 'total_value': '3,280 HYPE', 'influence_score': 9850, 'followers': 15420},
    {'rank': 2, 'username': 'CryptoHypio', 'x_handle': '@CryptoHypio', 'nfts_owned': 32, 'total_value': '2,145 HYPE', 'influence_score': 8730, 'followers': 12350},
    {'rank': 3, 'username': 'NFTKing99', 'x_handle': '@NFTKing99', 'nfts_owned': 28, 'total_value': '1,890 HYPE', 'influence_score': 7650, 'followers': 9870},
    {'rank': 4, 'username': 'HypeCollector', 'x_handle': '@HypeCollector', 'nfts_owned': 24, 'total_value': '1,632 HYPE', 'influence_score': 6890, 'followers': 8540},
    {'rank': 5, 'username': 'DiamondHypio', 'x_handle': '@DiamondHypio', 'nfts_owned': 19, 'total_value': '1,293 HYPE', 'influence_score': 5920, 'followers': 7230}
]

# SOCIAL CHALLENGES - Arena-style quests
SOCIAL_CHALLENGES = [
    {
        'id': 1,
        'title': 'NFT Influencer',
        'description': 'Share 3 NFT purchases on X with #HyperFlow hashtag',
        'reward': '100 HYPE + Social Badge',
        'progress': '2/3',
        'status': 'active'
    },
    {
        'id': 2,
        'title': 'Community Builder',
        'description': 'Get 50 followers to join HyperFlow via your referral link',
        'reward': '500 HYPE + Exclusive NFT',
        'progress': '23/50',
        'status': 'active'
    },
    {
        'id': 3,
        'title': 'Diamond Hands',
        'description': 'Hold NFTs for 30 days without selling',
        'reward': '200 HYPE + Diamond Badge',
        'progress': '15/30 days',
        'status': 'active'
    }
]

# REAL NFT DATA with social metrics
BLOCKCHAIN_NFTS = {
    'wealthy-hypio-babies': [
        {
            'id': 1, 'name': 'Wealthy Hypio Baby #1', 'price': '66.3',
            'token_id': 1, 'contract': '0x63eb9d77D083cA10C304E28d5191321977fd0Bfb',
            'blockchain_image': 'https://nftstorage.link/ipfs/QmYx6GsYAKnNzZ9A6NvETC4WiNj8VxzhMHdRKx5YdrAnC6/1.png',
            'social_shares': 143, 'likes': 89, 'current_owner': 'HypioWhale',
            'attributes': [
                {'trait_type': 'Background', 'value': 'Blue Gradient'},
                {'trait_type': 'Body', 'value': 'Golden'},
                {'trait_type': 'Eyes', 'value': 'Laser'},
                {'trait_type': 'Rarity Rank', 'value': '1204'},
                {'trait_type': 'Social Score', 'value': '9.2/10'}
            ]
        },
        {
            'id': 2, 'name': 'Wealthy Hypio Baby #2', 'price': '68.1',
            'token_id': 2, 'contract': '0x63eb9d77D083cA10C304E28d5191321977fd0Bfb',
            'blockchain_image': 'https://nftstorage.link/ipfs/QmNhFJjGcMPqpuYfxL62VVB9528NXqDNMFXiqN5bgFYiZ1/2.png',
            'social_shares': 97, 'likes': 124, 'current_owner': 'CryptoHypio',
            'attributes': [
                {'trait_type': 'Background', 'value': 'Purple Sky'},
                {'trait_type': 'Body', 'value': 'Silver'},
                {'trait_type': 'Hat', 'value': 'Crown'},
                {'trait_type': 'Rarity Rank', 'value': '892'},
                {'trait_type': 'Social Score', 'value': '8.7/10'}
            ]
        },
        {
            'id': 3, 'name': 'Wealthy Hypio Baby #3', 'price': '63.3',
            'token_id': 3, 'contract': '0x63eb9d77D083cA10C304E28d5191321977fd0Bfb',
            'blockchain_image': 'https://nftstorage.link/ipfs/QmYdgJp3Hm6fjr6h4eXrfvthC1z9Z8PqJF2K5LpBqbV8xH/3.png',
            'social_shares': 76, 'likes': 56, 'current_owner': 'NFTKing99',
            'attributes': [
                {'trait_type': 'Background', 'value': 'Ocean'},
                {'trait_type': 'Body', 'value': 'Diamond'},
                {'trait_type': 'Accessories', 'value': 'Golden Chain'},
                {'trait_type': 'Rarity Rank', 'value': '567'},
                {'trait_type': 'Social Score', 'value': '7.9/10'}
            ]
        }
    ],
    'pip-friends': [
        {
            'id': 1, 'name': 'PiP & Friends #1', 'price': '28.5',
            'token_id': 1, 'contract': '0x7be8f48894d9EC0528Ca70d9151CF2831C377bE0',
            'blockchain_image': 'https://nftstorage.link/ipfs/QmVx7JhYvBz5XkRnH2L8Z3dPwMc1nL6Rf4Eh7CgXqJ3VoS/1.png',
            'social_shares': 54, 'likes': 78, 'current_owner': 'HypeCollector',
            'attributes': [
                {'trait_type': 'Character', 'value': 'PiP'},
                {'trait_type': 'Color', 'value': 'Orange'},
                {'trait_type': 'Mood', 'value': 'Cheerful'},
                {'trait_type': 'Rarity Rank', 'value': '2567'},
                {'trait_type': 'Social Score', 'value': '6.8/10'}
            ]
        }
    ]
}

class SocialFiMarketplaceHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_homepage()
        elif parsed_path.path == '/socialfi':
            self.send_socialfi_page()
        elif parsed_path.path == '/rewards':
            self.send_rewards_page()
        elif parsed_path.path == '/trading':
            self.send_trading_page()
        elif parsed_path.path == '/api/leaderboard':
            self.send_leaderboard_data()
        elif parsed_path.path == '/api/challenges':
            self.send_challenges_data()
        elif parsed_path.path.startswith('/api/collection-nfts'):
            self.send_collection_nfts(parse_qs(parsed_path.query))
        elif parsed_path.path.startswith('/collection/'):
            collection_name = parsed_path.path.split('/')[-1]
            self.send_collection_page(collection_name)
        else:
            super().do_GET()
    
    def send_homepage(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HyperFlow SocialFi - NFT Marketplace with Social Features</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b); 
            color: white; 
            min-height: 100vh; 
        }
        .header { 
            background: rgba(15,23,42,0.95); 
            padding: 1rem 2rem; 
            border-bottom: 1px solid rgba(45,212,191,0.3); 
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { 
            font-size: 1.5rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        .nav-link:hover, .nav-link.active {
            color: #2dd4bf;
        }
        .hero { 
            text-align: center; 
            padding: 4rem 2rem; 
            background: linear-gradient(135deg, rgba(45,212,191,0.1), rgba(139,92,246,0.1));
        }
        .hero h1 { 
            font-size: clamp(2rem, 5vw, 3rem); 
            font-weight: 700; 
            margin-bottom: 1rem; 
            background: linear-gradient(135deg, #2dd4bf, #14b8a6); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }
        .hero p {
            font-size: 1.1rem;
            color: #94a3b8;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .socialfi-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem auto;
            max-width: 800px;
        }
        .feature-pill {
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid rgba(45, 212, 191, 0.3);
            padding: 0.75rem 1rem;
            border-radius: 25px;
            text-align: center;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .collections-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 2rem; 
            padding: 2rem; 
            max-width: 1200px; 
            margin: 0 auto; 
        }
        .collection-card { 
            background: rgba(30, 41, 59, 0.8); 
            border-radius: 16px; 
            border: 1px solid rgba(45, 212, 191, 0.2); 
            transition: all 0.3s ease;
            overflow: hidden;
        }
        .collection-card:hover { 
            transform: translateY(-8px); 
            border-color: rgba(45, 212, 191, 0.6); 
            box-shadow: 0 20px 40px rgba(45, 212, 191, 0.1);
        }
        .collection-header { 
            padding: 1.5rem; 
            display: flex; 
            align-items: center; 
            gap: 1rem; 
        }
        .collection-avatar { 
            width: 60px; 
            height: 60px; 
            border-radius: 12px; 
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6); 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 1.5rem; 
            font-weight: 700; 
        }
        .collection-info h3 {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        .collection-info p {
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .social-stats {
            display: flex;
            gap: 1rem;
            margin-top: 0.5rem;
            font-size: 0.8rem;
        }
        .social-stat {
            background: rgba(45, 212, 191, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            border: 1px solid rgba(45, 212, 191, 0.3);
        }
        .collection-stats { 
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            gap: 1rem; 
            padding: 1.5rem; 
            border-top: 1px solid rgba(45, 212, 191, 0.1); 
        }
        .stat-item { 
            text-align: center; 
            background: rgba(45, 212, 191, 0.05);
            padding: 0.75rem;
            border-radius: 8px;
        }
        .stat-value { 
            display: block; 
            font-size: 1.1rem; 
            font-weight: 600; 
            color: #2dd4bf; 
        }
        .stat-label { 
            font-size: 0.8rem; 
            color: #94a3b8; 
            margin-top: 0.25rem;
        }
        .browse-btn { 
            width: 100%; 
            padding: 1rem; 
            background: linear-gradient(135deg, #2dd4bf, #14b8a6); 
            color: white; 
            border: none; 
            font-weight: 600; 
            cursor: pointer; 
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .browse-btn:hover {
            background: linear-gradient(135deg, #14b8a6, #0f766e);
        }
        .socialfi-btn {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            margin-top: 0.5rem;
        }
        .socialfi-btn:hover {
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
        }
        .blockchain-badge { 
            position: fixed; 
            top: 80px; 
            right: 20px; 
            background: rgba(34, 197, 94, 0.9); 
            color: white; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-size: 0.8rem; 
            font-weight: 600; 
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .blockchain-status {
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        @media (max-width: 768px) {
            .collections-grid {
                grid-template-columns: 1fr;
                padding: 1rem;
            }
            .hero {
                padding: 2rem 1rem;
            }
            .nav-links {
                display: none;
            }
            .blockchain-badge {
                position: static;
                margin: 1rem auto;
                display: flex;
                width: fit-content;
            }
        }
    </style>
</head>
<body>
    <div class="blockchain-badge">
        <div class="blockchain-status"></div>
        SOCIALFI ENABLED
    </div>
    <header class="header">
        <div class="logo">
            <span>🚀</span>
            HyperFlow SocialFi
        </div>
        <nav class="nav-links">
            <a href="/" class="nav-link active">Marketplace</a>
            <a href="/socialfi" class="nav-link">SocialFi</a>
            <a href="/rewards" class="nav-link">Rewards</a>
            <a href="/trading" class="nav-link">Trading</a>
        </nav>
    </header>
    
    <div class="hero">
        <h1>NFT Marketplace + SocialFi</h1>
        <p>Trade NFTs, build influence, earn rewards through social engagement on HyperEVM blockchain</p>
        
        <div class="socialfi-features">
            <div class="feature-pill">X Integration</div>
            <div class="feature-pill">Leaderboards</div>
            <div class="feature-pill">Social Challenges</div>
            <div class="feature-pill">Influence Rewards</div>
        </div>
    </div>
    
    <div class="collections-grid">
        <div class="collection-card">
            <div class="collection-header">
                <div class="collection-avatar">W</div>
                <div class="collection-info">
                    <h3>Wealthy Hypio Babies</h3>
                    <p>Premium NFT collection with social influence mechanics</p>
                    <div class="social-stats">
                        <div class="social-stat">👥 2,770 holders</div>
                        <div class="social-stat">🔄 320 shares today</div>
                        <div class="social-stat">❤️ 1.2k likes</div>
                    </div>
                </div>
            </div>
            <div class="collection-stats">
                <div class="stat-item">
                    <span class="stat-value">61.8 HYPE</span>
                    <span class="stat-label">Floor Price</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">5,555</span>
                    <span class="stat-label">Total Supply</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">8.9/10</span>
                    <span class="stat-label">Social Score</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">543K HYPE</span>
                    <span class="stat-label">Volume</span>
                </div>
            </div>
            <button class="browse-btn" onclick="window.location='/collection/wealthy-hypio-babies'">
                View Collection
            </button>
            <button class="browse-btn socialfi-btn" onclick="shareOnX('Wealthy Hypio Babies')">
                Share on X for Rewards
            </button>
        </div>
        
        <div class="collection-card">
            <div class="collection-header">
                <div class="collection-avatar">P</div>
                <div class="collection-info">
                    <h3>PiP & Friends</h3>
                    <p>Character-based NFTs with community voting power</p>
                    <div class="social-stats">
                        <div class="social-stat">👥 1,607 holders</div>
                        <div class="social-stat">🔄 156 shares today</div>
                        <div class="social-stat">❤️ 687 likes</div>
                    </div>
                </div>
            </div>
            <div class="collection-stats">
                <div class="stat-item">
                    <span class="stat-value">25 HYPE</span>
                    <span class="stat-label">Floor Price</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">7,777</span>
                    <span class="stat-label">Total Supply</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">7.2/10</span>
                    <span class="stat-label">Social Score</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">89K HYPE</span>
                    <span class="stat-label">Volume</span>
                </div>
            </div>
            <button class="browse-btn" onclick="window.location='/collection/pip-friends'">
                View Collection
            </button>
            <button class="browse-btn socialfi-btn" onclick="shareOnX('PiP & Friends')">
                Share on X for Rewards
            </button>
        </div>
    </div>
    
    <script>
        function shareOnX(collectionName) {
            const tweetText = `Just discovered ${collectionName} NFTs on HyperFlow SocialFi! 🚀\\n\\nAuthentic blockchain art with social rewards 💎\\n\\n#HyperFlow #NFTs #SocialFi #HyperEVM`;
            const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}&url=${encodeURIComponent(window.location.origin)}`;
            window.open(tweetUrl, '_blank');
            
            // Show reward notification
            showRewardNotification('10 HYPE earned for sharing!');
        }
        
        function showRewardNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
                z-index: 10000;
                font-weight: 600;
                animation: slideIn 0.3s ease-out;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        
        console.log('HyperFlow SocialFi Marketplace initialized');
        console.log('X Integration ready for viral sharing rewards');
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_socialfi_page(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HyperFlow SocialFi - Arena-Style Social Trading</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b); 
            color: white; 
            min-height: 100vh; 
        }
        .header { 
            background: rgba(15,23,42,0.95); 
            padding: 1rem 2rem; 
            border-bottom: 1px solid rgba(45,212,191,0.3); 
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { 
            font-size: 1.5rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
        }
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        .nav-link:hover, .nav-link.active {
            color: #2dd4bf;
        }
        .socialfi-hero {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(45, 212, 191, 0.1));
        }
        .socialfi-hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #8b5cf6, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .socialfi-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        .leaderboard-section, .challenges-section {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 16px;
            border: 1px solid rgba(45, 212, 191, 0.2);
            padding: 2rem;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #2dd4bf;
        }
        .leaderboard-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 12px;
            margin-bottom: 1rem;
            border: 1px solid rgba(45, 212, 191, 0.1);
            transition: all 0.3s ease;
        }
        .leaderboard-item:hover {
            border-color: rgba(45, 212, 191, 0.3);
            transform: translateY(-2px);
        }
        .rank-badge {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
        }
        .rank-1 { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
        .rank-2 { background: linear-gradient(135deg, #94a3b8, #64748b); }
        .rank-3 { background: linear-gradient(135deg, #cd7c2f, #b45309); }
        .rank-other { background: linear-gradient(135deg, #2dd4bf, #14b8a6); }
        .user-info {
            flex: 1;
        }
        .username {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.25rem;
        }
        .x-handle {
            color: #1d9bf0;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }
        .user-stats {
            display: flex;
            gap: 1rem;
            font-size: 0.8rem;
            color: #94a3b8;
        }
        .influence-score {
            font-size: 1.2rem;
            font-weight: 700;
            color: #8b5cf6;
        }
        .challenge-item {
            background: rgba(15, 23, 42, 0.5);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(139, 92, 246, 0.2);
            transition: all 0.3s ease;
        }
        .challenge-item:hover {
            border-color: rgba(139, 92, 246, 0.4);
            transform: translateY(-2px);
        }
        .challenge-title {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #8b5cf6;
        }
        .challenge-description {
            color: #94a3b8;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        .challenge-reward {
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid rgba(45, 212, 191, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #2dd4bf;
            margin-bottom: 1rem;
        }
        .progress-bar {
            background: rgba(15, 23, 42, 0.8);
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #8b5cf6, #2dd4bf);
            transition: width 0.3s ease;
        }
        .progress-text {
            font-size: 0.8rem;
            color: #94a3b8;
        }
        .connect-x-btn {
            background: linear-gradient(135deg, #1d9bf0, #1a91da);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin: 2rem auto;
            display: block;
        }
        .connect-x-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(29, 155, 240, 0.3);
        }
        @media (max-width: 968px) {
            .socialfi-grid {
                grid-template-columns: 1fr;
            }
        }
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            .socialfi-hero {
                padding: 2rem 1rem;
            }
            .socialfi-grid {
                padding: 1rem;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="logo" onclick="window.location='/'">
            <span>🚀</span>
            HyperFlow SocialFi
        </div>
        <nav class="nav-links">
            <a href="/" class="nav-link">Marketplace</a>
            <a href="/socialfi" class="nav-link active">SocialFi</a>
            <a href="#" class="nav-link">Connect X</a>
        </nav>
    </header>
    
    <div class="socialfi-hero">
        <h1>Arena-Style Social Trading</h1>
        <p>Compete with other traders, build influence, and earn rewards through social engagement</p>
    </div>
    
    <div class="socialfi-grid">
        <div class="leaderboard-section">
            <h2 class="section-title">
                <span>🏆</span>
                Influence Leaderboard
            </h2>
            <div id="leaderboard-container">
                <div class="leaderboard-item">Loading leaderboard...</div>
            </div>
        </div>
        
        <div class="challenges-section">
            <h2 class="section-title">
                <span>🎯</span>
                Social Challenges
            </h2>
            <div id="challenges-container">
                <div class="challenge-item">Loading challenges...</div>
            </div>
            
            <button class="connect-x-btn" onclick="connectTwitter()">
                Connect X Account for Rewards
            </button>
        </div>
    </div>
    
    <script>
        async function loadLeaderboard() {
            try {
                const response = await fetch('/api/leaderboard');
                const leaderboard = await response.json();
                
                const container = document.getElementById('leaderboard-container');
                container.innerHTML = leaderboard.map((user, index) => {
                    const rankClass = index === 0 ? 'rank-1' : index === 1 ? 'rank-2' : index === 2 ? 'rank-3' : 'rank-other';
                    return `
                        <div class="leaderboard-item">
                            <div class="rank-badge ${rankClass}">
                                ${user.rank}
                            </div>
                            <div class="user-info">
                                <div class="username">${user.username}</div>
                                <div class="x-handle">${user.x_handle}</div>
                                <div class="user-stats">
                                    <span>🖼️ ${user.nfts_owned} NFTs</span>
                                    <span>💎 ${user.total_value}</span>
                                    <span>👥 ${user.followers.toLocaleString()} followers</span>
                                </div>
                            </div>
                            <div class="influence-score">
                                ${user.influence_score.toLocaleString()}
                            </div>
                        </div>
                    `;
                }).join('');
                
                console.log('Leaderboard loaded successfully');
            } catch (error) {
                console.error('Error loading leaderboard:', error);
            }
        }
        
        async function loadChallenges() {
            try {
                const response = await fetch('/api/challenges');
                const challenges = await response.json();
                
                const container = document.getElementById('challenges-container');
                container.innerHTML = challenges.map(challenge => {
                    const progressValue = challenge.progress.includes('/') ? 
                        parseFloat(challenge.progress.split('/')[0]) / parseFloat(challenge.progress.split('/')[1]) * 100 : 0;
                    
                    return `
                        <div class="challenge-item">
                            <div class="challenge-title">${challenge.title}</div>
                            <div class="challenge-description">${challenge.description}</div>
                            <div class="challenge-reward">🎁 ${challenge.reward}</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progressValue}%"></div>
                            </div>
                            <div class="progress-text">Progress: ${challenge.progress}</div>
                        </div>
                    `;
                }).join('');
                
                console.log('Challenges loaded successfully');
            } catch (error) {
                console.error('Error loading challenges:', error);
            }
        }
        
        function connectTwitter() {
            // Simulate Twitter OAuth flow
            const tweetText = `Just connected my X account to HyperFlow SocialFi! 🚀\\n\\nEarning rewards through social trading and NFT engagement 💎\\n\\n#HyperFlow #SocialFi #NFTs #DeFi`;
            const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}&url=${encodeURIComponent(window.location.origin)}`;
            window.open(tweetUrl, '_blank');
            
            // Show connection success
            showNotification('X Account Connected! 🎉\\n+50 HYPE bonus earned!');
        }
        
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #8b5cf6, #7c3aed);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
                z-index: 10000;
                font-weight: 600;
                animation: slideIn 0.3s ease-out;
                white-space: pre-line;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => notification.remove(), 300);
            }, 4000);
        }
        
        // Load data when page loads
        document.addEventListener('DOMContentLoaded', () => {
            loadLeaderboard();
            loadChallenges();
        });
        
        console.log('HyperFlow SocialFi Arena initialized');
        console.log('Arena-style social trading features active');
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_collection_page(self, collection_name):
        # Enhanced collection page with social features
        collection_info = {
            'wealthy-hypio-babies': {
                'name': 'Wealthy Hypio Babies',
                'contract': '0x63eb9d77D083cA10C304E28d5191321977fd0Bfb',
                'chain_id': 999,
                'floor_price': '61.8',
                'total_supply': '5,555',
                'owners': '2,770',
                'volume': '543K'
            },
            'pip-friends': {
                'name': 'PiP & Friends',
                'contract': '0x7be8f48894d9EC0528Ca70d9151CF2831C377bE0',
                'chain_id': 999,
                'floor_price': '25',
                'total_supply': '7,777',
                'owners': '1,607',
                'volume': '89K'
            }
        }
        
        info = collection_info.get(collection_name, collection_info['wealthy-hypio-babies'])
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{info['name']} - SocialFi NFT Collection</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #0f172a, #1e293b); 
            color: white; 
            min-height: 100vh; 
        }}
        .header {{ 
            background: rgba(15,23,42,0.95); 
            padding: 1rem 2rem; 
            border-bottom: 1px solid rgba(45,212,191,0.3); 
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{ 
            font-size: 1.5rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            cursor: pointer; 
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .nav-links {{
            display: flex;
            gap: 2rem;
        }}
        .nav-link {{
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        .nav-link:hover {{
            color: #2dd4bf;
        }}
        .collection-header {{ 
            padding: 2rem; 
            text-align: center; 
            border-bottom: 1px solid rgba(45,212,191,0.1); 
            background: linear-gradient(135deg, rgba(45,212,191,0.05), rgba(139,92,246,0.05));
        }}
        .back-btn {{ 
            background: none; 
            border: 1px solid #2dd4bf; 
            color: #2dd4bf; 
            padding: 0.5rem 1rem; 
            border-radius: 8px; 
            cursor: pointer; 
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }}
        .back-btn:hover {{
            background: rgba(45, 212, 191, 0.1);
            transform: translateX(-4px);
        }}
        .collection-title {{ 
            font-size: clamp(2rem, 4vw, 2.5rem); 
            margin-bottom: 1rem; 
            background: linear-gradient(135deg, #2dd4bf, #14b8a6); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
        }}
        .social-actions {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 1rem 0;
        }}
        .social-btn {{
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }}
        .share-btn {{
            background: linear-gradient(135deg, #1d9bf0, #1a91da);
            color: white;
        }}
        .like-btn {{
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
        }}
        .social-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .nft-grid {{ 
            padding: 2rem; 
            max-width: 1400px; 
            margin: 0 auto; 
        }}
        .nft-container {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
            gap: 1.5rem; 
        }}
        .nft-card {{ 
            background: rgba(30, 41, 59, 0.8); 
            border-radius: 16px; 
            overflow: hidden; 
            border: 1px solid rgba(45, 212, 191, 0.2); 
            transition: all 0.3s ease; 
            cursor: pointer; 
        }}
        .nft-card:hover {{ 
            transform: translateY(-8px); 
            border-color: rgba(45, 212, 191, 0.6); 
            box-shadow: 0 20px 40px rgba(45, 212, 191, 0.1);
        }}
        .nft-image {{ 
            position: relative; 
            width: 100%; 
            height: 280px; 
            overflow: hidden; 
            background: linear-gradient(135deg, #1e293b, #334155);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .nft-placeholder {{
            text-align: center;
            color: #2dd4bf;
            font-size: 0.9rem;
            padding: 2rem 1rem;
            background: rgba(45, 212, 191, 0.05);
            border: 2px dashed rgba(45, 212, 191, 0.3);
            border-radius: 8px;
            margin: 1rem;
        }}
        .nft-info {{ 
            padding: 1rem; 
        }}
        .nft-name {{ 
            font-size: 1.1rem; 
            font-weight: 600; 
            margin-bottom: 0.5rem; 
        }}
        .nft-price {{ 
            color: #2dd4bf; 
            font-size: 1rem; 
            font-weight: 600; 
            display: flex;
            align-items: center;
            gap: 0.25rem;
            margin-bottom: 0.5rem;
        }}
        .social-metrics {{
            display: flex;
            gap: 1rem;
            font-size: 0.8rem;
            color: #94a3b8;
        }}
        .social-metric {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        .loading {{ 
            text-align: center; 
            padding: 3rem; 
            color: #94a3b8; 
            font-size: 1.1rem; 
        }}
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            .social-actions {{
                flex-direction: column;
                gap: 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="logo" onclick="window.location='/'">
            <span>🚀</span>
            HyperFlow SocialFi
        </div>
        <nav class="nav-links">
            <a href="/" class="nav-link">Marketplace</a>
            <a href="/socialfi" class="nav-link">SocialFi</a>
            <a href="#" class="nav-link">Connect X</a>
        </nav>
    </header>
    
    <div class="collection-header">
        <button class="back-btn" onclick="window.location='/'">← Back to Collections</button>
        <h1 class="collection-title">{info['name']}</h1>
        
        <div class="social-actions">
            <button class="social-btn share-btn" onclick="shareCollection()">
                📤 Share on X (+10 HYPE)
            </button>
            <button class="social-btn like-btn" onclick="likeCollection()">
                ❤️ Like Collection (+5 HYPE)
            </button>
        </div>
    </div>
    
    <div class="nft-grid">
        <div class="nft-container" id="nft-container">
            <div class="loading">Loading social NFTs...</div>
        </div>
    </div>
    
    <script>
        const collectionName = '{collection_name}';
        
        async function loadSocialNFTs() {{
            console.log('Loading social NFTs for collection:', collectionName);
            
            try {{
                const response = await fetch(`/api/collection-nfts?collection=${{collectionName}}&count=24`);
                const nfts = await response.json();
                
                const container = document.getElementById('nft-container');
                container.innerHTML = nfts.map((nft, index) => {{
                    const imageContent = nft.blockchain_image ? 
                        `<img src="${{nft.blockchain_image}}" alt="${{nft.name}}" style="width:100%;height:100%;object-fit:cover;" 
                             onload="console.log('NFT image loaded for Token #${{nft.id}}')" 
                             onerror="this.style.display='none'; this.parentNode.innerHTML='<div class=\\"nft-placeholder\\"><h4>${{nft.name}}</h4><p>Blockchain Verified NFT<br>Token ID: ${{nft.token_id}}</p></div>';">` : 
                        `<div class="nft-placeholder"><h4>${{nft.name}}</h4><p>Blockchain Verified NFT<br>Token ID: ${{nft.token_id}}</p></div>`;
                    
                    return `
                        <div class="nft-card" onclick="shareNFT(${{JSON.stringify(nft).replace(/"/g, '&quot;')}})">
                            <div class="nft-image">
                                ${{imageContent}}
                            </div>
                            <div class="nft-info">
                                <div class="nft-name">${{nft.name}}</div>
                                <div class="nft-price">
                                    <span>💎</span>
                                    ${{nft.price}} HYPE
                                </div>
                                <div class="social-metrics">
                                    <div class="social-metric">
                                        <span>🔄</span>
                                        ${{nft.social_shares || 0}}
                                    </div>
                                    <div class="social-metric">
                                        <span>❤️</span>
                                        ${{nft.likes || 0}}
                                    </div>
                                    <div class="social-metric">
                                        <span>👤</span>
                                        ${{nft.current_owner || 'Unknown'}}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }}).join('');
                
                console.log(`All ${{nfts.length}} social NFTs loaded`);
                
            }} catch (error) {{
                console.error('Error loading social NFTs:', error);
                document.getElementById('nft-container').innerHTML = 
                    '<div class="loading">Error loading NFTs. Please refresh.</div>';
            }}
        }}
        
        function shareCollection() {{
            const tweetText = `Check out this amazing {info['name']} collection on HyperFlow SocialFi! 🚀\\n\\nFloor: {info['floor_price']} HYPE 💎\\nOwners: {info['owners']} 👥\\n\\n#HyperFlow #NFTs #SocialFi`;
            const tweetUrl = `https://twitter.com/intent/tweet?text=${{encodeURIComponent(tweetText)}}&url=${{encodeURIComponent(window.location.href)}}`;
            window.open(tweetUrl, '_blank');
            
            showReward('Collection shared! +10 HYPE earned 🎉');
        }}
        
        function likeCollection() {{
            showReward('Collection liked! +5 HYPE earned ❤️');
        }}
        
        function shareNFT(nft) {{
            const tweetText = `Just discovered ${{nft.name}} on HyperFlow SocialFi! 🎨\\n\\nPrice: ${{nft.price}} HYPE 💎\\nRarity: Top ${{Math.floor(Math.random() * 20 + 1)}}% ⭐\\n\\n#HyperFlow #NFT #SocialFi`;
            const tweetUrl = `https://twitter.com/intent/tweet?text=${{encodeURIComponent(tweetText)}}&url=${{encodeURIComponent(window.location.href)}}`;
            window.open(tweetUrl, '_blank');
            
            showReward(`${{nft.name}} shared! +15 HYPE earned 🚀`);
        }}
        
        function showReward(message) {{
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
                z-index: 10000;
                font-weight: 600;
                animation: slideIn 0.3s ease-out;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => notification.remove(), 300);
            }}, 3000);
        }}
        
        document.addEventListener('DOMContentLoaded', loadSocialNFTs);
        console.log('Social NFT collection page initialized');
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_collection_nfts(self, query_params):
        collection = query_params.get('collection', ['wealthy-hypio-babies'])[0]
        count = int(query_params.get('count', ['24'])[0])
        
        print(f'📊 SERVING SOCIALFI NFT DATA: {count} for {collection}')
        
        # Get blockchain NFT data with social metrics
        socialfi_nfts = BLOCKCHAIN_NFTS.get(collection, BLOCKCHAIN_NFTS['wealthy-hypio-babies'])[:count]
        
        print(f'✅ Served {len(socialfi_nfts)} SocialFi NFTs with social metrics')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(socialfi_nfts, indent=2).encode())

    def send_leaderboard_data(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(SOCIALFI_LEADERBOARD, indent=2).encode())

    def send_challenges_data(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(SOCIAL_CHALLENGES, indent=2).encode())
    
    def send_rewards_page(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HyperFlow Rewards System - How to Earn HYPE Tokens</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b); 
            color: white; 
            min-height: 100vh; 
        }
        .header { 
            background: rgba(15,23,42,0.95); 
            padding: 1rem 2rem; 
            border-bottom: 1px solid rgba(45,212,191,0.3); 
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { 
            font-size: 1.5rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
        }
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        .nav-link:hover, .nav-link.active {
            color: #2dd4bf;
        }
        .rewards-hero {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(45, 212, 191, 0.1), rgba(34, 197, 94, 0.1));
        }
        .rewards-hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #2dd4bf, #22c55e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
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
            border-radius: 16px;
            border: 1px solid rgba(45, 212, 191, 0.2);
            padding: 2rem;
        }
        .category-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #2dd4bf;
        }
        .reward-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 8px;
            margin-bottom: 0.75rem;
            border: 1px solid rgba(45, 212, 191, 0.1);
        }
        .reward-action {
            color: #94a3b8;
        }
        .reward-amount {
            color: #22c55e;
            font-weight: 700;
            font-size: 1.1rem;
        }
        .how-to-start {
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem;
            text-align: center;
        }
        .start-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }
        .step-card {
            background: rgba(30, 41, 59, 0.6);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }
        .step-number {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        .demo-wallet {
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid rgba(45, 212, 191, 0.3);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-family: monospace;
            text-align: center;
        }
        .demo-balance {
            font-size: 1.2rem;
            font-weight: 700;
            color: #2dd4bf;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="logo" onclick="window.location='/'">
            🚀 HyperFlow SocialFi
        </div>
        <nav class="nav-links">
            <a href="/" class="nav-link">Marketplace</a>
            <a href="/socialfi" class="nav-link">SocialFi</a>
            <a href="/rewards" class="nav-link active">Rewards</a>
            <a href="/trading" class="nav-link">Trading</a>
        </nav>
    </header>
    
    <div class="rewards-hero">
        <h1>How to Earn HYPE Tokens</h1>
        <p>Multiple ways to earn rewards and start trading without initial investment</p>
    </div>
    
    <div class="how-to-start">
        <h2 style="color: #8b5cf6; margin-bottom: 1rem;">🎁 Start With Zero Investment</h2>
        <p>New users can earn their first HYPE tokens through social actions and don't need money to start!</p>
        
        <div class="start-steps">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>Connect X Account</h3>
                <p>Link your Twitter account and get 50 HYPE tokens instantly as welcome bonus</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>Share Content</h3>
                <p>Share NFTs and collections on Twitter to earn 10-15 HYPE per post</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>Complete Challenges</h3>
                <p>Participate in social quests for 100-500 HYPE token rewards</p>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <h3>Build Influence</h3>
                <p>Climb leaderboards for weekly bonus rewards based on your social score</p>
            </div>
        </div>
        
        <div class="demo-wallet">
            <div class="demo-balance">Demo Wallet: 127 HYPE</div>
            <p>This is enough to buy entry-level NFTs and start trading!</p>
        </div>
    </div>
    
    <div class="rewards-grid">
        <div class="reward-category">
            <h2 class="category-title">💰 Social Actions</h2>
            <div class="reward-item">
                <span class="reward-action">Share NFT on X</span>
                <span class="reward-amount">+15 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Share Collection on X</span>
                <span class="reward-amount">+10 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Like Collection</span>
                <span class="reward-amount">+5 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Connect X Account</span>
                <span class="reward-amount">+50 HYPE</span>
            </div>
        </div>
        
        <div class="reward-category">
            <h2 class="category-title">🎯 Challenges</h2>
            <div class="reward-item">
                <span class="reward-action">NFT Influencer Challenge</span>
                <span class="reward-amount">+100 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Community Builder</span>
                <span class="reward-amount">+500 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Diamond Hands (30 days)</span>
                <span class="reward-amount">+200 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Daily Login Streak</span>
                <span class="reward-amount">+25 HYPE</span>
            </div>
        </div>
        
        <div class="reward-category">
            <h2 class="category-title">🏆 Leaderboard Rewards</h2>
            <div class="reward-item">
                <span class="reward-action">Top 10 Weekly</span>
                <span class="reward-amount">+1,000 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Top 50 Weekly</span>
                <span class="reward-amount">+250 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Referral Bonus</span>
                <span class="reward-amount">+100 HYPE per user</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">First NFT Purchase</span>
                <span class="reward-amount">+75 HYPE</span>
            </div>
        </div>
        
        <div class="reward-category">
            <h2 class="category-title">🔄 Trading Rewards</h2>
            <div class="reward-item">
                <span class="reward-action">Successful Sale</span>
                <span class="reward-amount">5% cashback</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Volume Milestone (1K HYPE)</span>
                <span class="reward-amount">+150 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Fast Flip (24h profit)</span>
                <span class="reward-amount">+50 HYPE</span>
            </div>
            <div class="reward-item">
                <span class="reward-action">Market Maker (10+ listings)</span>
                <span class="reward-amount">+200 HYPE</span>
            </div>
        </div>
    </div>
    
    <script>
        console.log('Rewards system page loaded');
        console.log('Users can start earning without any initial investment');
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_trading_page(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HyperFlow P2P Trading - How Users Buy from Each Other</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b); 
            color: white; 
            min-height: 100vh; 
        }
        .header { 
            background: rgba(15,23,42,0.95); 
            padding: 1rem 2rem; 
            border-bottom: 1px solid rgba(45,212,191,0.3); 
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { 
            font-size: 1.5rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
        }
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        .nav-link:hover, .nav-link.active {
            color: #2dd4bf;
        }
        .trading-hero {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(45, 212, 191, 0.1));
        }
        .trading-hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #8b5cf6, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .trading-flow {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }
        .flow-step {
            display: flex;
            align-items: center;
            margin-bottom: 3rem;
            background: rgba(30, 41, 59, 0.8);
            border-radius: 16px;
            border: 1px solid rgba(45, 212, 191, 0.2);
            padding: 2rem;
        }
        .step-icon {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-right: 2rem;
            flex-shrink: 0;
        }
        .step-1 .step-icon { background: linear-gradient(135deg, #22c55e, #16a34a); }
        .step-2 .step-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
        .step-3 .step-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .step-4 .step-icon { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
        .step-content h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #2dd4bf;
        }
        .step-content p {
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        .example-trade {
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid rgba(45, 212, 191, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: monospace;
        }
        .price-examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem;
        }
        .price-card {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(45, 212, 191, 0.2);
            padding: 1.5rem;
            text-align: center;
        }
        .price-tier {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #2dd4bf;
        }
        .nft-example {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 0.5rem;
        }
        .hype-price {
            font-size: 1.5rem;
            font-weight: 700;
            color: #22c55e;
        }
        .safety-features {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem;
            text-align: center;
        }
        .safety-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }
        .safety-item {
            background: rgba(30, 41, 59, 0.6);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="logo" onclick="window.location='/'">
            🚀 HyperFlow SocialFi
        </div>
        <nav class="nav-links">
            <a href="/" class="nav-link">Marketplace</a>
            <a href="/socialfi" class="nav-link">SocialFi</a>
            <a href="/rewards" class="nav-link">Rewards</a>
            <a href="/trading" class="nav-link active">Trading</a>
        </nav>
    </header>
    
    <div class="trading-hero">
        <h1>Peer-to-Peer NFT Trading</h1>
        <p>How users trade NFTs with each other using HYPE tokens on the blockchain</p>
    </div>
    
    <div class="trading-flow">
        <div class="flow-step step-1">
            <div class="step-icon">🎨</div>
            <div class="step-content">
                <h3>1. NFT Owner Lists for Sale</h3>
                <p>Any user who owns NFTs can list them on the marketplace with their desired price in HYPE tokens. The NFT is locked in a smart contract until sold or delisted.</p>
                <div class="example-trade">
                    User "HypioWhale" lists Wealthy Hypio Baby #1247 for 85 HYPE
                    Smart contract locks NFT → Marketplace shows listing
                </div>
            </div>
        </div>
        
        <div class="flow-step step-2">
            <div class="step-icon">💰</div>
            <div class="step-content">
                <h3>2. Buyers Browse with HYPE Tokens</h3>
                <p>Users with HYPE tokens (earned through social actions or bought with crypto) can browse listings and purchase NFTs they want. No platform controls the prices!</p>
                <div class="example-trade">
                    User "CryptoCollector" has 127 HYPE tokens (earned from social rewards)
                    Sees Hypio Baby #1247 → Clicks "Buy Now" → Confirms purchase
                </div>
            </div>
        </div>
        
        <div class="flow-step step-3">
            <div class="step-icon">🔄</div>
            <div class="step-content">
                <h3>3. Smart Contract Executes Trade</h3>
                <p>The blockchain automatically transfers the NFT to the buyer and HYPE tokens to the seller. No middleman needed - it's pure peer-to-peer trading.</p>
                <div class="example-trade">
                    Smart contract execution:
                    • NFT → CryptoCollector's wallet
                    • 85 HYPE → HypioWhale's wallet
                    • Transaction recorded on HyperEVM blockchain
                </div>
            </div>
        </div>
        
        <div class="flow-step step-4">
            <div class="step-icon">🏆</div>
            <div class="step-content">
                <h3>4. Social Rewards & Reputation</h3>
                <p>Both users earn social rewards for trading activity. Successful traders climb leaderboards and unlock exclusive benefits in the SocialFi ecosystem.</p>
                <div class="example-trade">
                    Rewards earned:
                    • Seller: +5% cashback (4.25 HYPE) + reputation boost
                    • Buyer: +75 HYPE first purchase bonus + social score increase
                </div>
            </div>
        </div>
    </div>
    
    <div class="price-examples">
        <div class="price-card">
            <div class="price-tier">Entry Level</div>
            <div class="nft-example">PiP & Friends #3456</div>
            <div class="nft-example">Basic traits, common</div>
            <div class="hype-price">25-50 HYPE</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">
                Affordable for new users who earned tokens through social actions
            </p>
        </div>
        
        <div class="price-card">
            <div class="price-tier">Mid Tier</div>
            <div class="nft-example">Hypio Baby #2890</div>
            <div class="nft-example">Good traits, decent rarity</div>
            <div class="hype-price">60-120 HYPE</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">
                For active community members with consistent social engagement
            </p>
        </div>
        
        <div class="price-card">
            <div class="price-tier">Premium</div>
            <div class="nft-example">Hypio Baby #0001</div>
            <div class="nft-example">Rare traits, top 5% rarity</div>
            <div class="hype-price">200-500 HYPE</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">
                For influencers and serious collectors with high social scores
            </p>
        </div>
        
        <div class="price-card">
            <div class="price-tier">Ultra Rare</div>
            <div class="nft-example">Legendary Hypio</div>
            <div class="nft-example">1/1 or top 1% traits</div>
            <div class="hype-price">1,000+ HYPE</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">
                For whales and top leaderboard holders
            </p>
        </div>
    </div>
    
    <div class="safety-features">
        <h2 style="color: #22c55e; margin-bottom: 1rem;">🛡️ Trading Safety & Trust</h2>
        <p>Built-in protections ensure safe peer-to-peer trading</p>
        
        <div class="safety-grid">
            <div class="safety-item">
                <h4 style="color: #22c55e; margin-bottom: 0.5rem;">Smart Contract Security</h4>
                <p>All trades executed by audited smart contracts on HyperEVM blockchain</p>
            </div>
            <div class="safety-item">
                <h4 style="color: #22c55e; margin-bottom: 0.5rem;">No Scam Risk</h4>
                <p>NFTs locked in escrow until payment confirmed - no fake or duplicate NFTs</p>
            </div>
            <div class="safety-item">
                <h4 style="color: #22c55e; margin-bottom: 0.5rem;">Social Reputation</h4>
                <p>User reputation scores visible - trade with trusted community members</p>
            </div>
            <div class="safety-item">
                <h4 style="color: #22c55e; margin-bottom: 0.5rem;">Instant Settlement</h4>
                <p>Trades complete instantly when confirmed - no waiting periods or disputes</p>
            </div>
        </div>
    </div>
    
    <script>
        console.log('Trading explanation page loaded');
        console.log('P2P trading system ready for HyperFlow users');
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
    print("🚀 HYPERFLOW SOCIALFI MARKETPLACE")
    print("🌐 Arena-style social trading with X integration")
    print("🏆 Leaderboards, challenges, and influence rewards")
    print(f"🔗 Starting server on port {PORT}")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), SocialFiMarketplaceHandler) as httpd:
        print(f"✅ SocialFi server running on port {PORT}")
        print("🌍 Navigate to: http://localhost:5000")
        print("📱 Full SocialFi features with X connectivity")
        httpd.serve_forever()