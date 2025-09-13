#!/usr/bin/env python3
"""
Twitter App Configuration Debugger
"""
import os
import requests
import base64
import json

def check_twitter_app_config():
    """Check Twitter app configuration and permissions"""
    client_id = os.getenv('TWITTER_CLIENT_ID')
    client_secret = os.getenv('TWITTER_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Twitter credentials not found in environment")
        return False
    
    print(f"🔑 Twitter Client ID: {client_id[:15]}...")
    
    # Check if we can make a basic API call
    try:
        # Create basic auth header
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        
        # Test with Twitter API v2 to check app status
        response = requests.post(
            'https://api.twitter.com/oauth2/token',
            headers=headers,
            data='grant_type=client_credentials',
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Twitter API credentials are valid")
            return True
        else:
            print(f"❌ Twitter API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Twitter API: {e}")
        return False

def print_config_instructions():
    """Print detailed Twitter app configuration instructions"""
    print("\n" + "="*60)
    print("🔧 TWITTER APP CONFIGURATION REQUIRED")
    print("="*60)
    
    print("\n1. Go to: https://developer.twitter.com/en/portal/dashboard")
    print("2. Select your app with paid subscription")
    print("3. Click 'User authentication settings'")
    print("4. Configure these settings:")
    
    print("\n   📋 App Type: Web App")
    print("   📋 App permissions: Read")
    print("   📋 OAuth 2.0: ENABLED")
    print("   📋 Callback URI (COPY EXACTLY):")
    print("   https://3a9e0063-77a5-47c3-8b08-e9c97e127f0a-00-39uxnbmqdszny.picard.replit.dev/callback/twitter")
    
    print("\n   📋 Website URL: https://socialx-trading.replit.app")
    print("   📋 Terms of Service: https://socialx-trading.replit.app/terms")
    print("   📋 Privacy Policy: https://socialx-trading.replit.app/privacy")
    
    print("\n5. IMPORTANT: After saving, wait 5-10 minutes for Twitter to propagate changes")
    print("6. Make sure your app is NOT in 'Restricted' mode")
    
    print("\n" + "="*60)
    print("🚨 COMMON ISSUES:")
    print("="*60)
    print("- App permissions too restrictive")
    print("- Callback URI doesn't match exactly")
    print("- App is in development/restricted mode")
    print("- Changes haven't propagated yet (wait 5-10 min)")
    print("- OAuth 2.0 not enabled")

if __name__ == "__main__":
    print("🔍 Twitter App Configuration Debugger")
    print("=" * 50)
    
    if check_twitter_app_config():
        print("\n✅ API credentials work - issue is likely app configuration")
    else:
        print("\n❌ API credentials issue - check environment variables")
    
    print_config_instructions()