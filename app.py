from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Crypto Scanner Test</title></head>
    <body>
        <h1>🚀 Crypto Projects Scanner</h1>
        <p>✅ Vercel deployment is working!</p>
        <p><a href="/test">Test API endpoint</a></p>
        <p><a href="/env">Check Environment</a></p>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return jsonify({
        'success': True,
        'message': 'Flask app is working on Vercel!',
        'status': 'OK'
    })

@app.route('/env')
def env_check():
    import os
    
    env_vars = [
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH', 
        'TELEGRAM_SESSION_STRING',
        'PERPLEXITY_API_KEY',
        'GOOGLE_SHEET_ID',
        'GOOGLE_SERVICE_ACCOUNT_JSON'
    ]
    
    result = {}
    for var in env_vars:
        result[var] = 'SET' if os.getenv(var) else 'MISSING'
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 