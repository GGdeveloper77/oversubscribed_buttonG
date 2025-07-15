# -*- coding: utf-8 -*-
"""
Crypto Projects Scanner - Vercel Compatible Version
Monitors Telegram groups and analyzes projects using Perplexity AI
"""

from flask import Flask, render_template_string, jsonify
import asyncio
import json
import os
import tempfile
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# Get credentials from environment variables (Vercel-compatible)
TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID', '28632541'))
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', 'b14125bcf447f6f91d43e0f8beea56fb')
TELEGRAM_SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING', '1ApWapzMBu0vNsZi2PE2EB5uY8_GyLAH_DmpOaNwPAwehkuefbGMLkUjy9Etm5zt3ijiPsbq9QZ-qzs7v_uF2gjibY-GBArXiZuzBW-Ob6o_QJKR_YYrBq3T3jiB_1My7LZpI3TrDPjCL5FqPjdhJsILc-B3JoA3OiMi-WJ63kGEUgpQzhS701mv5zEzw09KmY5UTp7-MAiTZTB98a1uva4mKF1Hh08N2Q0qeTbkcZlNbXMDAbUJBE2iWKlNQMeDLP-GvJeQ3cSGUxFyASRGx4Wr8HhManTjTgDqm5PAizZzURRlU-Z1AypvOdegD-ZDycbQICX-H-6N1xZV_d3Aui6cBXaSnL40=')

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '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')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4')

def get_google_service_key():
    """Get Google service account key from environment variable"""
    key_env = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    if key_env:
        try:
            return json.loads(key_env)
        except json.JSONDecodeError:
            print("❌ Invalid GOOGLE_SERVICE_ACCOUNT_JSON format")
            return None
    
    # Fallback for testing
    return {
        "type": "service_account",
        "project_id": "oversubscribed-test",
        "private_key_id": "test_key_id",
        "private_key": "-----BEGIN PRIVATE KEY-----\ntest_key\n-----END PRIVATE KEY-----\n",
        "client_email": "test@oversubscribed-test.iam.gserviceaccount.com",
        "client_id": "test_client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test%40oversubscribed-test.iam.gserviceaccount.com"
    }

# Import required modules
import gspread
from telethon import TelegramClient
import requests

def upload_to_google_sheets(project_data):
    """Upload project data to Google Sheets"""
    try:
        # Get service account key
        service_key = get_google_service_key()
        if not service_key:
            return False, "No valid Google service account key found"
        
        # Create temporary file for credentials (Vercel-compatible)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(service_key, temp_file)
            temp_creds_path = temp_file.name
        
        try:
            # Authenticate with Google Sheets
            gc = gspread.service_account(filename=temp_creds_path)
            sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
            
            # Prepare row data
            row_data = [
                project_data.get('name', ''),
                project_data.get('source_group', ''),
                project_data.get('forwarder_name', ''),
                project_data.get('blurb', ''),
                project_data.get('review', ''),
                project_data.get('date', ''),
                '',  # Comment column (empty)
                project_data.get('questions', '')
            ]
            
            # Append to sheet
            sheet.append_row(row_data)
            return True, "Successfully uploaded to Google Sheets"
            
        finally:
            # Clean up temporary file
            os.unlink(temp_creds_path)
            
    except Exception as e:
        return False, f"Google Sheets error: {str(e)}"

async def scan_telegram_groups():
    """Scan Telegram groups for crypto projects"""
    try:
        client = TelegramClient(
            'scanner_session',
            TELEGRAM_API_ID, 
            TELEGRAM_API_HASH
        )
        
        # Use session string for authentication
        await client.start(session=TELEGRAM_SESSION_STRING)
        
        target_groups = [
            "[OS] Projects",
            "Oversubscribed <> Crypbooster Deal Flow",
            "Daily Alpha • Venture, Gaming & AI",
            "🏴‍☠️ Pirate Nation - Official DAO",
            "Hacker House Paris",
            "Web3 Gaming Jobs",
            "ArkStream Capital"
        ]
        
        projects = []
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        async for dialog in client.iter_dialogs():
            if dialog.name in target_groups:
                print(f"📡 Scanning: {dialog.name}")
                
                async for message in client.iter_messages(dialog, limit=50):
                    if message.date < cutoff_time:
                        break
                    
                    if message.text and len(message.text) > 100:
                        # Extract project data
                        project = {
                            'name': extract_project_name(message.text),
                            'source_group': dialog.name,
                            'forwarder_name': get_forwarder_name(message),
                            'blurb': message.text,
                            'date': message.date.strftime('%Y-%m-%d %H:%M'),
                            'message_id': message.id
                        }
                        
                        # Analyze with Perplexity
                        analysis = await analyze_with_perplexity(project['blurb'])
                        project['review'] = analysis
                        project['questions'] = ''
                        
                        projects.append(project)
        
        await client.disconnect()
        return projects
        
    except Exception as e:
        print(f"❌ Telegram scan error: {e}")
        return []

def extract_project_name(text):
    """Extract project name from message text"""
    lines = text.split('\n')
    for line in lines[:3]:
        if any(keyword in line.lower() for keyword in ['project', 'token', 'crypto', '$']):
            return line.strip()[:50]
    return lines[0].strip()[:50] if lines else "Unknown Project"

def get_forwarder_name(message):
    """Get the name of the message forwarder or sender"""
    if message.forward and message.forward.from_id:
        return f"@{message.forward.from_id.user_id}"
    elif message.sender:
        return getattr(message.sender, 'username', None) or getattr(message.sender, 'first_name', 'Unknown')
    return "Unknown"

async def analyze_with_perplexity(text):
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
            return f"**Score: 40%**\n\n⚠️ **Analysis Error:** Could not complete AI analysis. Manual review required."
            
    except Exception as e:
        return f"**Score: 30%**\n\n⚠️ **Analysis Failed:** {str(e)}"

# Web interface HTML template
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
        .progress { margin: 20px 0; padding: 15px; background: #ecf0f1; border-radius: 5px; display: none; }
        .results { margin-top: 20px; }
        .project { margin: 15px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #fafafa; }
        .project-name { font-weight: bold; color: #2c3e50; font-size: 18px; }
        .project-details { margin: 10px 0; color: #666; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .status.info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Projects Scanner</h1>
        <p style="text-align: center; color: #666;">Monitors Telegram groups and analyzes projects with AI</p>
        
        <button class="scan-button" onclick="startScan()" id="scanBtn">
            🔍 Scan for Fresh Projects
        </button>
        
        <div class="progress" id="progress">
            <h3>🔄 Scanning in progress...</h3>
            <p id="progressText">Initializing scanner...</p>
        </div>
        
        <div class="results" id="results"></div>
    </div>

    <script>
        async function startScan() {
            const btn = document.getElementById('scanBtn');
            const progress = document.getElementById('progress');
            const results = document.getElementById('results');
            
            btn.disabled = true;
            btn.textContent = '⏳ Scanning...';
            progress.style.display = 'block';
            results.innerHTML = '';
            
            try {
                const response = await fetch('/scan');
                const data = await response.json();
                
                progress.style.display = 'none';
                btn.disabled = false;
                btn.textContent = '🔍 Scan for Fresh Projects';
                
                if (data.success) {
                    displayResults(data.projects, data.stats);
                } else {
                    results.innerHTML = `<div class="status error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                progress.style.display = 'none';
                btn.disabled = false;
                btn.textContent = '🔍 Scan for Fresh Projects';
                results.innerHTML = `<div class="status error">❌ Network error: ${error.message}</div>`;
            }
        }
        
        function displayResults(projects, stats) {
            const results = document.getElementById('results');
            
            if (projects.length === 0) {
                results.innerHTML = '<div class="status info">📭 No new projects found in the last 24 hours.</div>';
                return;
            }
            
            let html = `<div class="status success">✅ Found ${projects.length} new projects!</div>`;
            
            projects.forEach(project => {
                html += `
                    <div class="project">
                        <div class="project-name">${project.name}</div>
                        <div class="project-details">
                            <strong>Source:</strong> ${project.source_group}<br>
                            <strong>Posted by:</strong> ${project.forwarder_name}<br>
                            <strong>Date:</strong> ${project.date}
                        </div>
                        <div><strong>Analysis:</strong><br><pre style="white-space: pre-wrap; font-family: inherit;">${project.review}</pre></div>
                        <div><strong>Details:</strong><br>${project.blurb.substring(0, 300)}${project.blurb.length > 300 ? '...' : ''}</div>
                    </div>
                `;
            });
            
            results.innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan')
def scan():
    """API endpoint to start scanning"""
    try:
        # Run async scan in thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        projects = loop.run_until_complete(scan_telegram_groups())
        loop.close()
        
        # Upload to Google Sheets
        uploaded_count = 0
        for project in projects:
            success, message = upload_to_google_sheets(project)
            if success:
                uploaded_count += 1
        
        return jsonify({
            'success': True,
            'projects': projects,
            'stats': {
                'total_found': len(projects),
                'uploaded_to_sheets': uploaded_count
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'crypto-scanner'})

# Vercel-compatible export
def handler(request):
    """Vercel handler function"""
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    print("🚀 Starting Crypto Projects Scanner...")
    print("📱 Telegram API configured")
    print("🤖 Perplexity AI ready")
    print("📊 Google Sheets integration active")
    print("🌐 Web interface: http://localhost:5000")
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=False) 