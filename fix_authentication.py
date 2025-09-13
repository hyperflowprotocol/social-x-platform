#!/usr/bin/env python3
"""
Fix for Twitter authentication session persistence issue
This handles rate limiting while maintaining authenticated sessions
"""

import pickle
import json
import time

def fix_authentication_session():
    """
    Fix the authentication session to handle Twitter rate limiting
    while maintaining user authentication state
    """
    try:
        # Load existing wallets
        with open('user_wallets.pkl', 'rb') as f:
            wallets = pickle.load(f)
        
        print("🔧 Fixing authentication sessions...")
        
        # Find sessions that need profile data
        fixed_sessions = 0
        for key, data in wallets.items():
            if key.startswith('session_') and isinstance(data, dict):
                if data.get('needs_profile_update') and data.get('access_token'):
                    print(f"📝 Found session needing profile update: {key}")
                    
                    # Mark as properly authenticated but pending profile
                    data['authenticated'] = True
                    data['profile_retry_count'] = data.get('profile_retry_count', 0)
                    data['last_profile_attempt'] = time.time()
                    
                    # Update display to show it's authenticated but profile pending
                    if data.get('handle', '').startswith('@twitter_user'):
                        data['handle'] = f"@authenticated_{data['user_id'][-6:]}"
                        data['name'] = "Authenticated User"
                        data['description'] = "Profile data will update when Twitter API allows"
                    
                    fixed_sessions += 1
        
        # Save updated wallets
        with open('user_wallets.pkl', 'wb') as f:
            pickle.dump(wallets, f)
        
        print(f"✅ Fixed {fixed_sessions} authentication sessions")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing authentication: {e}")
        return False

if __name__ == '__main__':
    fix_authentication_session()