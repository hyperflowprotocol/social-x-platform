#!/usr/bin/env python3
"""
Manual server startup script to bypass port conflicts
"""
import os
import sys
import subprocess
import time
import signal

def kill_existing():
    """Kill existing Python processes on port 5000"""
    try:
        # Find and kill processes using port 5000
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True, check=False)
        for line in result.stdout.split('\n'):
            if ':5000' in line and 'python' in line:
                try:
                    pid = line.split()[-1].split('/')[0]
                    if pid.isdigit():
                        os.kill(int(pid), signal.SIGKILL)
                        print(f"Killed process {pid}")
                except:
                    pass
    except:
        pass
    
    # Alternative approach
    try:
        subprocess.run(['pkill', '-9', '-f', 'social_trading_platform'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'python.*5000'], check=False)
    except:
        pass
    
    time.sleep(2)

def start_server():
    """Start the server with proper environment"""
    print("🔄 Starting SocialX with paid Twitter API...")
    
    # Set environment variables for paid Twitter API
    env = os.environ.copy()
    
    # Start server
    try:
        process = subprocess.Popen([
            'python3', 'social_trading_platform.py'
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Read startup output
        startup_lines = 0
        while startup_lines < 20:  # Read first 20 lines of startup
            line = process.stdout.readline()
            if not line:
                break
            print(line.strip())
            startup_lines += 1
            if "ready..." in line:
                break
        
        return process
        
    except Exception as e:
        print(f"Failed to start server: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Manual SocialX startup with paid Twitter API")
    kill_existing()
    process = start_server()
    
    if process:
        print("✅ Server started successfully!")
        print("🔗 Your redirect URI for Twitter app settings:")
        print("https://3a9e0063-77a5-47c3-8b08-e9c97e127f0a-00-39uxnbmqdszny.picard.replit.dev/callback/twitter")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            process.terminate()
    else:
        print("❌ Failed to start server")
        sys.exit(1)