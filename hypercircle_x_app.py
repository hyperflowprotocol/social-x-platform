#!/usr/bin/env python3
"""
HyperCircle X - Professional Circular Community Platform
X (Twitter) Authentication with Modern UI Design
Inspired by hypercircle.app interface patterns
"""

import http.server
import socketserver
import json
import random
from datetime import datetime

PORT = 5000

class HyperCircleHandler(http.server.BaseHTTPRequestHandler):
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
    <title>HyperCircle - Connect & Build</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary-blue: #1da1f2;
            --primary-dark: #0f1419;
            --primary-gray: #536471;
            --accent-cyan: #00d4ff;
            --accent-purple: #7856ff;
            --surface-dark: #16181c;
            --surface-light: #1c1f26;
            --border-color: #2f3336;
            --text-primary: #ffffff;
            --text-secondary: #8b98a5;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: 
                radial-gradient(circle at 10% 20%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(120, 86, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(29, 161, 242, 0.05) 0%, transparent 40%),
                linear-gradient(135deg, var(--primary-dark) 0%, var(--surface-dark) 100%);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .app-container {
            display: flex;
            min-height: 100vh;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Sidebar Navigation */
        .sidebar {
            width: 275px;
            background: rgba(22, 24, 28, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-color);
            padding: 20px 0;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }
        
        .logo-section {
            padding: 0 20px 30px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .circle-logo {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--primary-blue));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.5rem;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
            position: relative;
        }
        
        .circle-logo::before {
            content: '';
            position: absolute;
            width: 60px;
            height: 60px;
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 50%;
            animation: rotate-ring 8s linear infinite;
        }
        
        @keyframes rotate-ring {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .logo-text {
            font-size: 1.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan), var(--text-primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-menu {
            padding: 0 10px;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            margin-bottom: 5px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            gap: 15px;
            position: relative;
            overflow: hidden;
        }
        
        .nav-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 0;
            height: 100%;
            background: linear-gradient(90deg, rgba(0, 212, 255, 0.1), transparent);
            transition: width 0.3s ease;
        }
        
        .nav-item:hover {
            background: rgba(29, 161, 242, 0.1);
            transform: translateX(5px);
        }
        
        .nav-item:hover::before {
            width: 100%;
        }
        
        .nav-item.active {
            background: rgba(0, 212, 255, 0.15);
            color: var(--accent-cyan);
        }
        
        .nav-icon {
            width: 24px;
            height: 24px;
            opacity: 0.8;
        }
        
        .auth-section {
            position: absolute;
            bottom: 20px;
            left: 20px;
            right: 20px;
        }
        
        .connect-x-btn {
            width: 100%;
            background: linear-gradient(135deg, var(--primary-blue), #0d8bd9);
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            position: relative;
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
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(29, 161, 242, 0.4);
        }
        
        .connect-x-btn:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .user-profile {
            display: none;
            align-items: center;
            gap: 12px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 50px;
            border: 1px solid var(--border-color);
        }
        
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid var(--accent-cyan);
        }
        
        .user-info h4 { margin: 0; color: var(--accent-cyan); }
        .user-info p { margin: 0; font-size: 0.85rem; color: var(--text-secondary); }
        
        /* Main Content Area */
        .main-content {
            flex: 1;
            margin-left: 275px;
            min-height: 100vh;
        }
        
        .content-header {
            background: rgba(22, 24, 28, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-color);
            padding: 20px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .header-subtitle {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }
        
        .content-body {
            padding: 30px;
        }
        
        .welcome-section {
            text-align: center;
            padding: 60px 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .welcome-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple), var(--primary-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }
        
        .welcome-subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 40px;
            line-height: 1.5;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 50px;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.05) 0%, transparent 70%);
            transition: all 0.4s ease;
            transform: rotate(0deg);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-cyan);
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.1);
        }
        
        .feature-card:hover::before {
            transform: rotate(180deg);
        }
        
        .feature-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--primary-blue));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 1.5rem;
            position: relative;
            z-index: 2;
        }
        
        .feature-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
            position: relative;
            z-index: 2;
        }
        
        .feature-description {
            color: var(--text-secondary);
            line-height: 1.6;
            position: relative;
            z-index: 2;
        }
        
        .dashboard-grid {
            display: none;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .dashboard-grid.active {
            display: grid;
        }
        
        .dashboard-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 25px;
            transition: all 0.3s ease;
        }
        
        .dashboard-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .card-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--primary-blue));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .card-title {
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .card-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 10px;
        }
        
        .card-subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            cursor: pointer;
            margin-left: auto;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            
            .sidebar.open {
                transform: translateX(0);
            }
            
            .main-content {
                margin-left: 0;
            }
            
            .welcome-title {
                font-size: 2.2rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar Navigation -->
        <div class="sidebar">
            <div class="logo-section">
                <div class="circle-logo">○</div>
                <div class="logo-text">HyperCircle</div>
            </div>
            
            <nav class="nav-menu">
                <div class="nav-item active" onclick="showSection('home')">
                    <div class="nav-icon">🏠</div>
                    <span>Home</span>
                </div>
                <div class="nav-item" onclick="showSection('explore')">
                    <div class="nav-icon">🔍</div>
                    <span>Explore</span>
                </div>
                <div class="nav-item" onclick="showSection('communities')">
                    <div class="nav-icon">👥</div>
                    <span>Communities</span>
                </div>
                <div class="nav-item" onclick="showSection('messages')">
                    <div class="nav-icon">💬</div>
                    <span>Messages</span>
                </div>
                <div class="nav-item" onclick="showSection('notifications')">
                    <div class="nav-icon">🔔</div>
                    <span>Notifications</span>
                </div>
                <div class="nav-item" onclick="showSection('profile')">
                    <div class="nav-icon">👤</div>
                    <span>Profile</span>
                </div>
                <div class="nav-item" onclick="showSection('settings')">
                    <div class="nav-icon">⚙️</div>
                    <span>Settings</span>
                </div>
            </nav>
            
            <div class="auth-section">
                <button class="connect-x-btn" id="connect-btn" onclick="connectWithX()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                    </svg>
                    Connect with X
                </button>
                
                <div class="user-profile" id="user-profile">
                    <img class="user-avatar" id="user-avatar" src="" alt="User Avatar">
                    <div class="user-info">
                        <h4 id="user-name"></h4>
                        <p id="user-handle"></p>
                    </div>
                    <button class="logout-btn" onclick="logout()">Logout</button>
                </div>
            </div>
        </div>
        
        <!-- Main Content -->
        <main class="main-content">
            <header class="content-header">
                <h1 class="header-title" id="header-title">Welcome to HyperCircle</h1>
                <p class="header-subtitle" id="header-subtitle">Connect, create, and build amazing communities</p>
            </header>
            
            <div class="content-body">
                <!-- Welcome Section -->
                <div class="welcome-section" id="welcome-section">
                    <h2 class="welcome-title">The Future of Connection</h2>
                    <p class="welcome-subtitle">
                        Join the most innovative community platform where circles of like-minded individuals 
                        come together to share ideas, build projects, and create lasting connections.
                    </p>
                    
                    <div class="features-grid">
                        <div class="feature-card">
                            <div class="feature-icon">🚀</div>
                            <h3 class="feature-title">Launch Together</h3>
                            <p class="feature-description">
                                Collaborate on projects and bring your ideas to life with community support and expert guidance.
                            </p>
                        </div>
                        
                        <div class="feature-card">
                            <div class="feature-icon">💡</div>
                            <h3 class="feature-title">Share Knowledge</h3>
                            <p class="feature-description">
                                Exchange insights, learn from experts, and grow your skills in a supportive environment.
                            </p>
                        </div>
                        
                        <div class="feature-card">
                            <div class="feature-icon">🌐</div>
                            <h3 class="feature-title">Global Network</h3>
                            <p class="feature-description">
                                Connect with innovators worldwide and expand your network across industries and cultures.
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- Dashboard Section -->
                <div class="dashboard-grid" id="dashboard-section">
                    <div class="dashboard-card">
                        <div class="card-header">
                            <div class="card-icon">📊</div>
                            <h3 class="card-title">Your Communities</h3>
                        </div>
                        <div class="card-value">12</div>
                        <p class="card-subtitle">Active memberships</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <div class="card-header">
                            <div class="card-icon">🎯</div>
                            <h3 class="card-title">Projects</h3>
                        </div>
                        <div class="card-value">5</div>
                        <p class="card-subtitle">In progress</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <div class="card-header">
                            <div class="card-icon">⭐</div>
                            <h3 class="card-title">Contributions</h3>
                        </div>
                        <div class="card-value">89</div>
                        <p class="card-subtitle">This month</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <div class="card-header">
                            <div class="card-icon">🔥</div>
                            <h3 class="card-title">Streak</h3>
                        </div>
                        <div class="card-value">23</div>
                        <p class="card-subtitle">Days active</p>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script>
        console.log('🌐 HyperCircle X - Professional Community Platform Loaded');
        
        let isLoggedIn = false;
        let currentUser = null;
        let currentSection = 'home';
        
        // Mock X authentication
        function connectWithX() {
            const mockUsers = [
                {name: 'Alex Chen', handle: '@alexbuilds', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=A'},
                {name: 'Sarah Kim', handle: '@sarahdesigns', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=S'},
                {name: 'Mike Dev', handle: '@mikedev', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=M'},
                {name: 'Emma Code', handle: '@emmacode', avatar: 'https://via.placeholder.com/40/1da1f2/ffffff?text=E'},
            ];
            
            // Simulate OAuth flow
            document.getElementById('connect-btn').innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="3" opacity="0.6"/>
                </svg>
                Connecting...
            `;
            
            setTimeout(() => {
                currentUser = mockUsers[Math.floor(Math.random() * mockUsers.length)];
                
                document.getElementById('user-name').textContent = currentUser.name;
                document.getElementById('user-handle').textContent = currentUser.handle;
                document.getElementById('user-avatar').src = currentUser.avatar;
                
                document.getElementById('connect-btn').style.display = 'none';
                document.getElementById('user-profile').style.display = 'flex';
                
                document.getElementById('welcome-section').style.display = 'none';
                document.getElementById('dashboard-section').classList.add('active');
                
                document.getElementById('header-title').textContent = `Welcome back, ${currentUser.name}!`;
                document.getElementById('header-subtitle').textContent = 'Your communities are waiting for you';
                
                isLoggedIn = true;
                
            }, 1500);
        }
        
        function logout() {
            isLoggedIn = false;
            currentUser = null;
            
            document.getElementById('connect-btn').style.display = 'flex';
            document.getElementById('user-profile').style.display = 'none';
            
            document.getElementById('welcome-section').style.display = 'block';
            document.getElementById('dashboard-section').classList.remove('active');
            
            document.getElementById('header-title').textContent = 'Welcome to HyperCircle';
            document.getElementById('header-subtitle').textContent = 'Connect, create, and build amazing communities';
            
            document.getElementById('connect-btn').innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
                Connect with X
            `;
        }
        
        function showSection(section) {
            // Update active nav item
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.closest('.nav-item').classList.add('active');
            
            // Update header based on section
            const headers = {
                home: {title: isLoggedIn ? `Welcome back, ${currentUser?.name || 'User'}!` : 'Welcome to HyperCircle', subtitle: 'Your communities are waiting for you'},
                explore: {title: 'Explore Communities', subtitle: 'Discover new circles to join'},
                communities: {title: 'My Communities', subtitle: 'Your active memberships and projects'},
                messages: {title: 'Messages', subtitle: 'Connect with your circle'},
                notifications: {title: 'Notifications', subtitle: 'Stay updated on your communities'},
                profile: {title: 'Profile', subtitle: 'Manage your presence'},
                settings: {title: 'Settings', subtitle: 'Customize your experience'}
            };
            
            if (headers[section]) {
                document.getElementById('header-title').textContent = headers[section].title;
                document.getElementById('header-subtitle').textContent = headers[section].subtitle;
            }
            
            currentSection = section;
        }
    </script>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
        
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    print("🌐 HyperCircle X - Professional Community Platform")
    print("=" * 60)
    print("✨ Features:")
    print("  - X (Twitter) Social Authentication")
    print("  - Modern Circular UI Design")
    print("  - Professional Community Interface")
    print("  - Mobile-First Responsive Layout")
    print("  - Real-time Navigation System")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), HyperCircleHandler) as httpd:
            print(f"🌐 HyperCircle X Platform: http://localhost:{PORT}")
            print("🔗 Professional community platform ready...")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Port already in use
            PORT = 7001
            with socketserver.TCPServer(("", PORT), HyperCircleHandler) as httpd:
                print(f"🌐 HyperCircle X Platform: http://localhost:{PORT}")
                print("🔗 Professional community platform ready...")
                httpd.serve_forever()
        else:
            raise