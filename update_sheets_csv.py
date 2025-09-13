#!/usr/bin/env python3
"""
Force update Google Sheets CSV with ALL current wallet data
Including session data and backup data
"""

import json
import csv
import os
import pickle
from datetime import datetime

def update_sheets_csv_force():
    """Force update CSV with all available wallet data"""
    try:
        all_wallets = {}
        
        print("🔍 Scanning for wallet data...")
        
        # Check Google Sheets backup
        backup_file = "google_sheets_backup.json"
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
                print(f"📂 Found {len(backup_data)} wallets in google_sheets_backup.json")
                all_wallets.update(backup_data)
        
        # Check user wallets pickle file
        user_wallets_file = "user_wallets.pkl"
        if os.path.exists(user_wallets_file):
            with open(user_wallets_file, 'rb') as f:
                user_wallets = pickle.load(f)
                print(f"📂 Found {len(user_wallets)} wallets in user_wallets.pkl")
                
                # Convert pickle format to backup format
                for user_id, wallet_info in user_wallets.items():
                    wallet_key = f"user_{user_id}"
                    if wallet_key not in all_wallets:
                        all_wallets[wallet_key] = {
                            'user_id': user_id,
                            'username': wallet_info.get('username', f'user_{user_id}'),
                            'address': wallet_info.get('address', ''),
                            'private_key': wallet_info.get('private_key', ''),
                            'balance': wallet_info.get('balance', '0'),
                            'created': datetime.now().isoformat()
                        }
        
        # Check session file
        session_file = "session_storage.json"
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                print(f"📂 Found session data: {len(session_data)} entries")
                
                # Extract user data from sessions
                for session_id, session_info in session_data.items():
                    if 'user_id' in session_info and 'username' in session_info:
                        user_id = session_info['user_id']
                        wallet_key = f"user_{user_id}"
                        
                        if wallet_key not in all_wallets:
                            all_wallets[wallet_key] = {
                                'user_id': user_id,
                                'username': session_info.get('username', f'user_{user_id}'),
                                'address': session_info.get('address', ''),
                                'private_key': session_info.get('private_key', ''),
                                'balance': session_info.get('balance', '0'),
                                'followers': session_info.get('followers', 0),
                                'created': datetime.now().isoformat()
                            }
        
        print(f"📊 TOTAL WALLETS FOUND: {len(all_wallets)}")
        
        # Show wallet summary
        for key, wallet in list(all_wallets.items())[-5:]:  # Show last 5
            username = wallet.get('username', 'Unknown')
            address = wallet.get('address', '')[:20] + "..." if wallet.get('address') else 'No address'
            balance = wallet.get('balance', '0')
            followers = wallet.get('followers', '')
            print(f"   • {username} | {address} | {balance} HYPE | {followers} followers")
        
        # Generate comprehensive CSV
        csv_file = "google_sheets_import.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            headers = ['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Followers', 'Created Date']
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for key, wallet in all_wallets.items():
                writer.writerow([
                    wallet.get('username', ''),
                    str(wallet.get('user_id', '')),
                    wallet.get('address', ''),
                    wallet.get('private_key', ''),
                    str(wallet.get('balance', '0')),
                    str(wallet.get('followers', '')),
                    wallet.get('created', datetime.now().isoformat())
                ])
        
        # Also update the backup file with complete data
        with open(backup_file, 'w') as f:
            json.dump(all_wallets, f, indent=2)
        
        print(f"✅ CSV GENERATED: {csv_file}")
        print(f"✅ BACKUP UPDATED: {backup_file}")
        print(f"📤 Ready to import {len(all_wallets)} wallets to Google Sheets!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_sheets_csv_force()