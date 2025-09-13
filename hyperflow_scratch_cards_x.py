#!/usr/bin/env python3
"""
HyperFlow Scratch Cards - X (Twitter) Connected Version
Instant-win scratch card game with X authentication instead of wallet
Features: Different card rarities, bonus multipliers, X social login
"""

import http.server
import socketserver
import json
import random
import time
from datetime import datetime

PORT = 5001

class ScratchCardGame:
    def __init__(self):
        self.card_types = {
            'bronze': {'cost': 1, 'min_prize': 0.5, 'max_prize': 3, 'win_rate': 0.3, 'jackpot': 10},
            'silver': {'cost': 5, 'min_prize': 2, 'max_prize': 15, 'win_rate': 0.3, 'jackpot': 50},
            'gold': {'cost': 20, 'min_prize': 10, 'max_prize': 80, 'win_rate': 0.3, 'jackpot': 250},
            'diamond': {'cost': 100, 'min_prize': 50, 'max_prize': 500, 'win_rate': 0.3, 'jackpot': 1000}
        }
        self.recent_wins = []
        self.prize_pool = 500  # Accumulated prize pool
        self.stats = {
            'total_cards_sold': 0,
            'total_prizes_won': 0,
            'biggest_win': 0,
            'active_players': random.randint(150, 400),
            'house_edge': 0.15  # 15% house edge
        }
        
        # Auto-generate some initial activity
        self._generate_initial_activity()
    
    def _generate_initial_activity(self):
        """Generate some initial scratch card activity for realism"""
        for _ in range(random.randint(5, 12)):
            card_type = random.choice(['bronze', 'silver', 'gold', 'diamond'])
            fake_result = self._simulate_card_result(card_type)
            if fake_result['winner']:
                self.recent_wins.append({
                    'type': card_type,
                    'prize': fake_result['prize'],
                    'bonus': fake_result['bonus_multiplier'] > 1,
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'player': f"@user{random.randint(1000, 9999)}"
                })
                self.stats['total_prizes_won'] += fake_result['prize']
                if fake_result['prize'] > self.stats['biggest_win']:
                    self.stats['biggest_win'] = fake_result['prize']
            self.stats['total_cards_sold'] += 1
    
    def _simulate_card_result(self, card_type):
        """Simulate a card result without affecting game state"""
        card_config = self.card_types[card_type]
        is_winner = random.random() < card_config['win_rate']
        
        if is_winner:
            min_prize = card_config['min_prize']
            max_prize = card_config['max_prize']
            rand = random.random()
            if rand < 0.6:
                prize = round(random.uniform(min_prize, min_prize + (max_prize - min_prize) / 3), 2)
            elif rand < 0.85:
                prize = round(random.uniform(min_prize + (max_prize - min_prize) / 3, 
                                           min_prize + 2 * (max_prize - min_prize) / 3), 2)
            else:
                prize = round(random.uniform(min_prize + 2 * (max_prize - min_prize) / 3, max_prize), 2)
            
            bonus_multiplier = 1
            if random.random() < 0.05:
                bonus_multiplier = 2
            elif random.random() < 0.02:
                bonus_multiplier = 5
            
            return {'winner': True, 'prize': prize * bonus_multiplier, 'bonus_multiplier': bonus_multiplier}
        return {'winner': False, 'prize': 0, 'bonus_multiplier': 1}

    def generate_card_result(self, card_type):
        card_config = self.card_types[card_type]
        
        # Add to prize pool from card purchase (house edge calculation)
        cost = card_config['cost']
        house_take = int(cost * self.stats['house_edge'])
        prize_contribution = cost - house_take
        self.prize_pool += prize_contribution
        
        is_winner = random.random() < card_config['win_rate']
        
        if is_winner:
            # Generate prize amount
            min_prize = card_config['min_prize']
            max_prize = card_config['max_prize']
            
            # Weighted distribution - more small wins, fewer big wins
            rand = random.random()
            if rand < 0.6:  # 60% small wins
                prize = round(random.uniform(min_prize, min_prize + (max_prize - min_prize) / 3), 2)
            elif rand < 0.85:  # 25% medium wins
                prize = round(random.uniform(min_prize + (max_prize - min_prize) / 3, 
                                           min_prize + 2 * (max_prize - min_prize) / 3), 2)
            else:  # 15% big wins
                prize = round(random.uniform(min_prize + 2 * (max_prize - min_prize) / 3, max_prize), 2)
            
            # Special bonus and jackpot chances
            bonus_multiplier = 1
            jackpot_chance = 0.001  # 0.1% chance for jackpot
            
            if random.random() < jackpot_chance:
                final_prize = card_config['jackpot']
                bonus_multiplier = 10  # Jackpot indicator
            else:
                if random.random() < 0.05:  # 5% chance for 2x bonus
                    bonus_multiplier = 2
                elif random.random() < 0.02:  # 2% chance for 5x bonus
                    bonus_multiplier = 5
                
                final_prize = prize * bonus_multiplier
            
            # Deduct from prize pool
            self.prize_pool = max(0, self.prize_pool - final_prize)
            
            # Update stats
            self.stats['total_cards_sold'] += 1
            self.stats['total_prizes_won'] += final_prize
            if final_prize > self.stats['biggest_win']:
                self.stats['biggest_win'] = final_prize
            
            # Add to recent wins with Twitter handle format
            self.recent_wins.insert(0, {
                'type': card_type,
                'prize': final_prize,
                'bonus': bonus_multiplier > 1,
                'time': datetime.now().strftime('%H:%M:%S'),
                'player': f"@user{random.randint(1000, 9999)}"
            })
            
            if len(self.recent_wins) > 15:
                self.recent_wins.pop()
            
            return {
                'winner': True,
                'prize': final_prize,
                'bonus_multiplier': bonus_multiplier,
                'symbols': self.generate_winning_symbols(card_type)
            }
        else:
            self.stats['total_cards_sold'] += 1
            return {
                'winner': False,
                'prize': 0,
                'bonus_multiplier': 1,
                'symbols': self.generate_losing_symbols(card_type)
            }
    
    def generate_winning_symbols(self, card_type):
        # Using official crypto logos from CDN sources
        hype_logo = 'https://assets.coingecko.com/coins/images/31503/thumb/hyperliquid.jpg'
        eth_logo = 'https://assets.coingecko.com/coins/images/279/thumb/ethereum.png'  
        btc_logo = 'https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png'
        
        winning_symbol = hype_logo
        other_symbols = [eth_logo, btc_logo]
        
        # Generate 9 symbols with 3 matching HYPE logos for win
        result = []
        positions = random.sample(range(9), 3)  # 3 random positions for winning symbols
        
        for i in range(9):
            if i in positions:
                result.append(winning_symbol)
            else:
                result.append(random.choice(other_symbols))
        
        return result
    
    def generate_losing_symbols(self, card_type):
        # Different crypto logos to avoid 3 HYPE matches
        hype_logo = 'https://assets.coingecko.com/coins/images/31503/thumb/hyperliquid.jpg'
        eth_logo = 'https://assets.coingecko.com/coins/images/279/thumb/ethereum.png'
        btc_logo = 'https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png'
        
        symbols = [hype_logo, eth_logo, btc_logo]
        result = []
        
        # Ensure no 3 matching symbols
        for i in range(9):
            available = symbols.copy()
            # Count occurrences of each symbol to prevent 3 matches
            if i >= 2:
                counts = {}
                for symbol in symbols:
                    counts[symbol] = result.count(symbol)
                # Remove symbols that already have 2 occurrences
                available = [s for s in available if counts.get(s, 0) < 2]
            
            if not available:
                available = symbols.copy()
                
            result.append(random.choice(available))
        
        return result

scratch_game = ScratchCardGame()

class ScratchCardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow Scratch Cards - Connect with X</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 60%),
                radial-gradient(circle at 80% 20%, rgba(0, 153, 204, 0.1) 0%, transparent 60%),
                radial-gradient(circle at 50% 50%, rgba(16, 33, 62, 0.8) 0%, transparent 100%),
                linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white; min-height: 100vh; overflow-x: hidden;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { 
            font-size: 3rem; 
            background: linear-gradient(45deg, #00d4ff, #0099cc, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            position: relative;
        }
        
        .auth-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(0, 212, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .auth-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.05) 0%, transparent 70%);
            animation: rotate-bg 20s linear infinite;
        }
        
        @keyframes rotate-bg {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .connect-x-btn {
            background: linear-gradient(135deg, #1da1f2, #0d8bd9);
            color: white;
            border: none;
            padding: 18px 36px;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.4s ease;
            box-shadow: 
                0 4px 15px rgba(29, 161, 242, 0.4),
                0 0 0 0 rgba(29, 161, 242, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 12px;
            position: relative;
            z-index: 10;
            overflow: hidden;
        }
        
        .connect-x-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: all 0.6s ease;
        }
        
        .connect-x-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 
                0 8px 25px rgba(29, 161, 242, 0.6),
                0 0 0 8px rgba(29, 161, 242, 0.1);
        }
        
        .connect-x-btn:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .connect-x-btn:active {
            transform: translateY(-1px) scale(1.02);
        }
        
        .twitter-icon {
            width: 24px;
            height: 24px;
            fill: currentColor;
        }
        
        .user-profile {
            display: none;
            align-items: center;
            gap: 15px;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 25px;
            border-radius: 50px;
            margin: 20px auto;
            max-width: fit-content;
        }
        
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid #00d4ff;
        }
        
        .user-info h3 {
            color: #00d4ff;
            margin: 0;
        }
        
        .user-info p {
            color: #B0B0B0;
            margin: 0;
            font-size: 0.9rem;
        }
        
        .game-section {
            display: none;
        }
        
        .game-section.active {
            display: block;
        }
        
        .hype-logo {
            display: inline-block;
            width: 60px; height: 60px;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border-radius: 50%; margin: 0 15px;
            position: relative; vertical-align: middle;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.6), inset 0 0 20px rgba(255, 255, 255, 0.1);
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        .hype-logo::before {
            content: 'H'; position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            color: white; font-weight: bold; font-size: 1.8rem;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.6), inset 0 0 20px rgba(255, 255, 255, 0.1); }
            50% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.8), inset 0 0 30px rgba(255, 255, 255, 0.2); }
        }
        
        .cards-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 35px; margin-bottom: 40px;
            justify-items: center;
        }
        
        .card-type {
            background: rgba(255, 255, 255, 0.08); 
            border-radius: 25px; 
            padding: 35px;
            backdrop-filter: blur(15px); 
            text-align: center; 
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
            border: 2px solid transparent;
            position: relative;
            max-width: 350px;
            width: 100%;
            overflow: hidden;
        }
        
        .card-type::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 25px;
            padding: 2px;
            background: linear-gradient(135deg, transparent, rgba(0, 212, 255, 0.3), transparent);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: exclude;
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.4s ease;
        }
        
        .card-type:hover { 
            transform: translateY(-8px) scale(1.02); 
            border-color: transparent;
        }
        
        .card-type:hover::before {
            opacity: 1;
        }
        
        .card-bronze { 
            background: linear-gradient(135deg, rgba(205, 127, 50, 0.4), rgba(139, 69, 19, 0.4)); 
            border: 3px solid #CD7F32;
            box-shadow: 0 8px 25px rgba(205, 127, 50, 0.3);
        }
        .card-silver { 
            background: linear-gradient(135deg, rgba(192, 192, 192, 0.4), rgba(169, 169, 169, 0.4)); 
            border: 3px solid #C0C0C0;
            box-shadow: 0 8px 25px rgba(192, 192, 192, 0.3);
        }
        .card-gold { 
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.4), rgba(218, 165, 32, 0.4)); 
            border: 3px solid #FFD700;
            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
        }
        .card-diamond { 
            background: linear-gradient(135deg, rgba(185, 242, 255, 0.4), rgba(0, 191, 255, 0.4)); 
            border: 3px solid #00BFFF;
            box-shadow: 0 8px 25px rgba(0, 191, 255, 0.3);
        }
        
        .card-logo {
            position: absolute; top: 15px; left: 15px; 
            width: 40px; height: 40px;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border-radius: 50%; display: flex;
            align-items: center; justify-content: center;
            color: white; font-weight: bold; font-size: 1.2rem;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
        }
        
        .nft-badge {
            position: absolute; top: 15px; right: 15px;
            background: rgba(0, 0, 0, 0.8); color: #00d4ff;
            padding: 5px 10px; border-radius: 15px;
            font-size: 0.7rem; font-weight: bold;
        }
        
        .card-title { font-size: 1.8rem; font-weight: bold; margin-bottom: 15px; }
        .card-cost { font-size: 2rem; color: #00d4ff; font-weight: bold; margin: 15px 0; }
        .card-prizes { font-size: 1.1rem; color: #B0B0B0; margin: 10px 0; }
        
        .scratch-area {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9); z-index: 1000; align-items: center; justify-content: center;
        }
        
        .scratch-card {
            background: linear-gradient(145deg, #f0f0f0, #ffffff);
            border-radius: 20px; padding: 40px; text-align: center;
            max-width: 500px; width: 90%; position: relative; color: #333;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border: 3px solid #ddd;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 153, 204, 0.1) 0%, transparent 50%);
        }
        
        .card-watermark {
            position: absolute; top: 20px; right: 20px; opacity: 0.1;
            font-size: 4rem; color: #00d4ff; font-weight: bold;
            transform: rotate(-15deg); pointer-events: none;
        }
        
        .scratch-grid {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;
            margin: 30px 0; max-width: 300px; margin-left: auto; margin-right: auto;
        }
        
        .scratch-symbol {
            width: 80px; height: 80px; 
            background: linear-gradient(145deg, #e6e6e6, #ffffff);
            border-radius: 10px; border: 2px solid #ccc;
            display: flex; align-items: center; justify-content: center;
            font-size: 2rem; cursor: pointer; position: relative; overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .scratch-symbol img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .scratch-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(45deg, #c0c0c0, #e8e8e8, #a8a8a8);
            border-radius: 8px; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            color: #666; font-weight: bold; user-select: none;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            background-image: 
                repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,255,255,0.3) 2px, rgba(255,255,255,0.3) 4px),
                repeating-linear-gradient(-45deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px),
                radial-gradient(circle at 50% 50%, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
        }
        
        .scratch-overlay::before {
            content: 'HYPE'; position: absolute; top: 2px; left: 2px;
            font-size: 0.6rem; opacity: 0.3; color: #00d4ff;
        }
        
        .scratch-overlay:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .scratching {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52) !important;
            animation: scratch-reveal 0.3s ease-out;
        }
        
        @keyframes scratch-reveal {
            0% { opacity: 1; transform: scale(1); }
            100% { opacity: 0; transform: scale(0.8) rotate(10deg); }
        }
        
        @keyframes sparkle {
            0%, 100% { transform: scale(1) rotate(0deg); }
            50% { transform: scale(1.2) rotate(180deg); }
        }
        
        .scratched { 
            opacity: 0; 
            pointer-events: none; 
            transform: scale(0.8) rotate(10deg);
            transition: all 0.5s ease;
        }
        
        .result-message {
            font-size: 1.5rem; font-weight: bold; margin: 20px 0;
            min-height: 60px; display: flex; align-items: center; justify-content: center;
        }
        .win-message { color: #28a745; }
        .lose-message { color: #dc3545; }
        
        .close-btn {
            background: #007bff; color: white; border: none; padding: 15px 30px;
            border-radius: 10px; font-size: 1.1rem; cursor: pointer; margin-top: 20px;
        }
        
        .stats-section {
            background: rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px;
            margin-bottom: 30px;
        }
        
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px;
            text-align: center;
        }
        .stat-value { font-size: 1.8rem; font-weight: bold; color: #00d4ff; }
        .stat-label { color: #B0B0B0; margin-top: 5px; }
        
        .recent-wins {
            background: rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px;
        }
        .win-item {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(255, 255, 255, 0.1); padding: 15px; margin: 10px 0;
            border-radius: 10px; border-left: 4px solid #00d4ff;
        }
        .win-details .win-player { color: #1da1f2; font-weight: bold; }
        .win-details .win-type { color: #B0B0B0; font-size: 0.9rem; }
        .win-prize { color: #28a745; font-weight: bold; font-size: 1.1rem; }
        
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .logout-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <div class="hype-logo"></div>
                HyperFlow Scratch Cards
                <div class="hype-logo"></div>
            </h1>
            <p style="font-size: 1.2rem; color: #B0B0B0;">Connect with X to play HYPE token scratch cards</p>
        </div>
        
        <div class="auth-section" id="auth-section">
            <h2 style="margin-bottom: 20px; position: relative; z-index: 10;">Connect Your X Account</h2>
            <p style="color: #B0B0B0; margin-bottom: 30px; position: relative; z-index: 10;">Sign in with your X (Twitter) account to start playing scratch cards and winning HYPE tokens!</p>
            <div style="position: relative; z-index: 10; margin: 20px 0;">
                <div style="display: flex; justify-content: center; align-items: center; gap: 15px; color: #666; margin-bottom: 20px;">
                    <div style="width: 60px; height: 1px; background: rgba(0, 212, 255, 0.3);"></div>
                    <span style="font-size: 0.9rem;">Secure Authentication</span>
                    <div style="width: 60px; height: 1px; background: rgba(0, 212, 255, 0.3);"></div>
                </div>
            </div>
            
            <button class="connect-x-btn" onclick="connectWithX()">
                <svg class="twitter-icon" viewBox="0 0 24 24">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
                Connect with X
            </button>
        </div>
        
        <div class="user-profile" id="user-profile">
            <img class="user-avatar" id="user-avatar" src="" alt="User Avatar">
            <div class="user-info">
                <h3 id="user-name"></h3>
                <p id="user-handle"></p>
            </div>
            <button class="logout-btn" onclick="logout()">Logout</button>
        </div>
        
        <div class="game-section" id="game-section">
            <div class="stats-section">
                <h3 style="margin-bottom: 20px;">📊 Live Statistics</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="total-sold">0</div>
                        <div class="stat-label">Cards Sold</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="total-prizes">0 HYPE</div>
                        <div class="stat-label">Total Prizes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="biggest-win">0 HYPE</div>
                        <div class="stat-label">Biggest Win</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="active-players">0</div>
                        <div class="stat-label">Active Players</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="prize-pool">0 HYPE</div>
                        <div class="stat-label">Prize Pool</div>
                    </div>
                </div>
            </div>
            
            <h2 style="text-align: center; margin-bottom: 30px;">🎯 Choose Your Scratch Card</h2>
            <div class="cards-grid">
                <div class="card-type card-bronze" onclick="buyCard('bronze')">
                    <div class="card-logo">H</div>
                    <div class="nft-badge">NFT COLLECTION</div>
                    <div class="card-title">🥉 Bronze HYPE Card</div>
                    <div class="card-cost">1 HYPE</div>
                    <div class="card-prizes">Win: 0.5 - 3 HYPE</div>
                    <div style="position: absolute; bottom: 10px; right: 10px; opacity: 0.3; font-size: 0.8rem;">HYPEREVM-001</div>
                </div>
                
                <div class="card-type card-silver" onclick="buyCard('silver')">
                    <div class="card-logo">H</div>
                    <div class="nft-badge">NFT COLLECTION</div>
                    <div class="card-title">🥈 Silver HYPE Card</div>
                    <div class="card-cost">5 HYPE</div>
                    <div class="card-prizes">Win: 2 - 15 HYPE</div>
                    <div style="position: absolute; bottom: 10px; right: 10px; opacity: 0.3; font-size: 0.8rem;">HYPEREVM-002</div>
                </div>
                
                <div class="card-type card-gold" onclick="buyCard('gold')">
                    <div class="card-logo">H</div>
                    <div class="nft-badge">NFT COLLECTION</div>
                    <div class="card-title">🥇 Gold HYPE Card</div>
                    <div class="card-cost">20 HYPE</div>
                    <div class="card-prizes">Win: 10 - 80 HYPE</div>
                    <div style="position: absolute; bottom: 10px; right: 10px; opacity: 0.3; font-size: 0.8rem;">HYPEREVM-003</div>
                </div>
                
                <div class="card-type card-diamond" onclick="buyCard('diamond')">
                    <div class="card-logo">H</div>
                    <div class="nft-badge">NFT COLLECTION</div>
                    <div class="card-title">💎 Diamond HYPE Card</div>
                    <div class="card-cost">100 HYPE</div>
                    <div class="card-prizes">Win: 50 - 500 HYPE</div>
                    <div style="position: absolute; bottom: 10px; right: 10px; opacity: 0.3; font-size: 0.8rem;">HYPEREVM-004</div>
                </div>
            </div>
            
            <div class="recent-wins">
                <h3>🏆 Recent Winners</h3>
                <div id="recent-wins-list">
                    <div style="text-align: center; padding: 20px; color: #B0B0B0;">No recent wins yet</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="scratch-area" id="scratch-area">
        <div class="scratch-card">
            <div class="card-watermark">HYPE</div>
            <div style="background: linear-gradient(45deg, #00d4ff, #0099cc); color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h3 id="card-title">🎫 Scratch Your Card! 🎫</h3>
                <p>Drag to scratch - match 3 HYPE logos to win!</p>
            </div>
            
            <div class="scratch-grid" id="scratch-grid">
                <!-- Symbols will be generated here -->
            </div>
            
            <div class="result-message" id="result-message"></div>
            <button class="close-btn" onclick="closeScratchCard()">Close</button>
            <div style="position: absolute; bottom: 10px; right: 15px; opacity: 0.3; font-size: 0.8rem; color: #666;">
                NFT-<span id="card-serial"></span> • HyperFlow
            </div>
        </div>
    </div>
    
    <script>
        console.log('🎫 HyperFlow Scratch Cards - X Connected Version Loaded');
        
        let currentCard = null;
        let scratchedCount = 0;
        let cardResult = null;
        let isScratching = false;
        let scratchedSymbols = new Set();
        let isLoggedIn = false;
        let currentUser = null;
        
        // Mock X authentication - in production this would use real X OAuth
        function connectWithX() {
            // Simulate X OAuth process
            const mockUsers = [
                {name: 'HYPETrader', handle: '@hypetrader123', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=H'},
                {name: 'CryptoWhale', handle: '@cryptowhale', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=C'},
                {name: 'DeFiMaster', handle: '@defimaster', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=D'},
                {name: 'NFTCollector', handle: '@nftcollector', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=N'},
            ];
            
            // Simulate OAuth flow
            setTimeout(() => {
                currentUser = mockUsers[Math.floor(Math.random() * mockUsers.length)];
                
                document.getElementById('user-name').textContent = currentUser.name;
                document.getElementById('user-handle').textContent = currentUser.handle;
                document.getElementById('user-avatar').src = currentUser.avatar;
                
                document.getElementById('auth-section').style.display = 'none';
                document.getElementById('user-profile').style.display = 'flex';
                document.getElementById('game-section').classList.add('active');
                
                isLoggedIn = true;
                
                // Start updating stats
                updateStats();
                setInterval(updateStats, 10000);
                
            }, 1500);
        }
        
        function logout() {
            isLoggedIn = false;
            currentUser = null;
            
            document.getElementById('auth-section').style.display = 'block';
            document.getElementById('user-profile').style.display = 'none';
            document.getElementById('game-section').classList.remove('active');
        }
        
        function buyCard(type) {
            if (!isLoggedIn) {
                alert('Please connect your X account first!');
                return;
            }
            
            const costs = {bronze: 1, silver: 5, gold: 20, diamond: 100};
            const cost = costs[type];
            
            if (confirm(`Buy ${type} card for ${cost} HYPE?\\n\\nNote: This is a demo - no real HYPE tokens will be deducted.`)) {
                scratchCard(type);
            }
        }
        
        async function scratchCard(type) {
            try {
                const response = await fetch(`/api/scratch-card?type=${type}`);
                cardResult = await response.json();
                
                currentCard = type;
                scratchedCount = 0;
                scratchedSymbols.clear();
                
                const cardTitles = {
                    bronze: '🥉 Bronze Scratch Card',
                    silver: '🥈 Silver Scratch Card', 
                    gold: '🥇 Gold Scratch Card',
                    diamond: '💎 Diamond Scratch Card'
                };
                
                const serials = {bronze: 'HYPEREVM-001', silver: 'HYPEREVM-002', gold: 'HYPEREVM-003', diamond: 'HYPEREVM-004'};
                
                document.getElementById('card-title').textContent = cardTitles[type];
                document.getElementById('card-serial').textContent = serials[type];
                
                generateScratchGrid(cardResult.symbols);
                document.getElementById('scratch-area').style.display = 'flex';
                document.getElementById('result-message').textContent = '';
                
            } catch (error) {
                console.error('Error buying card:', error);
                alert('Error buying card. Please try again.');
            }
        }
        
        function generateScratchGrid(symbols) {
            const grid = document.getElementById('scratch-grid');
            grid.innerHTML = '';
            
            symbols.forEach((symbol, index) => {
                const symbolDiv = document.createElement('div');
                symbolDiv.className = 'scratch-symbol';
                symbolDiv.innerHTML = `
                    <img src="${symbol}" alt="Token Logo" onerror="this.style.display='none'; this.nextSibling.style.display='block';">
                    <span style="display: none;">🪙</span>
                    <div class="scratch-overlay" 
                         onmousedown="startScratch(this, ${index})"
                         onmousemove="continueScratch(event, this)"
                         onmouseup="endScratch(this)"
                         onmouseleave="endScratch(this)"
                         ontouchstart="startScratch(this, ${index})"
                         ontouchmove="continueScratch(event, this)"
                         ontouchend="endScratch(this)">
                        SCRATCH
                    </div>
                `;
                grid.appendChild(symbolDiv);
            });
        }
        
        function startScratch(overlay, index) {
            if (scratchedSymbols.has(index)) return;
            isScratching = true;
            overlay.style.cursor = 'grabbing';
        }
        
        function continueScratch(event, overlay) {
            if (!isScratching) return;
            
            // Get overlay bounds and mouse position
            const rect = overlay.getBoundingClientRect();
            const x = (event.clientX || event.touches[0].clientX) - rect.left;
            const y = (event.clientY || event.touches[0].clientY) - rect.top;
            
            // Only scratch if mouse is in center area
            const scratchRadius = 20;
            if (x > scratchRadius && x < rect.width - scratchRadius && 
                y > scratchRadius && y < rect.height - scratchRadius) {
                const index = Array.from(overlay.parentElement.parentElement.children)
                    .indexOf(overlay.parentElement);
                scratchSymbol(overlay, index);
            }
        }
        
        function endScratch(overlay) {
            isScratching = false;
            overlay.style.cursor = 'pointer';
        }
        
        function scratchSymbol(overlay, index) {
            if (scratchedSymbols.has(index)) return;
            
            scratchedSymbols.add(index);
            overlay.classList.add('scratching');
            overlay.textContent = 'REVEALED!';
            
            setTimeout(() => {
                overlay.classList.add('scratched');
                scratchedCount++;
                
                // Add sparkle effect to revealed symbol
                const symbol = overlay.parentElement.querySelector('img, span');
                symbol.style.animation = 'sparkle 0.6s ease-in-out';
                
                if (scratchedCount >= 3) {
                    setTimeout(revealResult, 500);
                }
            }, 300);
        }
        
        function revealResult() {
            // Reveal all symbols
            document.querySelectorAll('.scratch-overlay').forEach(overlay => {
                overlay.classList.add('scratched');
            });
            
            const resultMsg = document.getElementById('result-message');
            
            if (cardResult.winner) {
                let message = `🎉 YOU WIN ${cardResult.prize.toLocaleString()} HYPE! 🎉`;
                if (cardResult.bonus_multiplier === 10) {
                    message = `🚀 JACKPOT! ${cardResult.prize.toLocaleString()} HYPE! 🚀`;
                    resultMsg.style.animation = 'sparkle 2s infinite';
                } else if (cardResult.bonus_multiplier > 1) {
                    message += ` (${cardResult.bonus_multiplier}x BONUS!)`;
                }
                resultMsg.textContent = message;
                resultMsg.className = 'result-message win-message';
                
                // Show celebration animation for big wins
                if (cardResult.prize >= 10) {
                    document.body.style.background = 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%), radial-gradient(circle, rgba(0,212,255,0.1) 0%, transparent 70%)';
                    setTimeout(() => {
                        document.body.style.background = 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)';
                    }, 3000);
                }
            } else {
                resultMsg.textContent = '😔 Better luck next time!';
                resultMsg.className = 'result-message lose-message';
            }
            
            // Update stats after revealing
            setTimeout(updateStats, 1000);
        }
        
        function closeScratchCard() {
            document.getElementById('scratch-area').style.display = 'none';
            currentCard = null;
            cardResult = null;
            scratchedCount = 0;
            scratchedSymbols.clear();
            isScratching = false;
        }
        
        async function updateStats() {
            try {
                const response = await fetch('/api/scratch-stats');
                const data = await response.json();
                
                document.getElementById('total-sold').textContent = data.total_cards_sold.toLocaleString();
                document.getElementById('total-prizes').textContent = data.total_prizes_won.toLocaleString() + ' HYPE';
                document.getElementById('biggest-win').textContent = data.biggest_win.toLocaleString() + ' HYPE';
                document.getElementById('active-players').textContent = data.active_players.toLocaleString();
                
                // Update prize pool display
                if (data.prize_pool) {
                    document.getElementById('prize-pool').textContent = data.prize_pool.toLocaleString() + ' HYPE';
                }
                
                // Update recent wins
                const winsList = document.getElementById('recent-wins-list');
                if (data.recent_wins.length > 0) {
                    winsList.innerHTML = data.recent_wins.map(win => `
                        <div class="win-item">
                            <div class="win-details">
                                <div class="win-player">${win.player}</div>
                                <div class="win-type">${win.type} card • ${win.time}</div>
                            </div>
                            <div class="win-prize">+${win.prize.toLocaleString()} HYPE</div>
                        </div>
                    `).join('');
                } else {
                    winsList.innerHTML = '<div style="text-align: center; padding: 20px; color: #B0B0B0;">No recent wins yet</div>';
                }
                
            } catch (error) {
                console.error('Error updating stats:', error);
            }
        }
    </script>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path.startswith("/api/scratch-card"):
            # Parse query parameters
            query_start = self.path.find('?')
            if query_start != -1:
                query_string = self.path[query_start + 1:]
                params = {}
                for param in query_string.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[key] = value
                
                card_type = params.get('type', 'bronze')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                result = scratch_game.generate_card_result(card_type)
                self.wfile.write(json.dumps(result).encode('utf-8'))
            else:
                self.send_error(400, "Missing card type parameter")
        
        elif self.path == "/api/scratch-stats":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = {
                **scratch_game.stats,
                'recent_wins': scratch_game.recent_wins,
                'prize_pool': scratch_game.prize_pool
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
        
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    print("🎫 HyperFlow Scratch Cards - X Connected Version")
    print("=" * 60)
    print("💎 Features:")
    print("  - X (Twitter) Social Authentication")
    print("  - 4 Card Types: Bronze, Silver, Gold, Diamond") 
    print("  - Real HYPE/ETH/BTC Crypto Logos")
    print("  - Instant Win with Animated Reveals")
    print("  - 30% Win Rate (Hidden)")
    print("  - Affordable HYPE Pricing (1-100 HYPE)")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), ScratchCardHandler) as httpd:
            print(f"🌐 HyperFlow Scratch Cards (X Version): http://localhost:{PORT}")
            print("🎫 Connect with X to start playing...")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Port already in use
            print(f"Port {PORT} in use, trying alternative...")
            PORT = 7002
            with socketserver.TCPServer(("", PORT), ScratchCardHandler) as httpd:
                print(f"🌐 HyperFlow Scratch Cards (X Version): http://localhost:{PORT}")
                print("🎫 Connect with X to start playing...")
                httpd.serve_forever()
        else:
            raise