#!/usr/bin/env python3
"""
X Pro Profile Sync for $54K/year plans
Dedicated script to fetch real profile data using premium API access
"""

import os
import json
import urllib.request
import urllib.parse
import time
from datetime import datetime

def fetch_x_pro_profile(access_token, user_id):
    """
    Fetch real X profile data using X Pro API endpoints
    """
    print(f"🔍 X Pro Profile Sync for user: {user_id}")
    print(f"💎 Using $54K/year X Pro API access")
    
    # X Pro specific endpoints with higher rate limits
    endpoints = [
        {
            'url': 'https://api.twitter.com/2/users/me',
            'params': {
                'user.fields': 'id,name,username,profile_image_url,description,public_metrics,verified,created_at,location,url'
            }
        },
        {
            'url': 'https://api.twitter.com/1.1/account/verify_credentials.json',
            'params': {
                'include_entities': 'true',
                'skip_status': 'false'
            }
        }
    ]
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'SocialX-XPro-ProfileSync/1.0',
        'Accept': 'application/json'
    }
    
    for endpoint in endpoints:
        try:
            # Build URL with parameters
            if endpoint['params']:
                url = f"{endpoint['url']}?{urllib.parse.urlencode(endpoint['params'])}"
            else:
                url = endpoint['url']
                
            print(f"📡 API Call: {url}")
            
            request = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    # Parse response based on API version
                    if 'data' in data:  # v2 API
                        user = data['data']
                        profile = {
                            'id': str(user['id']),
                            'name': user['name'],
                            'username': user['username'],
                            'handle': f"@{user['username']}",
                            'avatar': user.get('profile_image_url', '').replace('_normal', '_400x400'),
                            'description': user.get('description', ''),
                            'verified': user.get('verified', False),
                            'followers': user.get('public_metrics', {}).get('followers_count', 0),
                            'following': user.get('public_metrics', {}).get('following_count', 0),
                            'tweets': user.get('public_metrics', {}).get('tweet_count', 0),
                            'created_at': user.get('created_at', ''),
                            'location': user.get('location', ''),
                            'url': user.get('url', ''),
                            'fetched_at': datetime.now().isoformat(),
                            'api_version': '2.0'
                        }
                        
                    elif 'screen_name' in data:  # v1.1 API
                        profile = {
                            'id': str(data['id']),
                            'name': data['name'],
                            'username': data['screen_name'],
                            'handle': f"@{data['screen_name']}",
                            'avatar': data.get('profile_image_url_https', '').replace('_normal', '_400x400'),
                            'description': data.get('description', ''),
                            'verified': data.get('verified', False),
                            'followers': data.get('followers_count', 0),
                            'following': data.get('friends_count', 0),
                            'tweets': data.get('statuses_count', 0),
                            'created_at': data.get('created_at', ''),
                            'location': data.get('location', ''),
                            'url': data.get('url', ''),
                            'fetched_at': datetime.now().isoformat(),
                            'api_version': '1.1'
                        }
                    else:
                        print(f"❌ Unexpected response format: {json.dumps(data, indent=2)}")
                        continue
                    
                    print(f"✅ SUCCESS! Real X profile data:")
                    print(f"   Name: {profile['name']}")
                    print(f"   Handle: {profile['handle']}")
                    print(f"   Followers: {profile['followers']:,}")
                    print(f"   Verified: {profile['verified']}")
                    
                    # Save to cache file
                    cache_file = f"x_pro_profile_{user_id}.json"
                    with open(cache_file, 'w') as f:
                        json.dump(profile, f, indent=2)
                    print(f"💾 Profile cached: {cache_file}")
                    
                    return profile
                    
                else:
                    error_data = response.read().decode('utf-8')
                    print(f"❌ API Error {response.status}: {error_data}")
                    
        except Exception as e:
            print(f"❌ Endpoint failed: {str(e)}")
            continue
    
    print("❌ All X Pro endpoints failed - this should not happen with $54K plan")
    return None

def update_user_session(user_id, profile_data):
    """
    Update the user session with real profile data
    """
    try:
        import pickle
        
        # Load existing wallets
        with open('user_wallets.pkl', 'rb') as f:
            wallets = pickle.load(f)
        
        session_key = f"session_{user_id}"
        if session_key in wallets:
            # Update with real profile data
            wallets[session_key].update({
                'name': profile_data['name'],
                'handle': profile_data['handle'],
                'followers': profile_data['followers'],
                'following': profile_data['following'],
                'tweets': profile_data['tweets'],
                'verified': profile_data['verified'],
                'description': profile_data['description'],
                'avatar': profile_data['avatar'],
                'profile_updated_at': datetime.now().isoformat(),
                'needs_profile_update': False
            })
            
            # Save back to disk
            with open('user_wallets.pkl', 'wb') as f:
                pickle.dump(wallets, f)
            
            print(f"✅ User session updated with real profile data")
            return True
            
    except Exception as e:
        print(f"❌ Session update failed: {str(e)}")
        
    return False

if __name__ == "__main__":
    # Test with environment token
    access_token = os.getenv('TWITTER_BEARER_TOKEN')
    if access_token:
        profile = fetch_x_pro_profile(access_token, 'test_user')
        if profile:
            print("🧪 X Pro profile sync test successful!")
        else:
            print("❌ X Pro profile sync test failed")
    else:
        print("❌ No access token for testing")