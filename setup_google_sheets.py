#!/usr/bin/env python3
"""
Google Sheets Setup Helper
Run this to configure Google Sheets integration for the crypto scanner
"""

import json
import os

def create_google_service_account():
    """Guide user through creating Google service account"""
    
    print("🔧 GOOGLE SHEETS SETUP GUIDE")
    print("=" * 50)
    print()
    print("To upload crypto projects to Google Sheets, you need a Google Service Account.")
    print()
    print("📋 STEP-BY-STEP INSTRUCTIONS:")
    print()
    print("1️⃣  Go to: https://console.cloud.google.com/")
    print("2️⃣  Create a new project or select existing project")
    print("3️⃣  Enable Google Sheets API:")
    print("    - Go to 'APIs & Services' > 'Library'")
    print("    - Search 'Google Sheets API'")
    print("    - Click 'Enable'")
    print()
    print("4️⃣  Create Service Account:")
    print("    - Go to 'APIs & Services' > 'Credentials'")
    print("    - Click 'Create Credentials' > 'Service Account'")
    print("    - Name: 'crypto-scanner'")
    print("    - Click 'Create and Continue'")
    print("    - Skip roles (click 'Continue')")
    print("    - Click 'Done'")
    print()
    print("5️⃣  Generate Key:")
    print("    - Click on your service account email")
    print("    - Go to 'Keys' tab")
    print("    - Click 'Add Key' > 'Create New Key'")
    print("    - Select 'JSON' format")
    print("    - Download the JSON file")
    print()
    print("6️⃣  Share Google Sheet:")
    print("    - Open your Google Sheet")
    print("    - Click 'Share' button")
    print("    - Add the service account email (from the JSON file)")
    print("    - Give 'Editor' permissions")
    print()
    print("7️⃣  Save Credentials:")
    print("    - Copy the downloaded JSON file to this folder")
    print("    - Rename it to: 'google_service_key.json'")
    print()
    print("🔗 Your Google Sheet ID: 1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4")
    print()
    
    # Check if credentials file exists
    if os.path.exists('google_service_key.json'):
        print("✅ Found 'google_service_key.json' file!")
        
        # Test the credentials
        try:
            with open('google_service_key.json', 'r') as f:
                creds = json.load(f)
            
            service_email = creds.get('client_email', 'Unknown')
            print(f"📧 Service Account Email: {service_email}")
            print()
            print("🧪 Testing connection...")
            
            # Test connection
            import sys
            sys.path.append('.')
            from fresh_scanner import test_google_sheets_connection
            
            success, message = test_google_sheets_connection()
            if success:
                print("✅ Google Sheets connection successful!")
                print("🚀 Your scanner can now upload to Google Sheets!")
            else:
                print(f"❌ Connection failed: {message}")
                print("💡 Make sure you shared the sheet with the service account email")
            
        except Exception as e:
            print(f"❌ Error reading credentials: {e}")
            print("💡 Make sure the JSON file is valid")
    else:
        print("❌ No 'google_service_key.json' file found")
        print("💡 Please follow the steps above to create and download the credentials")
    
    print()
    print("=" * 50)
    print("Once setup is complete, restart the scanner to use Google Sheets!")

if __name__ == "__main__":
    create_google_service_account() 