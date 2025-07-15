# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Fresh Crypto Projects Scanner
One-click web interface to find only NEW crypto projects (auto-filters duplicates)
"""

from flask import Flask, render_template_string, jsonify
import asyncio
import json
import os
import tempfile
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# Your working credentials
TELEGRAM_API_ID = 28632541
TELEGRAM_API_HASH = "b14125bcf447f6f91d43e0f8beea56fb"
TELEGRAM_SESSION_STRING = "1ApWapzMBu0vNsZi2PE2EB5uY8_GyLAH_DmpOaNwPAwehkuefbGMLkUjy9Etm5zt3ijiPsbq9QZ-qzs7v_uF2gjibY-GBArXiZuzBW-Ob6o_QJKR_YYrBq3T3jiB_1My7LZpI3TrDPjCL5FqPjdhJsILc-B3JoA3OiMi-WJ63kGEUgpQzhS701mv5zEzw09KmY5UTp7-MAiTZTB98a1uva4mKF1Hh08N2Q0qeTbkcZlNbXMDAbUJBE2iWKlNQMeDLP-GvJeQ3cSGUxFyASRGx4Wr8HhManTjTgDqm5PAizZzURRlU-Z1AypvOdegD-ZDycbQICX-H-6N1xZV_d3Aui6cBXaSnL40="

PERPLEXITY_API_KEY = "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"
GOOGLE_SHEET_ID = "1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4"

# Google service account key - load from file or environment
def get_google_service_key():
    """Get Google service account key from file or environment variable"""
    
    # Option 1: Try to load from JSON file
    key_file = "google_service_key.json"
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return json.load(f)
    
    # Option 2: Try environment variable
    key_env = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY')
    if key_env:
        return json.loads(key_env)
    
    # Option 3: Fallback dummy key for testing
    return {
        "type": "service_account",
        "project_id": "oversubscribed",
        "private_key_id": "dummy_key_id",
        "private_key": "dummy_private_key",
        "client_email": "crypto-sheet-writer@oversubscribed.iam.gserviceaccount.com",
        "client_id": "dummy_client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/crypto-sheet-writer%40oversubscribed.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

GOOGLE_SERVICE_ACCOUNT_KEY = get_google_service_key()

def test_google_sheets_connection():
    """Test if Google Sheets connection is properly configured"""
    if GOOGLE_SERVICE_ACCOUNT_KEY.get('private_key') == 'dummy_private_key':
        return False, "No valid service account key found"
    
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        print(f"🔍 Testing connection to sheet: {GOOGLE_SHEET_ID}")
        print(f"📧 Service account: {GOOGLE_SERVICE_ACCOUNT_KEY.get('client_email')}")
        
        # Try multiple connection methods
        gc = None
        
        # Method 1: Direct file path
        try:
            if os.path.exists('google_service_key.json'):
                gc = gspread.service_account(filename='google_service_key.json')
                print("✅ Connected using direct file method")
        except Exception as e:
            print(f"🔹 Direct file method failed: {e}")
        
        # Method 2: Credentials object
        if not gc:
            try:
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                credentials = Credentials.from_service_account_info(GOOGLE_SERVICE_ACCOUNT_KEY, scopes=scopes)
                gc = gspread.authorize(credentials)
                print("✅ Connected using credentials object method")
            except Exception as e:
                print(f"🔹 Credentials object method failed: {e}")
        
        if not gc:
            return False, "All connection methods failed"
        
        print("📊 Opening Google Sheet...")
        sheet = gc.open_by_key(GOOGLE_SHEET_ID)
        
        print("📋 Getting worksheet...")
        worksheet = sheet.sheet1
        
        print("✅ Testing read access...")
        # Try to read a small range
        try:
            cell_range = worksheet.get('A1:B2')
            print(f"📖 Successfully read range: {len(cell_range)} rows")
        except Exception as read_error:
            print(f"⚠️  Read test failed: {read_error}")
        
        return True, "Google Sheets connection successful"
        
    except gspread.exceptions.APIError as api_error:
        print(f"❌ Google API Error: {api_error}")
        if "PERMISSION_DENIED" in str(api_error):
            return False, "Sheet not shared with service account or wrong permissions"
        elif "API_NOT_ENABLED" in str(api_error):
            return False, "Google Sheets API not enabled in Google Cloud Console"
        else:
            return False, f"Google API Error: {api_error}"
    except gspread.exceptions.SpreadsheetNotFound:
        return False, "Google Sheet not found - check Sheet ID"
    except FileNotFoundError:
        return False, "Service account key file error"
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return False, f"Connection error: {type(e).__name__}: {e}"

TARGET_GROUPS = [
    "[OS] Projects",
    "Oversubscribed <> Crypbooster Deal Flow", 
    "Oversubscribed Capital + Platinum VC",
    "(Deal Flow) Oversubscribed Capital < > Listara",
    "[VC3] Daniil Angel 🟢 CE/DaoFund🔆",
    "DealFlow🤝: OS ↔️ SeaFi",
    "Crypto Executives Deal Flow Channel"
]

# Global scan status
scan_status = {
    "running": False,
    "last_scan": None,
    "last_results": None,
    "progress": "Ready to scan"
}

async def analyze_with_perplexity(text):
    """Analyze message with Perplexity AI"""
    try:
        import openai
        
        client = openai.AsyncClient(
            api_key=PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai"
        )
        
        prompt = f"""
        You are a CRITICAL crypto investment analyst. Analyze this Telegram message about a crypto project:
        
        "{text}"
        
        ONLY respond with valid JSON. If this is NOT about a crypto project (just general chat, news articles, or unrelated content), respond: {{"is_crypto_project": false}}
        
        If this IS about a legitimate crypto project, respond with:
        {{
            "is_crypto_project": true,
            "confidence_score": [0-100],
            "project_name": "exact project name",
            "detailed_analysis": "Format your analysis EXACTLY like this structure with emojis and sections:\n\n✅ Pros:\n[List 2-4 positive aspects with bullet points]\n\n⚠️ Risks / Red Flags:\n[List 2-4 concerning aspects with bullet points]\n\n🔎 What Are These Guys Doing?\n[Explain in 2-3 sentences what the project is actually building, their business model, and their strategy. Be specific about their approach.]"
        }}
        
        SCORING GUIDELINES:
        - 90-100%: Exceptional projects with proven teams, clear utility, strong tokenomics, and realistic goals
        - 70-89%: Good projects with some strengths but notable concerns or risks
        - 50-69%: Average projects with significant concerns or unproven elements  
        - 30-49%: Poor projects with major red flags or unrealistic claims
        - 0-29%: Scams, obvious failures, or projects with critical flaws
        
        BE CRITICAL and BALANCED. Show both positives and negatives. Most crypto projects fail - be skeptical but fair."""

        response = await client.chat.completions.create(
            model="sonar",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        content = response.choices[0].message.content.strip()
        print(f"📝 Perplexity raw response: {content}")
        
        if not content:
            print("❌ Empty response from Perplexity")
            return None
            
        # Try to extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Raw content: {content}")
        return None
    except Exception as e:
        print(f"❌ Perplexity analysis error: {e}")
        return None

async def get_existing_projects():
    """Get existing projects from Google Sheets to avoid duplicates"""
    
    # Check if we have a valid service account key
    if GOOGLE_SERVICE_ACCOUNT_KEY.get('private_key') == 'dummy_private_key':
        print("⚠️  No valid Google service account key found")
        print("💡 To connect to Google Sheets, create 'google_service_key.json' file")
        print("📋 Using empty set for duplicate check (will save locally)")
        return set()
    
    try:
        import gspread
        
        print("📊 Connecting to Google Sheets...")
        
        # Write to temporary file for gspread
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(GOOGLE_SERVICE_ACCOUNT_KEY, temp_file)
            temp_path = temp_file.name
        
        # Initialize Google Sheets client
        gc = gspread.service_account(filename=temp_path)
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Get all existing data
        try:
            all_records = sheet.get_all_records()
            existing_projects = set()
            
            for record in all_records:
                project_name = record.get('Name', '').strip().lower()
                if project_name:
                    existing_projects.add(project_name)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            print(f"📋 Found {len(existing_projects)} existing projects in sheet")
            return existing_projects
            
        except Exception as e:
            print(f"📋 No existing data found (empty sheet): {e}")
            os.unlink(temp_path)
            return set()
        
    except Exception as e:
        print(f"❌ Google Sheets connection error: {e}")
        print("⚠️  Using empty set for duplicate check")
        return set()

def is_duplicate_project(project_name, existing_projects):
    """Check if project already exists in sheet"""
    clean_name = project_name.strip().lower()
    
    # Check exact match
    if clean_name in existing_projects:
        return True
    
    # Check similar names (80% similarity)
    for existing in existing_projects:
        # Simple similarity check
        if clean_name in existing or existing in clean_name:
            return True
            
        # Check if names are very similar (token matching)
        existing_tokens = set(existing.split())
        new_tokens = set(clean_name.split())
        
        if len(existing_tokens) > 0 and len(new_tokens) > 0:
            intersection = existing_tokens.intersection(new_tokens)
            similarity = len(intersection) / max(len(existing_tokens), len(new_tokens))
            if similarity > 0.8:  # 80% token similarity
                return True
    
    return False

def simple_crypto_analysis(text):
    """Simple fallback analysis when Perplexity fails - INCLUSIVE project detection"""
    text_lower = text.lower()
    
    # Look for crypto project indicators (more inclusive)
    crypto_indicators = [
        # Token-related terms
        'token', 'tokenomics', 'coin', '$', 'presale', 'ico', 'ido', 'airdrop',
        # Project terms
        'blockchain', 'defi', 'nft', 'dao', 'dapp', 'web3', 'crypto', 'protocol',
        # Business terms
        'whitepaper', 'roadmap', 'funding', 'investment', 'backed by', 'investors',
        'team', 'ceo', 'founder', 'startup', 'venture', 'seed round', 'series',
        # Technology terms
        'smart contract', 'ethereum', 'polygon', 'solana', 'binance', 'trading',
        # Marketing terms
        'launch', 'platform', 'ecosystem', 'community', 'governance'
    ]
    
    # Advanced project description indicators
    advanced_indicators = [
        'decentralized', 'trustless', 'proof of', 'consensus', 'mining', 'staking',
        'yield farming', 'liquidity', 'market cap', 'total supply', 'circulation',
        'utility', 'governance', 'rewards', 'incentive', 'burn mechanism'
    ]
    
    # Exclude obvious non-projects
    exclusion_patterns = [
        'just saw', 'what do you think', 'anyone know', 'quick question',
        'btw', 'by the way', 'off topic', 'random question'
    ]
    
    # Check for exclusions first
    exclusion_score = sum(1 for pattern in exclusion_patterns if pattern in text_lower)
    if exclusion_score > 0:
        return None  # Skip obvious casual chat
    
    # Count crypto indicators
    crypto_score = sum(1 for indicator in crypto_indicators if indicator in text_lower)
    advanced_score = sum(1 for indicator in advanced_indicators if indicator in text_lower)
    
    # More lenient scoring - if it mentions crypto terms, it's likely a project
    total_score = crypto_score + (advanced_score * 2)
    
    if total_score >= 3:  # Much lower threshold
        # Try to extract project name
        words = text.split()
        project_name = "Unknown Project"
        
        # Look for token symbols ($TOKEN) or project names in caps
        for word in words:
            if word.startswith('$') and len(word) > 2:
                project_name = word[1:]  # Remove $
                break
            elif word.isupper() and len(word) > 2 and len(word) < 15:
                project_name = word
                break
        
        # If no clear name found, take first significant word
        if project_name == "Unknown Project":
            for word in words:
                clean_word = word.strip('.,!?:()[]{}').title()
                if len(clean_word) > 3 and clean_word.lower() not in ['the', 'and', 'with', 'this', 'that', 'have', 'been', 'from']:
                    project_name = clean_word
                    break
        
        confidence = min(60, 20 + (total_score * 5))  # More conservative scoring
        
        return {
            "is_crypto_project": True,
            "confidence_score": confidence,
            "project_name": project_name,
            "detailed_analysis": f"""✅ Pros:
• Detected {crypto_score} crypto indicators suggesting legitimate project discussion
• Contains {advanced_score} advanced blockchain features/terminology
• Structured presentation indicates organized development effort

⚠️ Risks / Red Flags:
• FALLBACK ANALYSIS - limited information available for thorough evaluation
• Team credentials and background cannot be verified from this message
• Tokenomics structure and viability assessment incomplete
• Market competition and differentiation factors unclear

🔎 What Are These Guys Doing?
Based on message analysis, this appears to be a crypto project with {confidence}% confidence score. The project mentions blockchain/crypto elements but requires deeper due diligence to assess the actual business model, team qualifications, and technical implementation. Consider this a preliminary flag for further investigation."""
        }
    
    return None  # Not enough crypto indicators

async def upload_to_google_sheets(projects):
    """Upload projects to Google Sheets with duplicate detection and correct column mapping"""
    try:
        import gspread  # Import here to avoid module errors
        from google.oauth2.service_account import Credentials
        
        print("📊 Connecting to Google Sheets...")
        
        # Try multiple connection methods to resolve "No key could be detected" error
        gc = None
        
        # Method 1: Direct file path (most reliable)
        try:
            if os.path.exists('google_service_key.json'):
                gc = gspread.service_account(filename='google_service_key.json')
                print("✅ Connected using direct file method")
        except Exception as e:
            print(f"🔹 Direct file method failed: {e}")
        
        # Method 2: Credentials object with explicit scopes
        if not gc:
            try:
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                credentials = Credentials.from_service_account_info(GOOGLE_SERVICE_ACCOUNT_KEY, scopes=scopes)
                gc = gspread.authorize(credentials)
                print("✅ Connected using credentials object method")
            except Exception as e:
                print(f"🔹 Credentials object method failed: {e}")
        
        # Method 3: Temporary file fallback
        if not gc:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as temp_file:
                json.dump(GOOGLE_SERVICE_ACCOUNT_KEY, temp_file)
                temp_path = temp_file.name
            
            try:
                gc = gspread.service_account(filename=temp_path)
                print("✅ Connected using temporary file method")
            finally:
                os.unlink(temp_path)  # Clean up
        
        if not gc:
            raise Exception("All connection methods failed")
        
        # Initialize Google Sheets client
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Set up headers first (always ensure proper headers)
        expected_headers = ["Name", "Referred by", "TG account", "Blurb", "Review", "Date", "Comment", "Questions"]
        try:
            # Check if sheet has any data
            all_values = sheet.get_all_values()
            
            if not all_values or len(all_values) == 0:
                # Completely empty sheet - add headers
                print("📝 Setting up headers for empty sheet...")
                sheet.update('A1:H1', [expected_headers])
            else:
                # Check if first row has correct headers
                headers = sheet.row_values(1) if len(all_values) > 0 else []
                
                # Pad headers to match expected length and clean them
                padded_headers = (headers + [''] * 8)[:8]  # Ensure exactly 8 columns
                
                if padded_headers != expected_headers:
                    print("📝 Updating headers to match expected format...")
                    sheet.update('A1:H1', [expected_headers])
                    
        except Exception as header_error:
            print(f"⚠️ Header setup failed: {header_error}")
            # Try to clear and reset headers
            sheet.clear()
            sheet.update('A1:H1', [expected_headers])
            print("📝 Reset sheet with proper headers")
        
        # Get existing project names from column A for duplicate detection
        existing_names = []
        try:
            existing_data = sheet.col_values(1)  # Column A (Name column)
            if len(existing_data) > 1:  # More than just header
                existing_names = [name.strip().lower() for name in existing_data[1:] if name.strip()]  # Skip header, normalize case
                print(f"📋 Found {len(existing_names)} existing projects for duplicate check")
            else:
                print("📋 No existing data found (fresh sheet)")
        except Exception as e:
            print(f"⚠️ Could not read existing projects: {e}")
        
        # Upload to Google Sheets (write to specific columns A-H)
        uploaded_count = 0
        duplicate_count = 0
        
        for project in projects:
            try:
                project_name = project.get('project_name', 'Unknown').strip()
                
                # Check for duplicates in column A
                if project_name.lower() in existing_names:
                    duplicate_count += 1
                    print(f"⚠️ Skipping duplicate: {project_name}")
                    continue
                
                # Generate questions for the project
                questions_list = [
                    "What are your current traction metrics?",
                    "How do you differentiate from competitors?", 
                    "What milestones will funding achieve?",
                    "What's your path to revenue?",
                    "What are the main risks?"
                ]
                questions_text = " | ".join(questions_list)
                
                # Prepare row data with CORRECT column mapping
                row_data = [
                    project_name,  # Name (Column A)
                    project.get('source_group', 'Unknown'),  # Referred by (Column B)
                    project.get('forwarder_info', 'Unknown'),  # TG account (Column C) - FORWARDER/SENDER INFO
                    project.get('original_message', ''),  # Blurb - FULL message content (Column D)
                    f"Score: {project.get('confidence_score', 0)}% | {project.get('detailed_analysis', 'AI analysis pending')}",  # Review (Column E) - DETAILED ANALYSIS HERE
                    project.get('message_date', datetime.now().strftime("%Y-%m-%d")),  # Date (Column F)
                    "",  # Comment (Column G) - EMPTY per user request
                    questions_text  # Questions (Column H) - properly populated
                ]
                
                # Find the next empty row and write to specific range A-H
                all_values = sheet.get_all_values()
                next_row = len(all_values) + 1
                range_name = f'A{next_row}:H{next_row}'
                
                # Write to specific columns A-H
                sheet.update(range_name, [row_data])
                
                # Add to existing names to prevent duplicates in same batch
                existing_names.append(project_name.lower())
                
                uploaded_count += 1
                print(f"✅ Uploaded project {uploaded_count}: {project_name} to row {next_row}")
                
            except Exception as e:
                print(f"❌ Failed to upload project: {e}")
                continue
        
        print(f"📊 Upload complete: {uploaded_count} new projects, {duplicate_count} duplicates skipped")
        return uploaded_count
        
    except Exception as e:
        error_msg = f"Google Sheets upload error: {e}"
        print(f"❌ {error_msg}")
        print("💾 Saving to local backup file instead...")
        save_to_backup_file(projects)
        return 0

def save_to_backup_file(projects):
    """Save projects to local backup JSON file"""
    try:
        backup_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "projects": projects
        }
        
        # Load existing backup data
        backup_file = "crypto_projects_backup.json"
        existing_data = []
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.append(backup_data)
        
        # Save updated data
        with open(backup_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        print(f"💾 Saved {len(projects)} projects to {backup_file}")
        return len(projects)
        
    except Exception as backup_error:
        print(f"❌ Backup save error: {backup_error}")
        return 0

async def run_daily_scan():
    """Run the daily crypto scan with Google Sheets upload"""
    global scan_status
    
    scan_status["running"] = True
    scan_status["progress"] = "Connecting to Telegram..."
    
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        
        # Initialize Telegram client
        session = StringSession(TELEGRAM_SESSION_STRING)
        client = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)
        await client.start()
        
        scan_status["progress"] = "Scanning groups..."
        
        found_projects = []
        messages_scanned = 0
        
        # Scan target groups for messages from last 24 hours
        from datetime import timezone
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                if dialog.title in TARGET_GROUPS:
                    scan_status["progress"] = f"Scanning: {dialog.title}"
                    print(f"🔍 Scanning group: {dialog.title}")
                    
                    group_messages = 0
                    async for message in client.iter_messages(dialog.entity, limit=100):
                        if message.date < cutoff_time:
                            break
                            
                        group_messages += 1
                        if message.text and len(message.text) > 30:
                            messages_scanned += 1
                            scan_status["progress"] = f"Analyzing message {messages_scanned} from {dialog.title}..."
                            
                            print(f"📝 Message {messages_scanned}: {message.text[:100]}...")
                            
                            # Get forwarding information
                            forwarder_info = "Unknown"
                            if message.forward:
                                if message.forward.from_id:
                                    try:
                                        # Get the user who forwarded the message
                                        forwarder = await client.get_entity(message.forward.from_id)
                                        if hasattr(forwarder, 'username') and forwarder.username:
                                            forwarder_info = f"@{forwarder.username}"
                                        elif hasattr(forwarder, 'first_name'):
                                            forwarder_info = forwarder.first_name
                                            if hasattr(forwarder, 'last_name') and forwarder.last_name:
                                                forwarder_info += f" {forwarder.last_name}"
                                    except Exception as e:
                                        print(f"⚠️ Could not get forwarder info: {e}")
                                        forwarder_info = "Private User"
                            else:
                                # Not a forwarded message, get original sender
                                try:
                                    sender = await message.get_sender()
                                    if sender and hasattr(sender, 'username') and sender.username:
                                        forwarder_info = f"@{sender.username}"
                                    elif sender and hasattr(sender, 'first_name'):
                                        forwarder_info = sender.first_name
                                        if hasattr(sender, 'last_name') and sender.last_name:
                                            forwarder_info += f" {sender.last_name}"
                                except Exception as e:
                                    print(f"⚠️ Could not get sender info: {e}")
                                    forwarder_info = "Unknown User"
                            
                            # Analyze with Perplexity
                            analysis = await analyze_with_perplexity(message.text)
                            
                            # Fallback simple analysis if Perplexity fails
                            if not analysis:
                                analysis = simple_crypto_analysis(message.text)
                            
                            if analysis and analysis.get('is_crypto_project') and analysis.get('confidence_score', 0) > 15:
                                print(f"✨ Found crypto project: {analysis.get('project_name')} (Score: {analysis.get('confidence_score')})")
                                project = {
                                    'project_name': analysis.get('project_name', 'Unknown'),
                                    'confidence_score': analysis.get('confidence_score', 0),
                                    'detailed_analysis': analysis.get('detailed_analysis', ''),
                                    'source_group': dialog.title,
                                    'forwarder_info': forwarder_info,  # NEW: Telegram account who forwarded/sent
                                    'message_date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                                    'original_message': message.text.strip()
                                }
                                found_projects.append(project)
                    
                    print(f"📊 Group {dialog.title}: {group_messages} total messages, {len([m for m in found_projects if m['source_group'] == dialog.title])} projects found")
        
        await client.disconnect()
        
        # Filter out duplicates
        scan_status["progress"] = "Checking for duplicates in Google Sheets..."
        existing_projects = await get_existing_projects()
        filtered_projects = []
        
        for project in found_projects:
            if not is_duplicate_project(project['project_name'], existing_projects):
                filtered_projects.append(project)
            else:
                print(f"🔄 Duplicate filtered: {project['project_name']}")
        
        print(f"✅ Filtered {len(found_projects) - len(filtered_projects)} duplicates, {len(filtered_projects)} fresh projects remain")
        
        # Upload to Google Sheets
        uploaded_count = 0
        if filtered_projects:
            scan_status["progress"] = "Uploading projects..."
            uploaded_count = await upload_to_google_sheets(filtered_projects)
        else:
            print("🔍 No new projects found to upload")
        
        # Save results
        scan_status["last_scan"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        scan_status["last_results"] = {
            "projects_found": len(found_projects),
            "duplicate_projects": len(found_projects) - len(filtered_projects),
            "fresh_projects": len(filtered_projects),
            "projects_uploaded": uploaded_count,
            "messages_scanned": messages_scanned,
            "projects": filtered_projects
        }
        
        duplicates_filtered = len(found_projects) - len(filtered_projects)
        scan_status["progress"] = f"Complete! Found {len(found_projects)} total, {duplicates_filtered} duplicates filtered, {uploaded_count} fresh projects added ✅"
        
        return scan_status["last_results"]
        
    except Exception as e:
        scan_status["progress"] = f"Error: {str(e)}"
        return {"error": str(e)}
        
    finally:
        scan_status["running"] = False

# Web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fresh Crypto Projects Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .scan-button { background: #3498db; color: white; padding: 15px 30px; font-size: 18px; border: none; border-radius: 5px; cursor: pointer; display: block; margin: 20px auto; }
        .scan-button:hover { background: #2980b9; }
        .scan-button:disabled { background: #bdc3c7; cursor: not-allowed; }
        .status { margin: 20px 0; padding: 15px; border-radius: 5px; }
        .status.running { background: #e8f4f8; border: 1px solid #3498db; }
        .status.complete { background: #d5f4e6; border: 1px solid #27ae60; }
        .results { margin-top: 20px; }
        .project { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
        .project-name { font-weight: bold; color: #2c3e50; }
        .project-details { margin-top: 10px; font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Fresh Crypto Projects Scanner</h1>
        <p style="text-align: center; color: #666;">
            Find NEW crypto projects from your 7 Telegram groups<br>
            🔍 Auto-filters duplicates • ✨ Only adds fresh projects • 📊 Uploads to Google Sheets
        </p>
        
        <button id="scanBtn" class="scan-button" onclick="startScan()">✨ Find Fresh Projects</button>
        
        <div style="text-align: center; margin: 20px 0;">
            <button onclick="testSheets()" style="background: #95a5a6; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">
                🔗 Test Google Sheets Connection
            </button>
            <button onclick="clearSheet()" style="background: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">
                🗑️ Clear & Reset Sheet
            </button>
        </div>
        
        <div id="sheets-status" style="display: none; margin: 20px 0; padding: 15px; border-radius: 5px;"></div>
        <div id="status" style="display: none;"></div>
        <div id="results"></div>
    </div>

    <script>
        let scanInterval;
        
        function startScan() {
            document.getElementById('scanBtn').disabled = true;
            document.getElementById('scanBtn').textContent = '⏳ Finding fresh projects...';
            
            fetch('/scan', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        checkStatus();
                    } else {
                        showError(data.error);
                    }
                });
        }
        
        function checkStatus() {
            scanInterval = setInterval(() => {
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {
                        updateStatus(data);
                        if (!data.running) {
                            clearInterval(scanInterval);
                            document.getElementById('scanBtn').disabled = false;
                            document.getElementById('scanBtn').textContent = '✨ Find Fresh Projects';
                            if (data.last_results) {
                                showResults(data.last_results);
                            }
                        }
                    });
            }, 2000);
        }
        
        function updateStatus(data) {
            const status = document.getElementById('status');
            status.style.display = 'block';
            status.className = 'status ' + (data.running ? 'running' : 'complete');
            status.innerHTML = `
                <strong>Status:</strong> ${data.progress}<br>
                ${data.last_scan ? `<strong>Last scan:</strong> ${data.last_scan}` : ''}
            `;
        }
        
        function showResults(results) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <h3>📊 Scan Results</h3>
                <p><strong>Total projects found:</strong> ${results.projects_found}</p>
                <p><strong>🔄 Duplicates filtered:</strong> ${results.duplicate_projects || 0}</p>
                <p><strong>✨ Fresh projects:</strong> ${results.fresh_projects || results.projects_found}</p>
                <p><strong>📤 Uploaded to Google Sheets:</strong> ${results.projects_uploaded}</p>
                <p><strong>💬 Messages scanned:</strong> ${results.messages_scanned}</p>
                
                ${results.projects && results.projects.length > 0 ? `
                    <h4>Found Projects:</h4>
                    ${results.projects.map(project => `
                        <div class="project">
                            <div class="project-name">${project.project_name}</div>
                            <div class="project-details">
                                <strong>Score:</strong> ${project.confidence_score}/100 • 
                                <strong>Group:</strong> ${project.source_group}<br>
                                <strong>Analysis:</strong> ${project.detailed_analysis}
                            </div>
                        </div>
                    `).join('')}
                ` : ''}
            `;
        }
        
        function showError(error) {
            const status = document.getElementById('status');
            status.style.display = 'block';
            status.className = 'status';
            status.style.background = '#f8d7da';
            status.style.border = '1px solid #dc3545';
            status.innerHTML = `<strong>Error:</strong> ${error}`;
            document.getElementById('scanBtn').disabled = false;
            document.getElementById('scanBtn').textContent = '✨ Find Fresh Projects';
        }
        
        function testSheets() {
            const sheetsStatus = document.getElementById('sheets-status');
            sheetsStatus.style.display = 'block';
            sheetsStatus.innerHTML = '🔄 Testing Google Sheets connection...';
            sheetsStatus.style.background = '#e8f4f8';
            sheetsStatus.style.border = '1px solid #3498db';
            
            fetch('/test-sheets')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        sheetsStatus.innerHTML = `✅ <strong>Google Sheets Connected!</strong><br>Sheet ID: ${data.sheet_id}`;
                        sheetsStatus.style.background = '#d5f4e6';
                        sheetsStatus.style.border = '1px solid #27ae60';
                    } else {
                        sheetsStatus.innerHTML = `❌ <strong>Google Sheets Not Connected</strong><br>${data.message}<br><small>Projects will be saved to local backup file</small>`;
                        sheetsStatus.style.background = '#f8d7da';
                        sheetsStatus.style.border = '1px solid #dc3545';
                    }
                })
                .catch(error => {
                    sheetsStatus.innerHTML = `❌ <strong>Connection Test Failed:</strong> ${error}`;
                    sheetsStatus.style.background = '#f8d7da';
                    sheetsStatus.style.border = '1px solid #dc3545';
                });
        }
        
        function clearSheet() {
            if (!confirm('This will clear ALL data in the Google Sheet and reset headers. Are you sure?')) {
                return;
            }
            
            const sheetsStatus = document.getElementById('sheets-status');
            sheetsStatus.style.display = 'block';
            sheetsStatus.innerHTML = '🗑️ Clearing Google Sheets and resetting headers...';
            sheetsStatus.style.background = '#fff3cd';
            sheetsStatus.style.border = '1px solid #ffc107';
            
            fetch('/clear-sheet', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        sheetsStatus.innerHTML = `✅ <strong>Sheet Cleared & Reset!</strong><br>${data.message}<br>Ready for fresh data upload.`;
                        sheetsStatus.style.background = '#d5f4e6';
                        sheetsStatus.style.border = '1px solid #27ae60';
                    } else {
                        sheetsStatus.innerHTML = `❌ <strong>Clear Failed:</strong> ${data.error}`;
                        sheetsStatus.style.background = '#f8d7da';
                        sheetsStatus.style.border = '1px solid #dc3545';
                    }
                })
                .catch(error => {
                    sheetsStatus.innerHTML = `❌ <strong>Clear Failed:</strong> ${error}`;
                    sheetsStatus.style.background = '#f8d7da';
                    sheetsStatus.style.border = '1px solid #dc3545';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/scan', methods=['POST'])
def start_scan():
    if scan_status["running"]:
        return jsonify({"success": False, "error": "Scan already running"})
    
    # Start scan in background
    def run_scan():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_daily_scan())
    
    threading.Thread(target=run_scan, daemon=True).start()
    return jsonify({"success": True})

@app.route('/status')
def get_status():
    return jsonify(scan_status)

@app.route('/test-sheets')
def test_sheets():
    success, message = test_google_sheets_connection()
    return jsonify({
        "success": success,
        "message": message,
        "sheet_id": GOOGLE_SHEET_ID
    })

@app.route('/clear-sheet', methods=['POST'])
def clear_sheet():
    """Clear the Google Sheets and reset headers"""
    try:
        import gspread
        
        # Write to temporary file for gspread
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(GOOGLE_SERVICE_ACCOUNT_KEY, temp_file)
            temp_path = temp_file.name
        
        # Initialize Google Sheets client
        gc = gspread.service_account(filename=temp_path)
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Clear all data
        sheet.clear()
        
        # Add proper headers starting from A1
        header_row = [
            "Name",
            "Referred by", 
            "TG account",
            "Blurb",
            "Review",
            "Date",
            "Comment",
            "Questions"
        ]
        sheet.update('A1:H1', [header_row])
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return jsonify({
            "success": True,
            "message": "Sheet cleared and headers reset in columns A-H"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    print("🚀 Starting Fresh Crypto Projects Scanner")
    print("📱 Open http://localhost:5000 in your browser")
    print("✨ Click 'Find Fresh Projects' to discover only NEW projects (duplicates auto-filtered)")
    
    # Check Google Sheets connection
    sheets_success, sheets_message = test_google_sheets_connection()
    if sheets_success:
        print("✅ Google Sheets: Connected and ready")
    else:
        print(f"⚠️  Google Sheets: {sheets_message}")
        print("💾 Projects will be saved to local backup file")
        print("📋 See GOOGLE_SHEETS_SETUP_FIXED.md for setup instructions")
    
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=True) 