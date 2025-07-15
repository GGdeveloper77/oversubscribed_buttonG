# Crypto Projects Scanner

A Telegram-based crypto projects scanner that monitors selected groups and analyzes projects using Perplexity AI, then uploads results to Google Sheets.

## Features

- 🔍 **Smart Scanning**: Monitors Telegram groups for crypto project mentions
- 🤖 **AI Analysis**: Uses Perplexity AI for critical project evaluation
- 📊 **Google Sheets Integration**: Automatically uploads findings with structured reviews
- 🚀 **Vercel Ready**: Configured for serverless deployment

## Key Files

- `fresh_scanner.py` - Main scanner application with Flask web interface
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment configuration
- `setup_google_sheets.py` - Google Sheets authentication setup

## Deployment

### Environment Variables Required:
- `TELEGRAM_API_ID` - Your Telegram API ID
- `TELEGRAM_API_HASH` - Your Telegram API Hash  
- `TELEGRAM_SESSION_STRING` - Your Telegram session string
- `PERPLEXITY_API_KEY` - Your Perplexity API key
- `GOOGLE_SHEET_ID` - Target Google Sheet ID
- `GOOGLE_SERVICE_ACCOUNT_JSON` - Google Service Account credentials (JSON)

### Deploy to Vercel:
1. Connect this repository to Vercel
2. Set up environment variables in Vercel dashboard
3. Deploy!

## Usage

The scanner provides a web interface at `/` for manual scanning and monitoring. It automatically:
- Detects new crypto projects from configured Telegram groups
- Analyzes them using Perplexity AI with critical evaluation
- Uploads structured reviews to Google Sheets
- Avoids duplicates and tracks message sources

## Target Groups

Currently monitors groups like:
- "[OS] Projects"
- "Oversubscribed <> Crypbooster Deal Flow"

Results include project analysis with structured format:
- ✅ Pros
- ⚠️ Risks/Red Flags  
- 🔎 What Are These Guys Doing

## Tech Stack

- Python 3.9+
- Flask (Web framework)
- Telethon (Telegram client)
- Perplexity AI (Analysis)
- Google Sheets API (Data storage)
- Vercel (Serverless hosting)
