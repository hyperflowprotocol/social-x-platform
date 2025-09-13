#!/usr/bin/env python3
"""
Real-time X Profile Data Fetcher
Continuously tries to get authentic X profile data for paid API users
"""

import requests
import time
import os
import json
from datetime import datetime

def fetch_real_profile_data(access_token, max_retries=10, delay_between_tries=30):
    """
    Continuously attempt to fetch real X profile data
    Returns real data or None if all attempts fail
    """
    
    # Multiple API endpoints to try
    endpoints = [
        {
            'url': 'https://api.twitter.com/2/users/me',
            'params': {
                'user.fields': 'id,name,username,profile_image_url,description,public_metrics,verified,created_at'
            },
            'version': '2.0'
        },
        {
            'url': 'https://api.twitter.com/1.1/account/verify_credentials.json',
            'params': {
                'include_entities': 'false',
                'skip_status': 'true'
            },
            'version': '1.1'
        },
        {
            'url': 'https://api.twitter.com/2/users/me',
            'params': {
                'user.fields': 'public_metrics'
            },
            'version': '2.0'
        }
    ]
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'SocialX-Real-Profile-Fetcher/1.0',
        'Content-Type': 'application/json'
    }
    
    for attempt in range(max_retries):
        print(f"🔍 Real profile fetch attempt {attempt + 1}/{max_retries}")
        
        for i, endpoint in enumerate(endpoints):
            try:
                print(f"   Trying endpoint {i+1}: {endpoint['version']} API")
                
                response = requests.get(
                    endpoint['url'], 
                    params=endpoint['params'],
                    headers=headers, 
                    timeout=15
                )
                
                print(f"   Response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    real_profile = parse_profile_response(data, endpoint['version'])
                    
                    if real_profile:
                        print(f"✅ SUCCESS! Real X profile data retrieved:")
                        print(f"   Username: @{real_profile['username']}")
                        print(f"   Followers: {real_profile['followers']:,}")
                        print(f"   Name: {real_profile['name']}")
                        return real_profile
                        
                elif response.status_code == 429:
                    print(f"   Rate limited - waiting {delay_between_tries}s before next attempt")
                    time.sleep(delay_between_tries)
                    break  # Try next attempt cycle
                    
                else:
                    print(f"   API error {response.status_code}: {response.text[:200]}")
                    
            except Exception as e:
                print(f"   Endpoint {i+1} failed: {str(e)}")
                continue
        
        if attempt < max_retries - 1:
            print(f"   All endpoints failed, waiting {delay_between_tries}s before retry...")
            time.sleep(delay_between_tries)
    
    print("❌ All attempts failed - no real profile data available")
    return None

def parse_profile_response(data, api_version):
    """Parse API response into standardized profile format"""
    try:
        if api_version == '2.0' and 'data' in data:
            user = data['data']
            metrics = user.get('public_metrics', {})
            
            return {
                'id': str(user['id']),
                'name': user['name'],
                'username': user['username'],
                'handle': f"@{user['username']}",
                'avatar': user.get('profile_image_url', '').replace('_normal', '_400x400'),
                'description': user.get('description', ''),
                'verified': user.get('verified', False),
                'followers': metrics.get('followers_count', 0),
                'following': metrics.get('following_count', 0),
                'tweets': metrics.get('tweet_count', 0),
                'created_at': user.get('created_at', ''),
                'fetched_at': datetime.now().isoformat(),
                'is_real_data': True
            }
            
        elif api_version == '1.1' and 'screen_name' in data:
            return {
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
                'fetched_at': datetime.now().isoformat(),
                'is_real_data': True
            }
            
    except Exception as e:
        print(f"❌ Profile parsing failed: {str(e)}")
        
    return None

def save_real_profile_cache(user_id, profile_data):
    """Save real profile data to cache file"""
    try:
        cache_file = f"real_profiles_{user_id}.json"
        with open(cache_file, 'w') as f:
            json.dump(profile_data, f, indent=2)
        print(f"💾 Real profile data cached: {cache_file}")
    except Exception as e:
        print(f"❌ Cache save failed: {str(e)}")

def load_real_profile_cache(user_id):
    """Load cached real profile data"""
    try:
        cache_file = f"real_profiles_{user_id}.json"
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
            print(f"📂 Loaded cached real profile: @{data['username']}")
            return data
    except Exception as e:
        print(f"❌ Cache load failed: {str(e)}")
    return None

if __name__ == "__main__":
    # Test the fetcher
    access_token = os.getenv('TWITTER_BEARER_TOKEN')
    if access_token:
        print("🧪 Testing real profile fetcher...")
        result = fetch_real_profile_data(access_token, max_retries=3, delay_between_tries=10)
        if result:
            print("✅ Test successful!")
            print(json.dumps(result, indent=2))
        else:
            print("❌ Test failed - no real data retrieved")
    else:
        print("❌ No access token provided")