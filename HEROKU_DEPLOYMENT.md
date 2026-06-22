# 🚀 SmartDars Bot - HEROKU DEPLOYMENT QOLLANMASI

Heroku Cloud'ga SmartDars Telegram Bot'ni deploy qilish!

---

## 📋 TAYYORLIK

### 1️⃣ Heroku Account Yaratish

```bash
# Heroku Website'ga oching
https://www.heroku.com/

# Ro'yxatdan o'ting yoki kiriting
# Email va password (xavfsiz saqlanadi)
```

### 2️⃣ Heroku CLI O'rnatish

**Windows:**
```bash
# Windows installer'ni download qiling
https://devcenter.heroku.com/articles/heroku-cli

# Yoki choco yordamida
choco install heroku-cli

# Tekshirish
heroku --version
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
heroku --version
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku --version
```

### 3️⃣ Git O'rnatish

```bash
# Git o'natilimimi tekshiring
git --version

# Agar bo'lmasa: https://git-scm.com/download
```

---

## 🔧 HEROKU'GA DEPLOY QILISH

### QADAM 1: Heroku CLI'ga Kirish

```bash
cd C:/Users/Diyorbek/Desktop/smartdars/smartdars

heroku login
# Brauzer ochiladi, kiriting
```

### QADAM 2: Heroku App Yaratish

```bash
# Yangi app yaratish
heroku create smartdars-bot

# YA CUSTOM DOMAIN (agar xohlasangiz):
heroku create your-custom-name

# Tekshirish
heroku apps
```

**Output:**
```
Creating smartdars-bot... done
https://smartdars-bot.herokuapp.com/ | https://git.heroku.com/smartdars-bot.git
```

### QADAM 3: Config Variable'larni Qo'yish

```bash
# Bot TOKEN qo'ying
heroku config:set BOT_TOKEN="YOUR_TOKEN_HERE" --app smartdars-bot

# Admin ID qo'ying
heroku config:set ADMIN_ID="123456789" --app smartdars-bot

# Tekshirish
heroku config --app smartdars-bot
```

**MUHIM:** `YOUR_TOKEN_HERE` o'rniga o'z Bot Token'ingizni qo'ying!

### QADAM 4: Git Initialize Qilish

```bash
# Git init (agar bo'lmasa)
git init

# Heroku remote qo'shish
heroku git:remote --app smartdars-bot

# Tekshirish
git remote -v
```

### QADAM 5: Heroku'ga Push Qilish (DEPLOY!)

```bash
# Barcha fayllarni add qilish
git add .

# Commit qilish
git commit -m "Initial SmartDars Bot deployment"

# Heroku'ga push qilish
git push heroku main

# YOKI (agar master branch bo'lsa):
git push heroku master
```

**Output:**
```
Counting objects: 45, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (42/42), done.
Writing objects: 100% (45/45), 12.34 KiB | 6.17 MiB/s, done.
Total 45 (delta 2), reused 0 (delta 0)
remote: Compiling Python app
remote: Installing requirements with pip
remote: Collecting python-telegram-bot==20.3
...
remote: -----> Launching... done, v156
remote:        https://smartdars-bot.herokuapp.com/ deployed to Heroku
```

---

## ✅ DEPLOYMENT TEKSHIRISH

### Bot Ishlayaptimi?

```bash
# Logs ko'rish
heroku logs --tail --app smartdars-bot

# Agar hammasi yaxshi bo'lsa, ko'rinadi:
# "🤖 Bot ishga tushdi!"
```

### Telegram'da Test Qilish

```
1. Telegram da @smartdars_bot'ni izlang (yoki o'zingizning bot'ingiz)
2. /start yozing
3. Testni boshlang ✅

Agar to'g'ri ishlasa - DEPLOYMENT MUVAFFAQ! 🎉
```

---

## 🔐 ENVIRONMENT VARIABLES

| Variable | Qiymat | Tavsif |
|----------|--------|--------|
| `BOT_TOKEN` | Telegram Bot Token | http://t.me/BotFather dan |
| `ADMIN_ID` | Telegram User ID | http://t.me/userinfobot dan |
| `DATABASE_NAME` | smartdars.db | SQLite database nomi |

### Config'ni Update Qilish

```bash
# Biror variable'ni o'zgartirish
heroku config:set BOT_TOKEN="new_token" --app smartdars-bot

# Remove qilish
heroku config:unset BOT_TOKEN --app smartdars-bot

# Barcha config'ni ko'rish
heroku config --app smartdars-bot
```

---

## 📊 HEROKU DYNOS (FREE -> PAID)

### Free Plan (Durustimmi)

```
✅ FREE TIER:
- Faqat 550 saatlik dyno
- Oy'da 30 daqiqalik sleep
- Ortda ishga tushishi mumkin

❌ MASALA:
- Bot 30 min ishlagach o'chib ketadi
- Hech kim jo'natmasa yana uyg'onmaydi
```

### SOLUTION: Payer Plan

```bash
# Heroku Account → Billing
# Add Credit Card
# Upgrade to Paid Plan

✅ PAID (Starter Pro):
- Doimo ishlaydigan dyno ($50/oy)
- Unlimited access
- Har vaqt ishlaydi
```

---

## 🐛 MUAMMOLAR VA YECHIM

### ❌ "Bot sleep'ga ketadi (30 min)"

**Masala:** Free plan'da dyno 30 minutdan so'ng o'chib ketadi

**Yechim:**
```
1. Paid plan'ga o'tish ($7-50/oy)
2. YOKI local server'da ishga tushirish
3. YOKI uptime-monitoring service (UptimeRobot)
```

### ❌ "App Error: H10"

```bash
# Logs tekshirish
heroku logs --tail --app smartdars-bot

# Agar RuntimeError bo'lsa:
# TOKEN'i tekshiring!
heroku config --app smartdars-bot
```

### ❌ "requirements.txt not found"

```bash
# requirements.txt mavjud ekaniga ishonch hosil qiling
ls requirements.txt

# Agar bo'lmasa:
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt"
git push heroku main
```

### ❌ "questions.json not found"

```bash
# Heroku'dagi database'ni tekshirish
heroku run python3 --app smartdars-bot

# yoki
heroku run ls -la --app smartdars-bot
```

---

## 📱 DATABASE (HEROKU'DA)

### SQLite (Hozir Bog'langan)

```
Masala: Heroku'da ephemeral filesystem
(Bot restart'lanmasa hamma ma'lumot o'chib ketadi)

Yechim: PostgreSQL (Heroku addon)
```

### PostgreSQL O'rnatish (OPTIONAL)

```bash
# Heroku addon qo'shish
heroku addons:create heroku-postgresql:hobby-dev --app smartdars-bot

# Connection string olish
heroku config --app smartdars-bot | grep DATABASE_URL

# Python'da ishlash (migration kerak)
```

---

## 🎯 LIVE MONITORING

### Heroku Dashboard'da Ko'rish

```
https://dashboard.heroku.com/apps/smartdars-bot
```

### Real-time Logs

```bash
# Live logs (Ctrl+C to stop)
heroku logs --tail --app smartdars-bot

# Last 100 lines
heroku logs -n 100 --app smartdars-bot
```

### Dyno Restart

```bash
# Bot'ni qayta ishga tushirish
heroku dyno:restart --app smartdars-bot
```

---

## 🔄 UPDATES VA VERSIONS

### Code Update Qilish

```bash
# O'zgarish qilish
# (masalan: bot.py'ni tahrirlang)

# Git'ga add qilish
git add .

# Commit
git commit -m "Fix: savol import bug"

# Deploy
git push heroku main
```

### Version Control

```bash
# Hozirgi status
git status

# Commit history
git log

# Branch tekshirish
git branch
```

---

## 💰 HEROKU PRICING

| Plan | Narxi | Davomiyligi | Ish |
|------|-------|-----------|-----|
| **Free** | $0 | 30 min/oy | Test uchun |
| **Hobby** | $7 | 1000 h/oy | Kichik proyekt |
| **Standard** | $50 | Unlimited | Production |

---

## 🌐 CUSTOM DOMAIN (OPTIONAL)

```bash
# Domain qo'shish
heroku domains:add yourdomain.com --app smartdars-bot

# DNS sozlash (Domain provider'da)
# CNAME -> smartdars-bot.herokuapp.com

# Tekshirish
heroku domains --app smartdars-bot
```

---

## 📜 HEROKU DEPLOYMENT CHECKLIST

```
✅ Heroku account bor
✅ Heroku CLI o'rnatilgan
✅ Git o'rnatilgan
✅ Bot Token bor (@BotFather)
✅ Admin ID bor (@userinfobot)
✅ requirements.txt bor
✅ Procfile bor
✅ runtime.txt bor
✅ Heroku app created (heroku create)
✅ Config variables set (heroku config:set)
✅ Git initialized (git init)
✅ Files committed (git add . && git commit)
✅ Push to Heroku (git push heroku main)
✅ Logs checked (heroku logs --tail)
✅ Telegram'da test (🎉 DEPLOY COMPLETE!)
```

---

## 🎉 MUVAFFAQ DEPLOYMENT

```
✅ Heroku'ga deploy qilindi
✅ Bot Telegram'da active
✅ Savolllar import qilish ishlamoqda
✅ Statistika saqlanmoqda
✅ Admin panel enabled
✅ Ko'plab users qo'llay oladi

🌟 SHUNGA OX RAHMAT!
```

---

## 🚀 KEYINGI QADAMLAR

1. **Domain qo'shish** (yourdomain.com)
2. **PostgreSQL qo'shish** (production)
3. **Monitoring qo'shish** (SendGrid, etc)
4. **Admin panel uchun Web UI**
5. **Scaling** (agar many users bo'lsa)

---

## 📞 HEROKU DOCUMENTATSIYA

```
https://devcenter.heroku.com/
https://devcenter.heroku.com/articles/python-support
```

---

## 💡 TIPS

```
🔐 TOKEN'i xavfsiz saqlang (environment variable'da)
📊 Database backup olish (PostgreSQL)
🔔 Error tracking (Sentry, etc)
⚡ Performance optimization
🌍 Multi-region deployment
```

---

**SmartDars Bot - Heroku'da Ishga Tushdi!** 🎓🚀

*O'quvchilar o'zgargan doni qolmadi!* 📱✨

---

**KEYING: BOT TOKEN VA ADMIN ID'NI HEROKU CONFIG'GA QO'YING!**

```bash
heroku config:set BOT_TOKEN="YOUR_TOKEN" --app smartdars-bot
heroku config:set ADMIN_ID="YOUR_ID" --app smartdars-bot
```

📝 **DEPLOY COMPLETE!** 🎉
