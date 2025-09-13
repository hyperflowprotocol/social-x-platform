#!/usr/bin/env python3
"""
Simple test to check Flask import and basic functionality
"""

try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    print("✅ Flask imports successful")
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok', 'message': 'Flask is working'})
    
    if __name__ == '__main__':
        import os
        port = int(os.getenv('PORT', 3000))
        print(f"🚀 Starting test Flask app on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")