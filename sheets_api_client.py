#!/usr/bin/env python3
"""
Direct Google Sheets API Client
Bypasses gspread dependencies with direct HTTP API calls
"""

import json
import base64
import time
import hmac
import hashlib
import requests
from datetime import datetime
import urllib.parse

# Try to import JWT libraries, fallback if not available
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("⚠️ PyJWT not available, using alternative approach")

try:
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ Cryptography not available, using alternative approach")

class GoogleSheetsAPIClient:
    def __init__(self, sheet_id, service_account_file):
        self.sheet_id = sheet_id
        self.service_account_file = service_account_file
        self.access_token = None
        self.token_expires = 0
        self.service_account_data = None
        
        # Load service account credentials
        try:
            with open(service_account_file, 'r') as f:
                self.service_account_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading service account: {e}")
    
    def create_simple_jwt(self):
        """Create a simple JWT for service account authentication"""
        try:
            # Simple base64 encoding approach (for development)
            now = int(time.time())
            
            header = {
                "alg": "RS256",
                "typ": "JWT"
            }
            
            payload = {
                "iss": self.service_account_data["client_email"],
                "scope": "https://www.googleapis.com/auth/spreadsheets",
                "aud": "https://oauth2.googleapis.com/token", 
                "exp": now + 3600,
                "iat": now
            }
            
            # Base64 encode header and payload
            header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
            payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
            
            # For now, return unsigned token (will implement signing later if needed)
            unsigned_token = f"{header_b64}.{payload_b64}"
            
            return unsigned_token
            
        except Exception as e:
            print(f"❌ JWT creation error: {e}")
            return None
    
    def get_access_token(self):
        """Get valid access token using alternative methods"""
        try:
            current_time = int(time.time())
            
            # Check if token is still valid (with 5 minute buffer)
            if self.access_token and current_time < (self.token_expires - 300):
                return self.access_token
            
            print("🔄 Getting new access token...")
            
            if JWT_AVAILABLE and CRYPTO_AVAILABLE:
                # Use full JWT implementation
                return self.get_jwt_token()
            else:
                # Use direct API key approach if available
                return self.get_api_key_token()
                
        except Exception as e:
            print(f"❌ Access token error: {e}")
            return None
    
    def get_jwt_token(self):
        """Get token using JWT (if libraries available)"""
        try:
            now = int(time.time())
            
            jwt_payload = {
                "iss": self.service_account_data["client_email"],
                "scope": "https://www.googleapis.com/auth/spreadsheets",
                "aud": "https://oauth2.googleapis.com/token",
                "exp": now + 3600,
                "iat": now
            }
            
            # Load private key
            private_key = serialization.load_pem_private_key(
                self.service_account_data["private_key"].encode(),
                password=None
            )
            
            # Create JWT
            token = jwt.encode(jwt_payload, private_key, algorithm="RS256")
            
            # Make token request
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": token
            }
            
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.token_expires = time.time() + token_data.get("expires_in", 3600)
                print("✅ JWT access token obtained")
                return self.access_token
            else:
                print(f"❌ JWT token request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ JWT token error: {e}")
            return None
    
    def get_api_key_token(self):
        """Alternative token method using Google API approach"""
        try:
            # For now, return None and suggest manual setup
            print("⚠️ JWT libraries not available")
            print("📝 Using fallback to local storage")
            print("🔧 Consider manual Google Sheets setup")
            
            return None
            
        except Exception as e:
            print(f"❌ API key token error: {e}")
            return None
    
    def setup_headers(self):
        """Add headers to the Google Sheet"""
        try:
            headers = ['Username', 'User ID', 'Wallet Address', 'Private Key', 'Balance (HYPE)', 'Created Date']
            
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.sheet_id}/values/Sheet1!A1:F1"
            
            request_headers = {
                "Authorization": f"Bearer {self.get_access_token()}",
                "Content-Type": "application/json"
            }
            
            data = {
                "range": "Sheet1!A1:F1",
                "majorDimension": "ROWS",
                "values": [headers]
            }
            
            response = requests.put(url, headers=request_headers, json=data, params={"valueInputOption": "USER_ENTERED"})
            
            if response.status_code == 200:
                print("✅ Headers added to Google Sheet")
                return True
            else:
                print(f"❌ Failed to add headers: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error setting up headers: {e}")
            return False
    
    def append_wallet(self, username, user_id, address, private_key, balance):
        """Append wallet data to the Google Sheet"""
        try:
            row_data = [username, str(user_id), address, private_key, str(balance), datetime.now().isoformat()]
            
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.sheet_id}/values/Sheet1:append"
            
            request_headers = {
                "Authorization": f"Bearer {self.get_access_token()}",
                "Content-Type": "application/json"
            }
            
            data = {
                "range": "Sheet1",
                "majorDimension": "ROWS",
                "values": [row_data]
            }
            
            response = requests.post(url, headers=request_headers, json=data, params={"valueInputOption": "USER_ENTERED"})
            
            if response.status_code == 200:
                print(f"✅ Added wallet to Google Sheet: {username}")
                return True
            else:
                print(f"❌ Failed to add wallet: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error appending wallet: {e}")
            return False
    
    def get_all_wallets(self):
        """Get all wallet data from the Google Sheet"""
        try:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.sheet_id}/values/Sheet1"
            
            request_headers = {
                "Authorization": f"Bearer {self.get_access_token()}"
            }
            
            response = requests.get(url, headers=request_headers)
            
            if response.status_code == 200:
                data = response.json()
                values = data.get("values", [])
                
                if len(values) > 1:  # Skip header row
                    wallets = []
                    for row in values[1:]:  # Skip header
                        if len(row) >= 6:  # Ensure all columns present
                            wallets.append({
                                'username': row[0],
                                'user_id': row[1],
                                'address': row[2],
                                'private_key': row[3],
                                'balance': row[4],
                                'created': row[5]
                            })
                    return wallets
                else:
                    return []
            else:
                print(f"❌ Failed to get wallets: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting wallets: {e}")
            return []

def test_sheets_api():
    """Test the Google Sheets API client"""
    sheet_id = "13epUun3GrneQV5d8O9nvXl5xr6hpYXH48vDOpWHgJ5w"
    service_account_file = "service_account.json"
    
    client = GoogleSheetsAPIClient(sheet_id, service_account_file)
    
    print("🧪 Testing Google Sheets API Client")
    print("=" * 50)
    
    # Test authentication
    token = client.get_access_token()
    if token:
        print("✅ Authentication successful")
        
        # Setup headers
        if client.setup_headers():
            print("✅ Headers setup successful")
            
            # Test adding a wallet
            if client.append_wallet("@test_api_user", "999999999", "0x1234567890123456789012345678901234567890", "test_private_key", "2.5"):
                print("✅ Wallet addition successful")
                
                # Test getting wallets
                wallets = client.get_all_wallets()
                print(f"✅ Retrieved {len(wallets)} wallets from sheet")
                
                for wallet in wallets[-3:]:  # Show last 3 wallets
                    print(f"   - {wallet['username']} | {wallet['address']}")
            else:
                print("❌ Wallet addition failed")
        else:
            print("❌ Headers setup failed")
    else:
        print("❌ Authentication failed")

if __name__ == "__main__":
    test_sheets_api()