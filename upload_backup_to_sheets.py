#!/usr/bin/env python3
"""
Upload Backup Projects to Google Sheets
Run this after setting up Google credentials to upload found projects
"""

import json
import os
import sys

def upload_backup_projects():
    print("📊 UPLOADING BACKUP PROJECTS TO GOOGLE SHEETS")
    print("=" * 50)
    
    # Check if backup file exists
    backup_file = "crypto_projects_backup.json"
    if not os.path.exists(backup_file):
        print("❌ No backup file found (crypto_projects_backup.json)")
        return
    
    # Check if Google credentials exist
    if not os.path.exists('google_service_key.json'):
        print("❌ No Google credentials found")
        print("💡 Run: python setup_google_credentials.py first")
        return
    
    # Load backup data
    try:
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        print(f"📋 Found {len(backup_data)} backup sessions")
        
        # Get all projects from all sessions
        all_projects = []
        for session in backup_data:
            projects = session.get('projects', [])
            all_projects.extend(projects)
            print(f"📅 Session {session.get('timestamp', 'Unknown')}: {len(projects)} projects")
        
        print(f"\n📊 Total projects to upload: {len(all_projects)}")
        
        if len(all_projects) == 0:
            print("❌ No projects found in backup")
            return
        
        # Show projects
        print("\n🔍 Projects found:")
        for i, project in enumerate(all_projects, 1):
            name = project.get('project_name', 'Unknown')
            score = project.get('confidence_score', 0)
            source = project.get('source_group', 'Unknown')
            print(f"  {i}. {name} (Score: {score}%) from {source}")
        
        # Confirm upload
        print()
        confirm = input("Upload these projects to Google Sheets? (y/n): ").lower()
        
        if confirm != 'y':
            print("❌ Upload cancelled")
            return
        
        # Import scanner functions
        sys.path.append('.')
        from fresh_scanner import upload_to_google_sheets
        import asyncio
        
        # Upload projects
        print("\n🚀 Uploading to Google Sheets...")
        
        async def do_upload():
            uploaded_count = await upload_to_google_sheets(all_projects)
            return uploaded_count
        
        # Run upload
        uploaded_count = asyncio.run(do_upload())
        
        if uploaded_count > 0:
            print(f"✅ Successfully uploaded {uploaded_count} projects to Google Sheets!")
            print("🔗 Check your Google Sheet to see the results")
        else:
            print("❌ Upload failed - check the error messages above")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    upload_backup_projects() 