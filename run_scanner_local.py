#!/usr/bin/env python3
"""
🚀 FREE Crypto Scanner - Local Runner
Run this anytime for immediate crypto project scanning!
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append('.')

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment

def print_banner():
    """Print a nice banner"""
    print("=" * 60)
    print("🚀 FREE CRYPTO PROJECTS SCANNER")
    print("⚡ Local Edition - Run Anytime!")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

async def main():
    """Main function to run the scanner"""
    print_banner()
    
    try:
        # Import scanner functions
        from fresh_scanner import run_daily_scan, upload_to_google_sheets
        
        print("🔍 Scanning Telegram groups for crypto projects...")
        print("📱 Target groups: [OS] Projects, Oversubscribed groups, etc.")
        print()
        
        # Run the scan
        projects = await run_daily_scan()
        
        print(f"📊 SCAN RESULTS: Found {len(projects)} crypto projects!")
        print()
        
        if projects:
            # Show what we found
            for i, project in enumerate(projects, 1):
                print(f"🔥 Project {i}: {project.get('name', 'Unknown')}")
                print(f"   📍 Source: {project.get('source_group', 'Unknown')}")
                print(f"   👤 Posted by: {project.get('forwarder_name', 'Unknown')}")
                print()
            
            print("📤 Uploading to Google Sheets...")
            success = await upload_to_google_sheets(projects)
            
            if success:
                print("✅ SUCCESS! All projects uploaded to Google Sheets!")
                print(f"🔗 Check: https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SHEET_ID', '1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4')}")
            else:
                print("⚠️  Upload had some issues, but projects were found!")
                
        else:
            print("📭 No new crypto projects found in the last 24 hours.")
            print("💡 This could mean:")
            print("   • Groups have been quiet")
            print("   • All recent projects were already scanned")
            print("   • Projects didn't meet crypto keywords threshold")
        
        print()
        print("=" * 60)
        print("✨ SCAN COMPLETE!")
        print(f"🕐 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("💡 Run this script anytime for fresh results!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're in the correct directory with fresh_scanner.py")
        return False
        
    except Exception as e:
        print(f"❌ Scanner Error: {e}")
        print("💡 Check your credentials and internet connection")
        return False
    
    return True

def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Checking environment...")
    
    required_vars = [
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH', 
        'TELEGRAM_SESSION_STRING',
        'PERPLEXITY_API_KEY',
        'GOOGLE_SHEET_ID'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("❌ Missing environment variables:")
        for var in missing:
            print(f"   • {var}")
        print()
        print("💡 Add these to your environment or .env file")
        return False
    else:
        print("✅ Environment configured correctly!")
        print()
        return True

if __name__ == "__main__":
    print("🚀 Starting FREE Crypto Scanner...")
    print()
    
    # Check environment first
    if not check_environment():
        print("⚠️  Please fix environment variables first")
        sys.exit(1)
    
    # Run the scanner
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Scanner stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 