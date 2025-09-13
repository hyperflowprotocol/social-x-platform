#!/usr/bin/env python3
"""
Working Google Sheets Sync using Google API Client
Direct integration with Google Sheets API v4
"""

import json
import os
from datetime import datetime

# Use the available Google API libraries
try:
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials
    GOOGLE_API_AVAILABLE = True
    print("✅ Google API Client libraries available")
except ImportError as e:
    GOOGLE_API_AVAILABLE = False
    print(f"❌ Google API Client not available: {e}")

class WorkingGoogleSheetsSync:
    def __init__(self, sheet_id, service_account_file):
        self.sheet_id = sheet_id
        self.service_account_file = service_account_file
        self.service = None
        self.sheet_name = "Sheet1"
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if not GOOGLE_API_AVAILABLE:
                print("❌ Google API libraries not available")
                return False
                
            if not os.path.exists(self.service_account_file):
                print(f"❌ Service account file not found: {self.service_account_file}")
                return False
            
            # Define the required scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials from service account file
            credentials = Credentials.from_service_account_file(
                self.service_account_file, 
                scopes=scopes
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            
            print("✅ Google Sheets API authentication successful")
            return True
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def setup_headers(self):
        """Add headers to the Google Sheet"""
        try:
            if not self.service:
                print("❌ Not authenticated")
                return False
                
            headers = [['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Created Date']]
            
            # Clear and add headers
            body = {
                'values': headers
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A1:F1',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            print(f"✅ Headers added successfully: {result.get('updatedCells')} cells updated")
            return True
            
        except Exception as e:
            print(f"❌ Error adding headers: {e}")
            return False
    
    def add_wallet_to_sheet(self, username, user_id, address, private_key, balance):
        """Add a wallet to the Google Sheet"""
        try:
            if not self.service:
                print("❌ Not authenticated")
                return False
            
            # Prepare wallet data
            wallet_row = [[
                username,
                str(user_id),
                address,
                private_key,
                str(balance),
                datetime.now().isoformat()
            ]]
            
            # Append to sheet
            body = {
                'values': wallet_row
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A2:F2',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            print(f"✅ Wallet added to Google Sheet: {username} -> {address}")
            print(f"   Updated range: {result.get('updates', {}).get('updatedRange')}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding wallet: {e}")
            return False
    
    def get_all_wallets(self):
        """Get all wallets from the Google Sheet"""
        try:
            if not self.service:
                print("❌ Not authenticated")
                return []
            
            # Get all data from sheet
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A2:F1000'  # Skip header, get up to 1000 rows
            ).execute()
            
            values = result.get('values', [])
            
            wallets = []
            for row in values:
                if len(row) >= 6:  # Ensure all columns are present
                    wallets.append({
                        'username': row[0],
                        'user_id': row[1],
                        'address': row[2],
                        'private_key': row[3],
                        'balance': row[4],
                        'created': row[5]
                    })
            
            print(f"✅ Retrieved {len(wallets)} wallets from Google Sheet")
            return wallets
            
        except Exception as e:
            print(f"❌ Error getting wallets: {e}")
            return []
    
    def sync_local_wallets_to_sheet(self):
        """Sync all local wallet data to Google Sheets"""
        try:
            backup_file = "google_sheets_backup.json"
            
            if not os.path.exists(backup_file):
                print("❌ No local wallet backup found")
                return False
            
            # Load local wallets
            with open(backup_file, 'r') as f:
                wallets = json.load(f)
            
            print(f"📤 Syncing {len(wallets)} wallets to Google Sheets...")
            
            # Setup headers first
            if not self.setup_headers():
                return False
            
            # Add each wallet
            success_count = 0
            for key, wallet in wallets.items():
                if self.add_wallet_to_sheet(
                    wallet.get('username', ''),
                    wallet.get('user_id', ''),
                    wallet.get('address', ''),
                    wallet.get('private_key', ''),
                    wallet.get('balance', '0')
                ):
                    success_count += 1
            
            print(f"✅ Successfully synced {success_count}/{len(wallets)} wallets")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Error syncing wallets: {e}")
            return False

def test_working_sync():
    """Test the working Google Sheets sync"""
    sheet_id = "13epUun3GrneQV5d8O9nvXl5xr6hpYXH48vDOpWHgJ5w"
    service_account_file = "service_account.json"
    
    print("🧪 Testing Working Google Sheets Sync")
    print("=" * 50)
    
    sync = WorkingGoogleSheetsSync(sheet_id, service_account_file)
    
    # Test authentication
    if sync.authenticate():
        print("✅ Authentication successful")
        
        # Sync all local wallets to sheet
        if sync.sync_local_wallets_to_sheet():
            print("✅ Wallet sync successful")
            
            # Verify by reading back
            wallets = sync.get_all_wallets()
            if wallets:
                print(f"✅ Verification successful: {len(wallets)} wallets in sheet")
                for wallet in wallets[-3:]:  # Show last 3
                    print(f"   - {wallet['username']} | {wallet['address'][:20]}...")
            else:
                print("⚠️ No wallets found in verification")
        else:
            print("❌ Wallet sync failed")
    else:
        print("❌ Authentication failed")

if __name__ == "__main__":
    test_working_sync()