# 🆓 FREE Crypto Scanner Options

**You have 3 completely FREE ways to run your crypto scanner!**

## 🖥️ **OPTION 1: Local Scanning (INSTANT & FREE)**

**Best for:** Immediate results when you want them

### **Windows Users:**
```bash
# Just double-click this file:
run_scanner.bat
```

### **Python Users:**
```bash
python run_scanner_local.py
```

**What it does:**
- ✅ Scans all your Telegram groups
- ✅ Finds crypto projects from last 24 hours
- ✅ Analyzes with Perplexity AI
- ✅ Uploads to Google Sheets automatically
- ✅ Shows results in terminal
- ✅ **Completely FREE!**

---

## 🤖 **OPTION 2: GitHub Actions (AUTOMATIC & FREE)**

**Best for:** Automatic scanning every 6 hours

### **Setup (One-time):**

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Add free scanning options"
   git push origin main
   ```

2. **Add GitHub Secrets:**
   - Go to your GitHub repository
   - Settings → Secrets and variables → Actions
   - Add these secrets:
     ```
     TELEGRAM_API_ID = 28632541
     TELEGRAM_API_HASH = b14125bcf447f6f91d43e0f8beea56fb
     TELEGRAM_SESSION_STRING = your_session_string
     PERPLEXITY_API_KEY = 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
     GOOGLE_SHEET_ID = 1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4
     GOOGLE_SERVICE_ACCOUNT_JSON = {"type":"service_account"...}
     ```

3. **Enable Actions:**
   - Go to "Actions" tab in your GitHub repo
   - Enable workflows

**What it does:**
- 🕒 **Runs every 6 hours automatically**
- 🌍 **Runs on GitHub's servers** (not your computer)
- 📊 **Results go directly to Google Sheets**
- 🆓 **Completely FREE** (GitHub gives 2,000 minutes/month)
- 📧 **Email notifications** if something breaks

---

## ⚡ **OPTION 3: Manual Web Interface (FREE)**

**Best for:** When you want a nice UI

### **Run locally:**
```bash
python fresh_scanner.py
# Then open: http://localhost:5000
```

**What it does:**
- 🌐 **Nice web interface**
- 🖱️ **Click button to scan**
- 📊 **See results in browser**
- 🆓 **Free to run locally**

---

## 🚀 **QUICK START - Choose Your Method:**

### **Want results RIGHT NOW?**
→ **Use Option 1**: Double-click `run_scanner.bat`

### **Want automatic scanning?**
→ **Use Option 2**: Setup GitHub Actions (runs every 6 hours)

### **Want both?**
→ **Use both!** GitHub Actions for automatic + local for immediate

---

## 📋 **Environment Setup (Required for all options):**

Make sure you have these environment variables set:

```bash
# Windows (add to system environment variables):
TELEGRAM_API_ID=28632541
TELEGRAM_API_HASH=b14125bcf447f6f91d43e0f8beea56fb
TELEGRAM_SESSION_STRING=your_session_string
PERPLEXITY_API_KEY=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
GOOGLE_SHEET_ID=1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account"...}
```

**Or create a `.env` file:**
```
TELEGRAM_API_ID=28632541
TELEGRAM_API_HASH=b14125bcf447f6f91d43e0f8beea56fb
TELEGRAM_SESSION_STRING=your_session_string
PERPLEXITY_API_KEY=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
GOOGLE_SHEET_ID=1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account"...}
```

---

## 🎯 **Expected Results:**

When you run any of these options, you'll see:

```
🚀 FREE CRYPTO PROJECTS SCANNER
⚡ Local Edition - Run Anytime!
════════════════════════════════

🔍 Scanning Telegram groups for crypto projects...
📱 Target groups: [OS] Projects, Oversubscribed groups, etc.

📊 SCAN RESULTS: Found 3 crypto projects!

🔥 Project 1: PrompTale AI
   📍 Source: [OS] Projects
   👤 Posted by: @crypto_hunter

🔥 Project 2: Maiga.ai
   📍 Source: Oversubscribed <> Crypbooster Deal Flow
   👤 Posted by: @deal_flow_bot

📤 Uploading to Google Sheets...
✅ SUCCESS! All projects uploaded to Google Sheets!
🔗 Check: https://docs.google.com/spreadsheets/d/1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4

✨ SCAN COMPLETE!
```

---

## 💡 **Tips:**

1. **Run Option 1 immediately** to test everything works
2. **Setup Option 2** for automatic background scanning
3. **All results go to the same Google Sheet**
4. **No conflicts** - you can run multiple options
5. **100% FREE** - no hosting costs

---

## 🔧 **Troubleshooting:**

**"Import Error":** Make sure you're in the right directory  
**"Missing environment variables":** Set up your .env file  
**"No projects found":** Groups might be quiet, try again later  
**"Upload failed":** Check Google credentials  

---

## 🎉 **BEST SETUP:**

**My recommendation:**
1. **Test locally first:** Run `run_scanner.bat` to make sure everything works
2. **Setup GitHub Actions:** For automatic scanning every 6 hours
3. **Keep local runner:** For when you want immediate results

**This gives you:**
- ✅ **Automatic scanning** every 6 hours
- ✅ **Manual scanning** when you want it
- ✅ **100% FREE**
- ✅ **No server costs**
- ✅ **Reliable results** 