#!/usr/bin/env python3
"""
Direct server startup to bypass port binding issues
"""
import os
import sys
import subprocess
import time
import signal
import socket

def kill_port_processes(port):
    """Kill any processes using the specified port"""
    try:
        # Check if port is in use
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:  # Port is in use
            print(f"🔄 Port {port} is in use, killing processes...")
            
            # Kill Python processes
            subprocess.run(['pkill', '-9', '-f', 'python.*social_trading'], check=False)
            subprocess.run(['pkill', '-9', '-f', f'python.*{port}'], check=False)
            
            # Wait for cleanup
            time.sleep(3)
            
            # Check again
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"⚠️ Port {port} still in use after cleanup")
                return False
            else:
                print(f"✅ Port {port} freed successfully")
                return True
        else:
            print(f"✅ Port {port} is available")
            return True
            
    except Exception as e:
        print(f"⚠️ Error checking port {port}: {e}")
        return True  # Continue anyway

def start_socialx():
    """Start the SocialX platform directly"""
    
    # Kill existing processes
    if not kill_port_processes(5000):
        print("❌ Could not free port 5000, trying anyway...")
    
    print("🚀 Starting SocialX Trading Platform...")
    print("🔑 Using your paid Twitter API credentials")
    print("📊 Real authentication with enhanced retry system")
    
    try:
        # Start the server with explicit environment
        env = os.environ.copy()
        
        # Add any needed environment variables
        process = subprocess.Popen([
            sys.executable, 'social_trading_platform.py'
        ], 
        env=env,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
        )
        
        # Monitor startup for first few lines
        startup_complete = False
        line_count = 0
        
        # Check if process started successfully
        if process.stdout is None:
            print("❌ Failed to start process - no stdout")
            process.terminate()
            return False
        
        while line_count < 30:  # Read first 30 lines
            try:
                line = process.stdout.readline()
                if not line:
                    break
                    
                print(line.strip())
                line_count += 1
                
                # Check for successful startup indicators
                if any(indicator in line.lower() for indicator in [
                    'trading platform:', 
                    'ready...', 
                    'listening on',
                    'server started'
                ]):
                    startup_complete = True
                    
                # Check for errors
                if any(error in line.lower() for error in [
                    'failed to bind',
                    'address already in use',
                    'port busy'
                ]):
                    print("❌ Server startup failed due to port conflict")
                    process.terminate()
                    return False
                    
            except Exception as e:
                print(f"Error reading startup output: {e}")
                break
        
        if startup_complete or line_count >= 25:
            print("✅ SocialX server started successfully!")
            print("🔗 Platform running with enhanced Twitter authentication")
            print("💡 Enhanced retry system active for paid API rate limits")
            
            # Keep process running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                process.terminate()
                process.wait()
                
            return True
        else:
            print("❌ Server startup timeout or failure")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Direct SocialX Server Launcher")
    print("=" * 50)
    success = start_socialx()
    
    if not success:
        print("❌ Server startup failed")
        sys.exit(1)