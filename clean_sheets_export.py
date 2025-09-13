#!/usr/bin/env python3
"""
Create clean Google Sheets export with only real users
"""

import json
import csv
import os
import pickle
from datetime import datetime

def create_clean_export():
    """Create clean CSV with only real authenticated users"""
    try:
        # Load session data to get real usernames
        session_data = {}
        if os.path.exists("session_storage.json"):
            with open("session_storage.json", 'r') as f:
                session_data = json.load(f)
        
        # Load wallet data
        user_wallets = {}
        if os.path.exists("user_wallets.pkl"):
            with open("user_wallets.pkl", 'rb') as f:
                user_wallets = pickle.load(f)
        
        # Match session data with wallet data to get real users only
        real_users = []
        
        for session_id, session in session_data.items():
            user_id = session.get('user_id')
            username = session.get('username')
            
            # Only include if we have both real username and user_id
            if user_id and username and not username.startswith('@') and 'pending' not in username:
                # Look for wallet data
                wallet = user_wallets.get(user_id, {})
                
                real_users.append({
                    'username': f"@{username}" if not username.startswith('@') else username,
                    'user_id': str(user_id),
                    'address': wallet.get('address', ''),
                    'private_key': wallet.get('private_key', ''),
                    'balance': wallet.get('balance', '0'),
                    'followers': session.get('followers', ''),
                    'created': datetime.now().isoformat()
                })
        
        # Also include the test user for completeness
        backup_file = "google_sheets_backup.json"
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                backup = json.load(f)
                for key, wallet in backup.items():
                    if wallet.get('username', '').startswith('@'):
                        real_users.append(wallet)
        
        # Remove duplicates based on username
        seen_users = set()
        unique_users = []
        for user in real_users:
            username = user.get('username', '')
            if username and username not in seen_users:
                seen_users.add(username)
                unique_users.append(user)
        
        print(f"📊 REAL USERS FOUND: {len(unique_users)}")
        
        # Generate clean CSV
        csv_file = "google_sheets_clean_export.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            headers = ['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Followers', 'Created Date']
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for user in unique_users:
                writer.writerow([
                    user.get('username', ''),
                    str(user.get('user_id', '')),
                    user.get('address', ''),
                    user.get('private_key', ''),
                    str(user.get('balance', '0')),
                    str(user.get('followers', '')),
                    user.get('created', datetime.now().isoformat())
                ])
                
                # Show user info
                username = user.get('username', 'Unknown')
                address = user.get('address', '')[:20] + "..." if user.get('address') else 'No address'
                balance = user.get('balance', '0')
                followers = user.get('followers', '')
                print(f"   • {username} | {address} | {balance} HYPE | {followers} followers")
        
        print(f"✅ CLEAN CSV GENERATED: {csv_file}")
        print(f"📤 Ready to import {len(unique_users)} REAL users to Google Sheets!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_clean_export()