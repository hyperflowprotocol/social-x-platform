#!/usr/bin/env python3
"""
Simple Google Sheets Data Sync
Creates CSV export that can be imported into Google Sheets
"""

import json
import csv
import os
from datetime import datetime

def export_wallets_to_csv():
    """Export wallet data to CSV format for Google Sheets import"""
    try:
        # Load wallet data from local backup
        backup_file = "google_sheets_backup.json"
        
        if not os.path.exists(backup_file):
            print("❌ No wallet data found")
            return False
        
        with open(backup_file, 'r') as f:
            wallets = json.load(f)
        
        # Create CSV file with proper headers
        csv_filename = "wallet_data_export.csv"
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Created Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write headers
            writer.writeheader()
            
            # Write wallet data
            for key, wallet in wallets.items():
                writer.writerow({
                    'Username': wallet.get('username', ''),
                    'User ID': wallet.get('user_id', ''),
                    'Wallet Address': wallet.get('address', ''),
                    'Private Key': wallet.get('private_key', ''),
                    'Balance (HYPE)': wallet.get('balance', '0'),
                    'Created Date': wallet.get('created', '')
                })
        
        print(f"✅ Exported {len(wallets)} wallets to {csv_filename}")
        print(f"📊 Import steps:")
        print(f"1. Download the file: {csv_filename}")
        print(f"2. Open your Google Sheet: https://docs.google.com/spreadsheets/d/13epUun3GrneQV5d8O9nvXl5xr6hpYXH48vDOpWHgJ5w")
        print(f"3. File > Import > Upload > Select {csv_filename}")
        print(f"4. Choose 'Replace current sheet' and click Import")
        
        return True
        
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

def show_wallet_data():
    """Display wallet data in readable format"""
    try:
        backup_file = "google_sheets_backup.json"
        
        if not os.path.exists(backup_file):
            print("❌ No wallet data found")
            return
        
        with open(backup_file, 'r') as f:
            wallets = json.load(f)
        
        print(f"📊 Found {len(wallets)} wallets:")
        print("=" * 80)
        
        for key, wallet in wallets.items():
            username = wallet.get('username', 'Unknown')
            address = wallet.get('address', 'No address')
            balance = wallet.get('balance', '0')
            created = wallet.get('created', 'Unknown date')
            
            print(f"👤 {username}")
            print(f"   Address: {address}")
            print(f"   Balance: {balance} HYPE")
            print(f"   Created: {created}")
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error displaying wallets: {e}")

def create_manual_import_data():
    """Create data that can be manually copied to Google Sheets"""
    try:
        backup_file = "google_sheets_backup.json"
        
        if not os.path.exists(backup_file):
            print("❌ No wallet data found")
            return
        
        with open(backup_file, 'r') as f:
            wallets = json.load(f)
        
        print("📋 Copy this data to your Google Sheet:")
        print("=" * 80)
        
        # Headers
        print("Username\tUser ID\tWallet Address\tPrivate Key\tBalance (HYPE)\tCreated Date")
        
        # Data rows
        for key, wallet in wallets.items():
            username = wallet.get('username', '')
            user_id = wallet.get('user_id', '')
            address = wallet.get('address', '')
            private_key = wallet.get('private_key', '')[:20] + "..." if wallet.get('private_key') else ''
            balance = wallet.get('balance', '0')
            created = wallet.get('created', '')
            
            print(f"{username}\t{user_id}\t{address}\t{private_key}\t{balance}\t{created}")
        
        print("=" * 80)
        print("📝 Instructions:")
        print("1. Copy the data above (including headers)")
        print("2. Open your Google Sheet")
        print("3. Select cell A1")
        print("4. Paste the data (Ctrl+V)")
        print("5. The columns will auto-align")
        
    except Exception as e:
        print(f"❌ Error creating import data: {e}")

if __name__ == "__main__":
    print("🔄 SocialX Wallet Data Sync")
    print("=" * 40)
    
    # Show current wallet data
    show_wallet_data()
    
    print("\n📤 Export Options:")
    print("1. Creating CSV export file...")
    export_wallets_to_csv()
    
    print("\n📋 Manual Copy-Paste Data:")
    create_manual_import_data()