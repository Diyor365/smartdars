# 🚀 SmartDars Bot - RAILWAY DEPLOYMENT QOLLANMASI

Railway'ga SmartDars Telegram Bot'ni deploy qilish (Heroku'ndan ANCHA YAXSHI!)

---

## 📋 TAYYORLIK

### 1️⃣ Railway Account Yaratish (GitHub orqali)

```bash
# Railway Website'ga oching
https://railway.app/

# GitHub Account orqali sign up qiling (1 click)
# GitHub salomat bo'lsa - Oauth orqali kiritadi
```

**Natija:** Railway dashboard ochiladi ✅

---

## 🔧 RAILWAY'GA DEPLOY QILISH (2 QADAM!)

### QADAM 1: GitHub'da Repository Yaratish

```bash
# GitHub Desktop yoki Terminal'da:
cd C:/Users/Diyorbek/Desktop/smartdars/smartdars

# Git init (agar bo'lmasa)
git init

# Remote qo'shish
git remote add origin https://github.com/YOUR_USERNAME/smartdars-bot.git

# Barcha fayllarni add qilish
git add .

# Commit qilish
git commit -m "Initial commit: SmartDars Telegram Bot"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### QADAM 2: Railway Dashboard'dan Deploy Qilish

1. **Railway Dashboard'ni oching:**
   ```
   https://railway.app/dashboard
   ```

2. **"New Project" bosing**

3. **"Deploy from GitHub" bosing**

4. **O'z repository'ni tanlang:**
   - `smartdars-bot` ni izlab toping
   - "Connect Repository" bosing ✅

5. **Environment Variables Qo'ying:**
   
   Rail way Dashboard → Variables → Add Variable:
   ```
   BOT_TOKEN=YOUR_TOKEN_HERE
   ADMIN_ID=123456789
   DATABASE_NAME=smartdars.db
   ```

6. **Deploy Tugmasini Bosing!**
   ```
   🟢 Deploy Button → Waiting...
   ```

**NATIJA:**
```
✅ Deployment started
✅ Building Python app
✅ Installing requirements
✅ Starting bot
🌍 URL: https://smartdars-bot.up.railway.app
```

---

## ✅ DEPLOYMENT TEKSHIRISH

### Bot Ishlayaptimi?

```bash
# Railway Dashboard → Logs
# Yoki terminal:
railway logs
```

**Ko'rinishi kerak:**
```
🤖 Bot ishga tushdi!
Waiting for messages...
```

### Telegram'da Test Qilish

```
1. Telegram da @smartdars_bot ni yoki o'z bot'ingizni izlang
2. /start yozing
3. Testni boshlang ✅

Agar ishlasa - DEPLOY MUVAFFAQ! 🎉
```

---

## 🔐 ENVIRONMENT VARIABLES

Railway Dashboard'da:
```
Settings → Variables → Add Variable

BOT_TOKEN = YOUR_TOKEN_FROM_BOTFATHER
ADMIN_ID = YOUR_ID_FROM_USERINFOBOT
DATABASE_NAME = smartdars.db
```

**Hozirgi setup:**
```bash
railway env:pull
# .env fayli create qiladi

# Tekshirish:
cat .env

# O'zgarish qilish:
railway env:set BOT_TOKEN="new_token"
```

---

## 🔄 CODE UPDATE QILISH (Git Push!)

Hozir engine juda sodda - Code o'zgargan vaqt:

```bash
# 1. O'zgarish qilish (masalan bot.py'ni tahrirlash)

# 2. Git'ga add qilish
git add .

# 3. Commit
git commit -m "Feature: savol import bug fix"

# 4. Push GitHub'ga
git push origin main

# 5. Railway automatic deploy qiladi! ✅
# (5-10 soniyada redeploy bo'ladi)
```

**Logs tekshirish:**
```bash
railway logs --tail
```

---

## 📊 RAILWAY PLANS (FREE -> PAID)

### Free Plan (BEPUL!)

```
✅ BEPUL:
- Unlimited dyno hours (24/7!)
- $5 free credit/month
- PostgreSQL/MySQL bepul
- 1GB SSD storage
- Perfect for small bots

❌ LIMIT:
- CPU: Shared
- Memory: Limited
- Bandwidth: 100GB/month
```

### Paid Plan (PRO)

```
STARTER: $5/month
- Dedicated CPU
- 4GB RAM
- More storage

HOBBY: $10/month
- Better performance
- Priority support
```

**TAVSIYA:** Hozircha FREE yetarli! 👍

---

## 🐛 MUAMMOLAR VA YECHIM

### ❌ "500 Internal Server Error"

```bash
# Logs tekshirish
railway logs --tail

# Agar RuntimeError bo'lsa:
# 1. BOT_TOKEN to'g'rimi?
# 2. ADMIN_ID to'g'rimi?
# 3. requirements.txt mavjudmi?

# Railway Dashboard → Redeploy
```

### ❌ "H12 Request Timeout"

```
Masala: Bot 30 sekunddan ko'proq vaqt oldi

Yechim:
- Local'da test qiling
- requirements.txt optimizatsiya qiling
```

### ❌ "Database Error"

```bash
# Railway shell orqali tekshirish
railway shell
python3
>>> import sqlite3
>>> conn = sqlite3.connect('smartdars.db')
>>> print(conn)

# Agar file yo'q bo'lsa - create qiladi
```

---

## 📱 DATABASE (RAILWAY'DA)

### SQLite (Hozir Bog'langan)

```
✅ TO'G'RI:
- Builtin file storage
- No setup needed
- Backup easy

❌ MASALA:
- Ephemeral (bot restart → data lost)
```

### PostgreSQL QOSHING (RECOMMENDED)

Railway'da PostgreSQL 100% free! 🎁

```bash
# Railway CLI orqali
railway add postgresql

# Automatic integration!
# DATABASE_URL environment variable qo'shiladi

# Python'da ishlash (migration):
# 1. psycopg2 o'rnatish
# 2. Connection change
```

**HOZIRCHA KERAK EMAS** - SQLite shu basta yaxshi. Keyincha qo'shishimiz mumkin.

---

## 🎯 RAILWAY CLI COMMANDS

```bash
# Login
railway login

# GitHub auth'ga qayta marhamat qiladi
# Browser orqali kiritadi

# Current project
railway list

# Logs (live)
railway logs --tail

# Environment variables
railway env:pull     # .env'ni pull qilish
railway env:set      # Variable qo'yish
railway env:delete   # Variable o'chirish

# Database
railway db:shell     # SQLite shell ochish

# Redeploy
railway deploy

# Status
railway status

# Local run
railway run python3 bot.py
```

---

## 🌐 CUSTOM DOMAIN (OPTIONAL)

Railway Dashboard:
```
Settings → Domain
Add Custom Domain
railway.app -> yourdomain.com

DNS CNAME:
yourdomain.com -> smartdars.railway.app
```

---

## 📜 RAILWAY DEPLOYMENT CHECKLIST

```
✅ GitHub account bor
✅ Repository created
✅ Bot Token bor (@BotFather)
✅ Admin ID bor (@userinfobot)
✅ requirements.txt bor
✅ Procfile bor (Railway opsional)
✅ runtime.txt bor
✅ GitHub'ga push qilindi
✅ Railway account bor
✅ Repository connected
✅ Environment variables set
✅ Deploy bosandi
✅ Logs checked
✅ Telegram'da test (🎉 DEPLOY COMPLETE!)
```

---

## 🎉 MUVAFFAQ DEPLOYMENT

```
✅ Railway'ga deploy qilindi
✅ Bot 24/7 active (no sleep!)
✅ GitHub integration (auto-redeploy)
✅ Logs live monitoring
✅ PostgreSQL ready (optional)
✅ Free tier yetarli
✅ Ko'plab users qo'llay oladi

🌟 RAILWAY TAFSILI!
```

---

## 🚀 KEYINGI QADAMLAR

1. **PostgreSQL qo'shish** (long-term)
2. **Custom domain** (branding)
3. **Email notifications** (alerts)
4. **Monitoring** (LogDNA, etc)
5. **Scaling** (agar many users bo'lsa)

---

## 🔗 RAILWAY DOCS

```
https://docs.railway.app/
https://docs.railway.app/deploy/deployments
https://docs.railway.app/guides/python
```

---

## 💡 RAILWAY vs HEROKU

| Feature | Railway | Heroku |
|---------|---------|--------|
| **Deploy** | GitHub Integration | Git Push |
| **Free Tier** | $5/month credit | 550h/month sleep |
| **Sleep** | ❌ NO! 24/7 | ❌ YES (30min) |
| **Database** | PostgreSQL free | Costly addon |
| **Setup** | 2 clicks | 5 steps |
| **CLI** | railway | heroku |
| **Price** | $5/month free | $0 (limited) |
| **Monitoring** | In-built | Add-on |
| **Speed** | ⚡ Fast | Medium |

**NATIJA:** Railway > Heroku ✅

---

## 🎓 RAILWAY QISQA GUIDE

### 1. GitHub'da Push Qilish
```bash
git push origin main
```

### 2. Railway Dashboard'dan Deploy Qilish
```
https://railway.app/dashboard
→ New Project
→ Connect GitHub
→ Select smartdars-bot
→ Add Variables
→ Deploy!
```

### 3. Test Qilish
```bash
railway logs --tail
# Bot logs ko'rish

# Telegram'da /start
# Ishlamoqda ✅
```

### 4. Update Qilish
```bash
git push origin main
# Railway automatic redeploy qiladi!
```

**SHUNGA OX!** 🎉

---

## 📞 SUPPORT

Railway dokumentatsiya juda yaxshi:
```
https://docs.railway.app/guides/telegram
```

---

**SmartDars Bot - Railway'da Ishga Tushdi!** 🚀

*Hozir Heroku'dan xalos bo'ldik!* 🎉

---

**QADAM 1:** Bot Token Berish
```bash
railway env:set BOT_TOKEN="YOUR_TOKEN"
```

**QADAM 2:** Admin ID Berish
```bash
railway env:set ADMIN_ID="YOUR_ID"
```

**QADAM 3:** Deploy!
```bash
git push origin main
```

📝 **DEPLOY COMPLETE!** 🎓

---

## ⚡ RAILWAY YA.QUICK START

**Time: 5 minutes** ⏱️

```bash
# 1. GitHub'ga push
git push origin main

# 2. Railway Dashboard
https://railway.app/dashboard

# 3. "New Project" + "Connect GitHub"
# Smartdars-bot tanlang

# 4. Variables qo'ying
railway env:set BOT_TOKEN="YOUR_TOKEN"
railway env:set ADMIN_ID="YOUR_ID"

# 5. Deploy!
# Green button → Deploy

# 6. Logs tekshirish
railway logs --tail

# 7. Test Telegram'da
/start → ✅ ISHGA TUSHDI!
```

**BITTI!** 🎉

---

**Tabriklaydu SmartDars Bot Railway'da Ishga Tushdi!** 🚀✨
