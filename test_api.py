#!/usr/bin/env python3
"""Test script to verify API endpoints are working"""

import urllib.request
import json
import sys

def test_api_endpoint(endpoint):
    """Test a single API endpoint"""
    try:
        url = f"http://localhost:3000{endpoint}"
        print(f"Testing {url}")
        
        with urllib.request.urlopen(url, timeout=5) as response:
            status = response.status
            content_type = response.headers.get('Content-Type', '')
            data = response.read().decode('utf-8')
            
            print(f"  Status: {status}")
            print(f"  Content-Type: {content_type}")
            print(f"  Response length: {len(data)} bytes")
            
            if content_type.startswith('application/json'):
                try:
                    json_data = json.loads(data)
                    print(f"  Valid JSON: Yes")
                    print(f"  Data: {json_data}")
                except json.JSONDecodeError:
                    print(f"  Valid JSON: No - {data[:100]}")
            else:
                print(f"  Raw data: {data[:100]}")
            
            return status == 200
            
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

if __name__ == "__main__":
    endpoints = [
        "/api/trending-accounts", 
        "/api/market-overview",
        "/api/recent-trades"
    ]
    
    print("Testing SocialX API endpoints...")
    print("=" * 50)
    
    all_passed = True
    for endpoint in endpoints:
        success = test_api_endpoint(endpoint)
        all_passed = all_passed and success
        print()
    
    if all_passed:
        print("✅ All API endpoints working correctly!")
        sys.exit(0)
    else:
        print("❌ Some API endpoints failed!")
        sys.exit(1)