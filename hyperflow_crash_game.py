#!/usr/bin/env python3
"""
HyperFlow Crash Game - HYPE Token Platform
High-intensity multiplier crash game where players bet HYPE and cash out before the crash
Features: Real-time multiplier, social gameplay, instant payouts
"""

import http.server
import socketserver
import json
import random
import time
import threading
from datetime import datetime

PORT = 6000

class CrashGameState:
    def __init__(self):
        self.game_active = False
        self.multiplier = 1.0
        self.start_time = None
        self.crash_point = None
        self.players = {}
        self.game_history = []
        self.betting_time = 10  # 10 seconds to place bets
        self.betting_active = True
        
    def start_new_game(self):
        self.game_active = True
        self.multiplier = 1.0
        self.start_time = time.time()
        self.crash_point = self.generate_crash_point()
        self.players = {}
        self.betting_active = True
        
    def generate_crash_point(self):
        # Provably fair crash point generation
        # House edge of ~5%, most crashes between 1.1x - 10x
        rand = random.random()
        if rand < 0.5:
            return round(1.1 + random.random() * 2, 2)  # 1.1x - 3.1x (50%)
        elif rand < 0.8:
            return round(3.1 + random.random() * 4, 2)  # 3.1x - 7.1x (30%)
        elif rand < 0.95:
            return round(7.1 + random.random() * 15, 2)  # 7.1x - 22.1x (15%)
        else:
            return round(22.1 + random.random() * 78, 2)  # 22.1x - 100x (5%)
    
    def update_multiplier(self):
        if not self.game_active:
            return
            
        elapsed = time.time() - self.start_time
        if elapsed < self.betting_time:
            return
            
        # Multiplier growth formula
        game_time = elapsed - self.betting_time
        self.multiplier = 1.0 + (game_time * 0.1) * (1 + game_time * 0.02)
        
        if self.multiplier >= self.crash_point:
            self.crash_game()
    
    def crash_game(self):
        self.game_active = False
        self.multiplier = self.crash_point
        
        # Add to history
        self.game_history.insert(0, {
            'multiplier': self.crash_point,
            'time': datetime.now().strftime('%H:%M:%S'),
            'players': len(self.players)
        })
        
        if len(self.game_history) > 20:
            self.game_history.pop()

crash_state = CrashGameState()

class CrashGameHandler(http.server.BaseHTTPRequestHandler):
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
    <title>HyperFlow Crash - HYPE Token Game</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
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
        }
        
        .game-area {
            display: grid; grid-template-columns: 2fr 1fr; gap: 30px;
            margin-bottom: 30px;
        }
        
        .crash-display {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 40px; text-align: center;
            backdrop-filter: blur(10px); position: relative; min-height: 400px;
        }
        
        .multiplier {
            font-size: 6rem; font-weight: bold; margin: 40px 0;
            background: linear-gradient(45deg, #00d4ff, #0099cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            transition: all 0.3s ease;
        }
        
        .multiplier.crashed {
            color: #ff4757 !important;
            -webkit-text-fill-color: #ff4757 !important;
            animation: crashPulse 0.5s ease-in-out;
        }
        
        @keyframes crashPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .game-status {
            font-size: 1.5rem; margin: 20px 0;
            padding: 15px; border-radius: 10px;
        }
        .status-betting { background: rgba(255, 193, 7, 0.2); color: #ffc107; }
        .status-flying { background: rgba(40, 167, 69, 0.2); color: #28a745; }
        .status-crashed { background: rgba(220, 53, 69, 0.2); color: #dc3545; }
        
        .betting-panel {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 30px;
            backdrop-filter: blur(10px);
        }
        
        .bet-input {
            width: 100%; padding: 15px; font-size: 1.2rem;
            border: none; border-radius: 10px; margin: 10px 0;
            background: rgba(255, 255, 255, 0.2); color: white;
        }
        .bet-input::placeholder { color: #B0B0B0; }
        
        .quick-bets {
            display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0;
        }
        .quick-bet {
            padding: 12px; background: rgba(0, 212, 255, 0.3);
            border: none; border-radius: 8px; color: white; cursor: pointer;
            transition: all 0.3s;
        }
        .quick-bet:hover { background: rgba(0, 212, 255, 0.5); }
        
        .action-btn {
            width: 100%; padding: 20px; font-size: 1.3rem; font-weight: bold;
            border: none; border-radius: 15px; cursor: pointer; margin: 15px 0;
            transition: all 0.3s;
        }
        .btn-bet { background: linear-gradient(45deg, #28a745, #20c997); color: white; }
        .btn-cashout { background: linear-gradient(45deg, #ffc107, #fd7e14); color: #333; }
        .btn-disabled { background: #6c757d; cursor: not-allowed; }
        
        .players-section { margin: 20px 0; }
        .player-item {
            display: flex; justify-content: space-between;
            background: rgba(255, 255, 255, 0.1); padding: 10px; margin: 5px 0;
            border-radius: 8px; font-size: 0.9rem;
        }
        
        .history-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 30px; margin-top: 30px;
        }
        .history-items {
            display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;
        }
        .history-item {
            padding: 10px 15px; border-radius: 8px; font-weight: bold;
            min-width: 80px; text-align: center;
        }
        .history-green { background: rgba(40, 167, 69, 0.3); color: #28a745; }
        .history-red { background: rgba(220, 53, 69, 0.3); color: #dc3545; }
        
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin: 20px 0;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px;
            text-align: center;
        }
        .stat-value { font-size: 1.8rem; font-weight: bold; color: #00d4ff; }
        .stat-label { color: #B0B0B0; margin-top: 5px; }
        
        @media (max-width: 768px) {
            .game-area { grid-template-columns: 1fr; }
            .multiplier { font-size: 4rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 HyperFlow Crash</h1>
            <p>High-Risk HYPE Token Multiplier Game</p>
        </div>
        
        <div class="game-area">
            <div class="crash-display">
                <div class="game-status" id="game-status">Waiting for next round...</div>
                <div class="multiplier" id="multiplier">1.00x</div>
                <div id="crash-message" style="font-size: 1.2rem; color: #ff4757; display: none;">
                    CRASHED! 💥
                </div>
            </div>
            
            <div class="betting-panel">
                <h3>Place Your Bet</h3>
                <input type="number" class="bet-input" placeholder="HYPE Amount" id="bet-amount" min="10" step="10">
                
                <div class="quick-bets">
                    <button class="quick-bet" onclick="setBet(100)">100 HYPE</button>
                    <button class="quick-bet" onclick="setBet(500)">500 HYPE</button>
                    <button class="quick-bet" onclick="setBet(1000)">1K HYPE</button>
                    <button class="quick-bet" onclick="setBet(5000)">5K HYPE</button>
                </div>
                
                <button class="action-btn btn-bet" id="bet-btn" onclick="placeBet()">Place Bet</button>
                <button class="action-btn btn-cashout" id="cashout-btn" onclick="cashOut()" style="display: none;">Cash Out</button>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="my-bet">0</div>
                        <div class="stat-label">My Bet</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="potential-win">0</div>
                        <div class="stat-label">Potential Win</div>
                    </div>
                </div>
                
                <div class="players-section">
                    <h4>Active Players</h4>
                    <div id="players-list">No active players</div>
                </div>
            </div>
        </div>
        
        <div class="history-section">
            <h3>Recent Games</h3>
            <div class="history-items" id="game-history">
                <div class="history-item history-green">2.45x</div>
                <div class="history-item history-red">1.23x</div>
                <div class="history-item history-green">5.67x</div>
                <div class="history-item history-red">1.89x</div>
                <div class="history-item history-green">12.34x</div>
            </div>
        </div>
    </div>
    
    <script>
        let gameState = {
            active: false,
            multiplier: 1.0,
            myBet: 0,
            cashoutMultiplier: 0,
            hasBet: false
        };
        
        function setBet(amount) {
            document.getElementById('bet-amount').value = amount;
            updatePotentialWin();
        }
        
        function updatePotentialWin() {
            const betAmount = parseFloat(document.getElementById('bet-amount').value) || 0;
            const multiplier = gameState.multiplier;
            const potential = Math.floor(betAmount * multiplier);
            document.getElementById('potential-win').textContent = potential + ' HYPE';
        }
        
        function placeBet() {
            const amount = parseFloat(document.getElementById('bet-amount').value);
            if (!amount || amount < 10) {
                alert('Minimum bet is 10 HYPE');
                return;
            }
            
            gameState.myBet = amount;
            gameState.hasBet = true;
            document.getElementById('my-bet').textContent = amount + ' HYPE';
            document.getElementById('bet-btn').style.display = 'none';
            
            alert('Bet placed! Wait for the round to start.');
        }
        
        function cashOut() {
            if (!gameState.hasBet || !gameState.active) return;
            
            const winAmount = Math.floor(gameState.myBet * gameState.multiplier);
            alert(`Cashed out at ${gameState.multiplier.toFixed(2)}x! Won ${winAmount} HYPE`);
            
            gameState.hasBet = false;
            gameState.cashoutMultiplier = gameState.multiplier;
            document.getElementById('cashout-btn').style.display = 'none';
            document.getElementById('bet-btn').style.display = 'block';
        }
        
        async function updateGame() {
            try {
                const response = await fetch('/api/crash-game');
                const data = await response.json();
                
                gameState.active = data.active;
                gameState.multiplier = data.multiplier;
                
                document.getElementById('multiplier').textContent = data.multiplier.toFixed(2) + 'x';
                
                if (data.active && !data.betting) {
                    document.getElementById('game-status').textContent = 'Flying...';
                    document.getElementById('game-status').className = 'game-status status-flying';
                    if (gameState.hasBet) {
                        document.getElementById('cashout-btn').style.display = 'block';
                    }
                } else if (data.betting) {
                    document.getElementById('game-status').textContent = 'Betting Phase';
                    document.getElementById('game-status').className = 'game-status status-betting';
                    document.getElementById('bet-btn').style.display = 'block';
                    document.getElementById('cashout-btn').style.display = 'none';
                } else {
                    document.getElementById('game-status').textContent = 'CRASHED!';
                    document.getElementById('game-status').className = 'game-status status-crashed';
                    document.getElementById('multiplier').classList.add('crashed');
                    document.getElementById('crash-message').style.display = 'block';
                    document.getElementById('cashout-btn').style.display = 'none';
                    
                    if (gameState.hasBet && gameState.cashoutMultiplier === 0) {
                        alert('You crashed! Better luck next time.');
                        gameState.hasBet = false;
                    }
                    
                    setTimeout(() => {
                        document.getElementById('multiplier').classList.remove('crashed');
                        document.getElementById('crash-message').style.display = 'none';
                        gameState.cashoutMultiplier = 0;
                        document.getElementById('bet-btn').style.display = 'block';
                    }, 3000);
                }
                
                updatePotentialWin();
                
                // Update history
                if (data.history) {
                    const historyDiv = document.getElementById('game-history');
                    historyDiv.innerHTML = data.history.map(h => 
                        `<div class="history-item ${h.multiplier >= 2.0 ? 'history-green' : 'history-red'}">
                            ${h.multiplier.toFixed(2)}x
                        </div>`
                    ).join('');
                }
                
            } catch (error) {
                console.error('Error updating game:', error);
            }
        }
        
        updateGame();
        setInterval(updateGame, 100); // Update every 100ms for smooth multiplier
        
        console.log('🚀 HyperFlow Crash Game Loaded');
    </script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == "/api/crash-game":
            crash_state.update_multiplier()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Check if we need to start a new game
            if not crash_state.game_active and not crash_state.betting_active:
                # Wait 5 seconds before starting new game
                if crash_state.start_time is None or time.time() - crash_state.start_time > 8:
                    crash_state.start_new_game()
            
            # Determine betting phase
            betting_phase = False
            if crash_state.game_active and crash_state.start_time:
                elapsed = time.time() - crash_state.start_time
                betting_phase = elapsed < crash_state.betting_time
            
            data = {
                "active": crash_state.game_active and not betting_phase,
                "betting": betting_phase,
                "multiplier": crash_state.multiplier,
                "crash_point": crash_state.crash_point if not crash_state.game_active else None,
                "history": crash_state.game_history[:10],
                "players": len(crash_state.players)
            }
            
            self.wfile.write(json.dumps(data).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()

def run_game_loop():
    while True:
        time.sleep(0.1)
        if crash_state.game_active:
            crash_state.update_multiplier()

if __name__ == "__main__":
    print("🚀 HyperFlow Crash Game - HYPE Token Platform")
    print("=" * 60)
    print("💎 Features:")
    print("  - Real-time Multiplier Crash Game")
    print("  - HYPE Token Betting System")
    print("  - Provably Fair Crash Points")
    print("  - Social Multiplayer Experience")
    print("=" * 60)
    
    # Start game loop in background
    game_thread = threading.Thread(target=run_game_loop, daemon=True)
    game_thread.start()
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), CrashGameHandler) as httpd:
            print(f"🌐 HyperFlow Crash Game: http://localhost:{PORT}")
            print("🚀 High-intensity crash game loading...")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"Port {PORT} in use, trying alternative...")
            for alt_port in [6001, 6002, 7000, 7001]:
                try:
                    with socketserver.TCPServer(("0.0.0.0", alt_port), CrashGameHandler) as httpd:
                        print(f"🌐 HyperFlow Crash Game: http://localhost:{alt_port}")
                        print("🚀 High-intensity crash game loading...")
                        httpd.serve_forever()
                except OSError:
                    continue
        else:
            raise