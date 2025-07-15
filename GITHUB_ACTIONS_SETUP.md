# 🤖 GitHub Actions Setup Guide

**Get FREE automatic crypto scanning every 6 hours!**

## 🚀 **What This Does:**

- ✅ **Runs your `fresh_scanner.py` automatically every 6 hours**
- ✅ **Scans all your Telegram groups for crypto projects**
- ✅ **Analyzes projects with Perplexity AI**
- ✅ **Uploads results to Google Sheets automatically**
- ✅ **Completely FREE** (GitHub gives 2,000 minutes/month)
- ✅ **No server needed** (runs on GitHub's servers)

---

## 📋 **Step 1: Push Code to GitHub**

```bash
git add .
git commit -m "🤖 Add GitHub Actions automatic scanning"
git push origin main
```

---

## 🔑 **Step 2: Add GitHub Secrets**

**Go to your GitHub repository:**
1. Click **"Settings"** tab
2. Click **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"**

**Add these 6 secrets exactly:**

### **Secret 1: TELEGRAM_API_ID**
```
Name: TELEGRAM_API_ID
Value: 28632541
```

### **Secret 2: TELEGRAM_API_HASH**
```
Name: TELEGRAM_API_HASH  
Value: b14125bcf447f6f91d43e0f8beea56fb
```

### **Secret 3: TELEGRAM_SESSION_STRING**
```
Name: TELEGRAM_SESSION_STRING
Value: 1ApWapzMBu0vNsZi2PE2EB5uY8_GyLAH_DmpOaNwPAwehkuefbGMLkUjy9Etm5zt3ijiPsbq9QZ-qzs7v_uF2gjibY-GBArXiZuzBW-Ob6o_QJKR_YYrBq3T3jiB_1My7LZpI3TrDPjCL5FqPjdhJsILc-B3JoA3OiMi-WJ63kGEUgpQzhS701mv5zEzw09KmY5UTp7-MAiTZTB98a1uva4mKF1Hh08N2Q0qeTbkcZlNbXMDAbUJBE2iWKlNQMeDLP-GvJeQ3cSGUxFyASRGx4Wr8HhManTjTgDqm5PAizZzURRlU-Z1AypvOdegD-ZDycbQICX-H-6N1xZV_d3Aui6cBXaSnL40=
```

### **Secret 4: PERPLEXITY_API_KEY**
```
Name: PERPLEXITY_API_KEY
Value: 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
```

### **Secret 5: GOOGLE_SHEET_ID**
```
Name: GOOGLE_SHEET_ID
Value: 1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4
```

### **Secret 6: GOOGLE_SERVICE_ACCOUNT_JSON**
```
Name: GOOGLE_SERVICE_ACCOUNT_JSON
Value: {"type":"service_account","project_id":"oversubscribed","private_key_id":"your_key_id","private_key":"your_private_key","client_email":"crypto-sheet-writer@oversubscribed.iam.gserviceaccount.com","client_id":"your_client_id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}
```

⚠️ **Replace with your actual Google service account JSON**

---

## ⚡ **Step 3: Enable GitHub Actions**

1. Go to **"Actions"** tab in your repo
2. Click **"I understand my workflows, enable them"**
3. Find **"🚀 Crypto Projects Scanner"** workflow
4. Click **"Enable workflow"**

---

## 🧪 **Step 4: Test It Manually**

**Test before waiting 6 hours:**

1. Go to **"Actions"** tab
2. Click **"🚀 Crypto Projects Scanner"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it run in real-time!

---

## 📊 **What You'll See:**

```
🚀 Starting Fresh Crypto Scanner...
📅 Scan started at: Mon Jan 15 14:30:15 UTC 2024
🎯 Target groups: [OS] Projects, Oversubscribed groups, etc.

🔍 Running daily crypto scan...
📱 Scanning Telegram groups for new projects...

📊 SCAN RESULTS:
   💬 Messages scanned: 45
   🔥 Total projects found: 3
   🔄 Duplicates filtered: 1
   ✨ Fresh projects: 2
   📤 Uploaded to sheets: 2

🎉 SUCCESS! New crypto projects found and uploaded!
   1. PrompTale AI (from [OS] Projects)
   2. Maiga.ai (from Oversubscribed <> Crypbooster Deal Flow)

🔗 Check your Google Sheets: https://docs.google.com/spreadsheets/d/1v96qj9_ZS2YyJo9-PAGJShc7xMesPb55Gt0YtqeJop4

✅ Scan completed at: 2024-01-15 14:31:22 UTC

════════════════════════════════════════
🎯 GitHub Actions Crypto Scanner Complete
📅 Finished at: Mon Jan 15 14:31:25 UTC 2024
🔄 Next scan in 6 hours (automatic)
📊 Check your Google Sheets for results
════════════════════════════════════════
```

---

## 🕒 **Schedule:**

**Automatic scans run:**
- **Every 6 hours:** 00:00, 06:00, 12:00, 18:00 UTC
- **Manual trigger:** Run anytime from Actions tab
- **Free limit:** 2,000 minutes/month (you'll use ~20 minutes/month)

---

## 📧 **Notifications:**

**GitHub will email you if:**
- ❌ Scan fails (check credentials)
- ✅ Scan succeeds (optional, can disable)

**To disable success notifications:**
1. Go to your profile → Settings → Notifications
2. Uncheck "Actions" for successful workflows

---

## 🔧 **Troubleshooting:**

### **"Scan Failed" Error:**
- ✅ Check all 6 secrets are added correctly
- ✅ Verify Google service account JSON is valid
- ✅ Make sure Telegram session isn't expired

### **"No Projects Found":**
- ✅ Normal! Groups might be quiet
- ✅ Scanner only finds NEW projects (last 24h)
- ✅ Filters out duplicates automatically

### **"Upload Failed":**
- ✅ Check Google Sheets permissions
- ✅ Verify service account has edit access
- ✅ Make sure sheet ID is correct

---

## 🎉 **You're Done!**

**Now you have:**
- ✅ **Automatic scanning** every 6 hours
- ✅ **Real crypto project detection**
- ✅ **Critical AI analysis**
- ✅ **Google Sheets integration**
- ✅ **100% FREE** automation

**No more manual scanning needed!** 🚀

---

## 💡 **Pro Tips:**

1. **Bookmark your Google Sheet** for quick access
2. **Watch first few runs** to make sure everything works
3. **Check Actions tab** if you don't see results
4. **Run manually** before important meetings for fresh data
5. **Scanner learns** - it gets better at filtering over time

**Your crypto scanner is now fully automated!** 🎯 