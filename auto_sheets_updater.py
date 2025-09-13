#!/usr/bin/env python3
"""
Auto Google Sheets Updater
Monitors wallet data and automatically generates updated CSV exports
"""

import json
import csv
import os
import time
from datetime import datetime

class AutoSheetsUpdater:
    def __init__(self):
        self.backup_file = "google_sheets_backup.json"
        self.csv_file = "wallet_data_export.csv"
        self.last_modified = 0
        self.sheet_id = "13epUun3GrneQV5d8O9nvXl5xr6hpYXH48vDOpWHgJ5w"
        self.last_wallet_count = 0
        
    def get_wallet_data(self):
        """Get current wallet data"""
        try:
            if not os.path.exists(self.backup_file):
                return {}
            
            with open(self.backup_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading wallet data: {e}")
            return {}
    
    def generate_csv_export(self, wallets):
        """Generate CSV export file"""
        try:
            headers = ['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Created Date']
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for key, wallet in wallets.items():
                    writer.writerow({
                        'Username': wallet.get('username', ''),
                        'User ID': wallet.get('user_id', ''),
                        'Wallet Address': wallet.get('address', ''),
                        'Private Key': wallet.get('private_key', ''),
                        'Balance (HYPE)': wallet.get('balance', '0'),
                        'Created Date': wallet.get('created', '')
                    })
            
            return True
        except Exception as e:
            print(f"❌ CSV generation error: {e}")
            return False
    
    def check_for_updates(self):
        """Check if wallet data has been updated"""
        try:
            if not os.path.exists(self.backup_file):
                return False
            
            # Check if file was modified
            current_modified = os.path.getmtime(self.backup_file)
            
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                return True
            
            return False
        except Exception as e:
            print(f"❌ Error checking updates: {e}")
            return False
    
    def update_sheet_data(self):
        """Update CSV export and show instructions"""
        try:
            wallets = self.get_wallet_data()
            wallet_count = len(wallets)
            
            if wallet_count == 0:
                print("⚠️ No wallet data found")
                return False
            
            # Generate new CSV
            if self.generate_csv_export(wallets):
                print(f"✅ Updated CSV export with {wallet_count} wallets")
                
                # Show update instructions if new wallets were added
                if wallet_count > self.last_wallet_count:
                    new_wallets = wallet_count - self.last_wallet_count
                    print(f"🆕 {new_wallets} new wallet(s) added!")
                    print(f"📤 To update your Google Sheet:")
                    print(f"   1. Download: {self.csv_file}")
                    print(f"   2. Go to: https://docs.google.com/spreadsheets/d/{self.sheet_id}")
                    print(f"   3. File > Import > Upload CSV > Replace current sheet")
                    print(f"   4. Click 'Import data'")
                    
                    # Show recent wallets
                    print(f"\n📋 Latest wallets:")
                    for key, wallet in list(wallets.items())[-new_wallets:]:
                        username = wallet.get('username', 'Unknown')
                        address = wallet.get('address', '')[:20] + "..." if wallet.get('address') else 'No address'
                        print(f"   • {username} | {address}")
                
                self.last_wallet_count = wallet_count
                return True
            else:
                print("❌ Failed to generate CSV export")
                return False
                
        except Exception as e:
            print(f"❌ Update error: {e}")
            return False
    
    def monitor_wallets(self, interval=30):
        """Monitor wallet data for changes"""
        print(f"🔄 Starting wallet monitor (checking every {interval}s)")
        print(f"📊 Monitoring file: {self.backup_file}")
        print(f"📤 CSV export: {self.csv_file}")
        print(f"🔗 Google Sheet: https://docs.google.com/spreadsheets/d/{self.sheet_id}")
        print("-" * 60)
        
        # Initial check
        self.update_sheet_data()
        
        try:
            while True:
                if self.check_for_updates():
                    print(f"🔔 Wallet data updated at {datetime.now().strftime('%H:%M:%S')}")
                    self.update_sheet_data()
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped")
    
    def show_current_status(self):
        """Show current wallet status"""
        try:
            wallets = self.get_wallet_data()
            
            print(f"📊 Current Status:")
            print(f"   Wallets stored: {len(wallets)}")
            print(f"   CSV file: {'✅ Available' if os.path.exists(self.csv_file) else '❌ Not found'}")
            print(f"   Last updated: {datetime.fromtimestamp(os.path.getmtime(self.backup_file)).strftime('%Y-%m-%d %H:%M:%S') if os.path.exists(self.backup_file) else 'Never'}")
            
            if len(wallets) > 0:
                print(f"\n📋 Recent wallets:")
                for key, wallet in list(wallets.items())[-3:]:
                    username = wallet.get('username', 'Unknown')
                    address = wallet.get('address', '')
                    balance = wallet.get('balance', '0')
                    print(f"   • {username} | {address[:20]}... | {balance} HYPE")
                    
            return len(wallets)
            
        except Exception as e:
            print(f"❌ Status error: {e}")
            return 0

def main():
    """Main function"""
    updater = AutoSheetsUpdater()
    
    print("🚀 SocialX Google Sheets Auto-Updater")
    print("=" * 50)
    
    # Show current status
    wallet_count = updater.show_current_status()
    
    if wallet_count > 0:
        print(f"\n🔄 Generating fresh CSV export...")
        updater.update_sheet_data()
        
        print(f"\n⚡ Auto-monitor mode available:")
        print(f"   Run: python3 auto_sheets_updater.py monitor")
        print(f"   This will automatically update CSV when new wallets are added")
    else:
        print(f"\n⚠️ No wallets found. Wallets will appear when users authenticate.")

if __name__ == "__main__":
    import sys
    
    updater = AutoSheetsUpdater()
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        updater.monitor_wallets()
    else:
        main()