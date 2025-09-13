import json

def handler(request):
    """Vercel serverless function for market overview API"""
    
    response = {
        "total_market_cap": 12000,
        "total_volume_24h": 2500,
        "active_accounts": 1,
        "active_traders": 145,
        "total_tokens_launched": 1,
        "trending_change": "+25.8%"
    }
    
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