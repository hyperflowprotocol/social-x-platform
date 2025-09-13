from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def handler(request):
    """Vercel serverless function for trending accounts API"""
    
    # @diero_hl profile data
    accounts = [{
        "name": "diero_hl", 
        "handle": "diero_hl", 
        "avatar": "/avatar-diero.png",
        "price_per_token": 0.12, 
        "market_cap": 12000, 
        "daily_change": 25.8,
        "holders": 145,
        "volume_24h": 2500
    }]
    
    response = {"accounts": accounts}
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(response)
    }