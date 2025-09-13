#!/usr/bin/env python3
"""
Manual Google Sheets Sync
Direct HTTP approach to write wallet data to Google Sheets
"""

import requests
import json
import os
from datetime import datetime

def add_headers_to_sheet():
    """Manually add headers to the Google Sheet"""
    sheet_id = "13epUun3GrneQV5d8O9nvXl5xr6hpYXH48vDOpWHgJ5w"
    
    # Headers for the sheet
    headers = ['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Created Date']
    
    print(f"📋 Adding headers to Google Sheet: {sheet_id}")
    print(f"🔗 Sheet URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
    
    # For now, let's just document what needs to be done
    print("\n📝 To complete the setup manually:")
    print("1. Open your Google Sheet")
    print("2. Add these headers to row 1:")
    
    for i, header in enumerate(headers, 1):
        print(f"   {chr(64+i)}{1}: {header}")
    
    print("\n3. The system will then sync wallet data automatically")
    
    # Add test wallet data to show format
    if os.path.exists('google_sheets_backup.json'):
        with open('google_sheets_backup.json', 'r') as f:
            wallets = json.load(f)
        
        print(f"\n💾 Example wallet data to add:")
        for key, wallet in wallets.items():
            username = wallet.get('username', 'Unknown')
            user_id = wallet.get('user_id', '')
            address = wallet.get('address', '')
            balance = wallet.get('balance', '0')
            created = wallet.get('created', datetime.now().isoformat())
            
            print(f"   {username} | {user_id} | {address} | [private_key] | {balance} | {created}")

if __name__ == "__main__":
    add_headers_to_sheet()