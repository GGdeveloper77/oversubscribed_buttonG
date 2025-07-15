#!/usr/bin/env python3
"""
Fix Google Sheets Connection
Resolves "No key could be detected" error
"""

import json
import os
import tempfile

def fix_google_connection():
    print("🔧 FIXING GOOGLE SHEETS CONNECTION")
    print("=" * 40)
    
    # Check if credentials file exists
    if not os.path.exists('google_service_key.json'):
        print("❌ google_service_key.json not found")
        return False
    
    try:
        # Load and validate credentials
        with open('google_service_key.json', 'r') as f:
            creds = json.load(f)
        
        print("✅ Credentials file loaded successfully")
        print(f"📧 Service Account: {creds.get('client_email', 'Unknown')}")
        
        # Test different gspread connection methods
        print("\n🧪 Testing gspread connection methods...")
        
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            
            # Method 1: Direct file path
            print("🔹 Method 1: Direct file authentication...")
            try:
                gc = gspread.service_account(filename='google_service_key.json')
                print("✅ Method 1 successful!")
                return test_sheet_access(gc)
            except Exception as e:
                print(f"❌ Method 1 failed: {e}")
            
            # Method 2: Credentials object
            print("🔹 Method 2: Credentials object...")
            try:
                credentials = Credentials.from_service_account_file(
                    'google_service_key.json',
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                )
                gc = gspread.authorize(credentials)
                print("✅ Method 2 successful!")
                return test_sheet_access(gc)
            except Exception as e:
                print(f"❌ Method 2 failed: {e}")
            
            # Method 3: Temporary file with proper encoding
            print("🔹 Method 3: Temporary file method...")
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as temp_file:
                    json.dump(creds, temp_file, indent=2)
                    temp_path = temp_file.name
                
                gc = gspread.service_account(filename=temp_path)
                os.unlink(temp_path)  # Clean up
                print("✅ Method 3 successful!")
                return test_sheet_access(gc)
            except Exception as e:
                print(f"❌ Method 3 failed: {e}")
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            # Method 4: Manual credentials setup
            print("🔹 Method 4: Manual credentials...")
            try:
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                credentials = Credentials.from_service_account_info(creds, scopes=scopes)
                gc = gspread.authorize(credentials)
                print("✅ Method 4 successful!")
                return test_sheet_access(gc)
            except Exception as e:
                print(f"❌ Method 4 failed: {e}")
            
            print("❌ All connection methods failed")
            return False
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("💡 Try: pip install gspread google-auth")
            return False
    
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return False

def test_sheet_access(gc):
    """Test access to the specific Google Sheet"""
    try:
        GOOGLE_SHEET_ID = "1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4"
        
        print(f"📊 Testing access to sheet: {GOOGLE_SHEET_ID}")
        sheet = gc.open_by_key(GOOGLE_SHEET_ID)
        worksheet = sheet.sheet1
        
        # Test read access
        print("📖 Testing read access...")
        cell_range = worksheet.get('A1:B2')
        print(f"✅ Read test successful: {len(cell_range)} rows")
        
        # Test write access (write a test value)
        print("✏️ Testing write access...")
        test_cell = worksheet.acell('A1')
        current_value = test_cell.value
        
        # Write test marker
        worksheet.update('A1', 'TEST_CONNECTION')
        
        # Restore original value
        if current_value:
            worksheet.update('A1', current_value)
        else:
            worksheet.update('A1', 'Name')  # Default header
        
        print("✅ Write test successful!")
        print("🎉 Google Sheets connection is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Sheet access failed: {e}")
        if "PERMISSION_DENIED" in str(e):
            print("💡 Make sure the sheet is shared with the service account")
        elif "not found" in str(e).lower():
            print("💡 Check the Google Sheet ID")
        return False

if __name__ == "__main__":
    success = fix_google_connection()
    if success:
        print("\n✅ Google Sheets is ready to use!")
        print("🚀 Restart your scanner to upload projects automatically!")
    else:
        print("\n❌ Connection still failing")
        print("💡 Check the troubleshooting suggestions above") 