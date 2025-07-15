from flask import Flask, render_template_string, jsonify
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)

# Simple HTML template for the scanner interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Projects Scanner</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .scan-button { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; display: block; margin: 20px auto; }
        .scan-button:hover { background: #2980b9; }
        .scan-button:disabled { background: #bdc3c7; cursor: not-allowed; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .status.info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .env-check { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .env-item { margin: 5px 0; }
        .env-ok { color: #28a745; }
        .env-missing { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Projects Scanner</h1>
        <p style="text-align: center; color: #666;">Monitors Telegram groups and analyzes projects with AI</p>
        
        <div class="env-check">
            <h3>📋 Configuration Status:</h3>
            <div id="envStatus">Loading...</div>
        </div>
        
        <button class="scan-button" onclick="startScan()" id="scanBtn">
            🔍 Test Scanner
        </button>
        
        <div id="results"></div>
    </div>

    <script>
        // Check environment variables on page load
        fetch('/api/check-env')
            .then(response => response.json())
            .then(data => {
                const envStatus = document.getElementById('envStatus');
                let html = '';
                
                Object.entries(data.env_vars).forEach(([key, status]) => {
                    const statusClass = status ? 'env-ok' : 'env-missing';
                    const statusIcon = status ? '✅' : '❌';
                    html += `<div class="env-item ${statusClass}">${statusIcon} ${key}: ${status ? 'Set' : 'Missing'}</div>`;
                });
                
                envStatus.innerHTML = html;
            })
            .catch(error => {
                document.getElementById('envStatus').innerHTML = '<div class="env-missing">❌ Error checking environment</div>';
            });
        
        async function startScan() {
            const btn = document.getElementById('scanBtn');
            const results = document.getElementById('results');
            
            btn.disabled = true;
            btn.textContent = '⏳ Testing...';
            results.innerHTML = '';
            
            try {
                const response = await fetch('/api/test');
                const data = await response.json();
                
                btn.disabled = false;
                btn.textContent = '🔍 Test Scanner';
                
                if (data.success) {
                    results.innerHTML = `<div class="status success">✅ ${data.message}</div>`;
                } else {
                    results.innerHTML = `<div class="status error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                btn.disabled = false;
                btn.textContent = '🔍 Test Scanner';
                results.innerHTML = `<div class="status error">❌ Network error: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/check-env')
def check_env():
    """Check if environment variables are set"""
    env_vars = {
        'TELEGRAM_API_ID': bool(os.getenv('TELEGRAM_API_ID')),
        'TELEGRAM_API_HASH': bool(os.getenv('TELEGRAM_API_HASH')),
        'TELEGRAM_SESSION_STRING': bool(os.getenv('TELEGRAM_SESSION_STRING')),
        'PERPLEXITY_API_KEY': bool(os.getenv('PERPLEXITY_API_KEY')),
        'GOOGLE_SHEET_ID': bool(os.getenv('GOOGLE_SHEET_ID')),
        'GOOGLE_SERVICE_ACCOUNT_JSON': bool(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
    }
    
    return jsonify({
        'success': True,
        'env_vars': env_vars,
        'all_set': all(env_vars.values())
    })

@app.route('/api/test')
def test():
    """Test the scanner functionality"""
    try:
        # Test Perplexity API
        perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        if not perplexity_key:
            return jsonify({'success': False, 'error': 'PERPLEXITY_API_KEY not set'})
        
        # Simple test request to Perplexity
        headers = {
            "Authorization": f"Bearer {perplexity_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "sonar",
            "messages": [{"role": "user", "content": "Test message - respond with 'API working'"}],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'success': True,
                'message': f'Scanner is working! Perplexity API responded: {result.get("choices", [{}])[0].get("message", {}).get("content", "OK")}',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Perplexity API error: {response.status_code} - {response.text}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test failed: {str(e)}'
        })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'crypto-scanner',
        'timestamp': datetime.now().isoformat()
    })

# Vercel handler
def handler(request, response):
    """Vercel serverless handler"""
    from werkzeug.wrappers import Request, Response
    
    # Convert Vercel request to WSGI environ
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string,
        'CONTENT_TYPE': request.headers.get('content-type', ''),
        'CONTENT_LENGTH': request.headers.get('content-length', ''),
        'SERVER_NAME': request.headers.get('host', '').split(':')[0],
        'SERVER_PORT': '443',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': request.stream,
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False
    }
    
    # Add headers to environ
    for key, value in request.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Run Flask app
    response_data = []
    status = [None]
    headers = [None]
    
    def start_response(status_string, response_headers):
        status[0] = status_string
        headers[0] = response_headers
    
    app_response = app(environ, start_response)
    
    for data in app_response:
        response_data.append(data)
    
    # Set response
    response.status = int(status[0].split()[0])
    for header_name, header_value in headers[0]:
        response.headers[header_name] = header_value
    
    return b''.join(response_data)

# Export for Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True) 