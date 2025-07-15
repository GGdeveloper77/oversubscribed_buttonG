from flask import Flask, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

# Get environment variables
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '')

# HTML Template for testing
HTML_TEMPLATE = '''
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
        .test-button { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; display: block; margin: 20px auto; }
        .test-button:hover { background: #2980b9; }
        .test-button:disabled { background: #bdc3c7; cursor: not-allowed; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .status.info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .env-check { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .env-item { margin: 5px 0; }
        .env-ok { color: #28a745; }
        .env-missing { color: #dc3545; }
        .analysis-result { margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Projects Scanner</h1>
        <p style="text-align: center; color: #666;">Testing Perplexity AI Integration</p>
        
        <div class="env-check">
            <h3>📋 Configuration Status:</h3>
            <div id="envStatus">Loading...</div>
        </div>
        
        <button class="test-button" onclick="testPerplexity()" id="testBtn">
            🤖 Test Perplexity AI Analysis
        </button>
        
        <div id="results"></div>
    </div>

    <script>
        // Check environment variables on page load
        fetch('/env')
            .then(response => response.json())
            .then(data => {
                const envStatus = document.getElementById('envStatus');
                let html = '';
                
                Object.entries(data).forEach(([key, status]) => {
                    const statusClass = status === 'SET' ? 'env-ok' : 'env-missing';
                    const statusIcon = status === 'SET' ? '✅' : '❌';
                    html += `<div class="env-item ${statusClass}">${statusIcon} ${key}: ${status}</div>`;
                });
                
                envStatus.innerHTML = html;
            })
            .catch(error => {
                document.getElementById('envStatus').innerHTML = '<div class="env-missing">❌ Error checking environment</div>';
            });
        
        async function testPerplexity() {
            const btn = document.getElementById('testBtn');
            const results = document.getElementById('results');
            
            btn.disabled = true;
            btn.textContent = '⏳ Testing Perplexity...';
            results.innerHTML = '<div class="status info">🔄 Analyzing a sample crypto project...</div>';
            
            try {
                const response = await fetch('/test-perplexity');
                const data = await response.json();
                
                btn.disabled = false;
                btn.textContent = '🤖 Test Perplexity AI Analysis';
                
                if (data.success) {
                    results.innerHTML = `
                        <div class="status success">✅ Perplexity AI is working!</div>
                        <div class="analysis-result">
                            <h4>🤖 Sample Analysis Result:</h4>
                            <pre style="white-space: pre-wrap; font-family: inherit;">${data.analysis}</pre>
                        </div>
                    `;
                } else {
                    results.innerHTML = `<div class="status error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                btn.disabled = false;
                btn.textContent = '🤖 Test Perplexity AI Analysis';
                results.innerHTML = `<div class="status error">❌ Network error: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
'''

def analyze_with_perplexity(text):
    """Analyze project text using Perplexity AI"""
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        You are a CRITICAL crypto investment analyst. Analyze this crypto project announcement with EXTREME SKEPTICISM.

        Project Details: {text[:1000]}

        Provide a rigorous analysis in this EXACT format:

        **Score: X%** (Use this scoring guide:
        - 90-100%: Exceptional projects with verified teams, clear use cases, strong backing
        - 70-89%: Good projects but with some concerns or risks
        - 50-69%: Average projects with significant risks
        - 30-49%: Poor projects with major red flags
        - 0-29%: Likely scams or extremely high-risk)

        ✅ **Pros:**
        - List legitimate strengths (be very conservative)

        ⚠️ **Risks/Red Flags:**
        - List all concerns, warning signs, and potential issues

        🔎 **What Are These Guys Doing:**
        - Brief explanation of their actual business model/product

        Be HARSH and REALISTIC. Most crypto projects fail or are scams. Don't give high scores easily.
        """
        
        data = {
            "model": "sonar",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 800
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"**Score: 40%**\n\n⚠️ **Analysis Error:** Could not complete AI analysis. Status: {response.status_code}"
            
    except Exception as e:
        return f"**Score: 30%**\n\n⚠️ **Analysis Failed:** {str(e)}"

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/test')
def test():
    return jsonify({
        'success': True,
        'message': 'Flask app is working on Vercel!',
        'status': 'OK'
    })

@app.route('/env')
def env_check():
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

@app.route('/test-perplexity')
def test_perplexity():
    """Test Perplexity AI with a sample crypto project"""
    if not PERPLEXITY_API_KEY:
        return jsonify({
            'success': False,
            'error': 'PERPLEXITY_API_KEY not configured'
        })
    
    # Sample crypto project text for testing
    sample_text = """
    🚀 INTRODUCING CRYPTOMAX 🚀
    
    Revolutionary DeFi protocol that will change everything!
    
    ✅ 10,000% APY guaranteed
    ✅ Celebrity endorsements 
    ✅ Quantum blockchain technology
    ✅ No risk, all rewards!
    
    Presale starting now - only 24 hours left!
    Join our Telegram for exclusive bonuses!
    """
    
    try:
        # Test Perplexity analysis
        analysis = analyze_with_perplexity(sample_text)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'sample_text': sample_text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 