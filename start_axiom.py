#!/usr/bin/env python3
"""Simple startup script for AXIOM Trading Platform"""
import subprocess
import sys
import time

def start_axiom():
    print("🚀 Starting AXIOM Trading Platform...")
    
    # Kill any existing instances
    subprocess.run(["pkill", "-f", "axiom_trading_platform"], capture_output=True)
    time.sleep(1)
    
    # Start the platform
    try:
        subprocess.run([sys.executable, "axiom_trading_platform.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting platform: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_axiom()