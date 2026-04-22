# 🚀 HEROKU DEPLOYMENT - TEZDA QOLLANMA

**5 DAQIQADA DEPLOY!**

---

## 1️⃣ O'RNATISH

```bash
# Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli

# Windows: .exe installer
# Mac: brew install heroku-cli
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

## 2️⃣ HEROKU'GA KIRISH

```bash
heroku login
# Brauzer ochiladi, kiriting
```

## 3️⃣ APP YARATISH

```bash
heroku create smartdars-bot
```

## 4️⃣ CONFIG SOZLASH

```bash
# Token'ni @BotFather'dan olish (agar yo'q bo'lsa)
# ID'ni @userinfobot'dan olish (agar yo'q bo'lsa)

# Heroku'ga qo'yish:
heroku config:set BOT_TOKEN="5921954XXX:AAHXXX..." --app smartdars-bot
heroku config:set ADMIN_ID="123456789" --app smartdars-bot

# Tekshirish:
heroku config --app smartdars-bot
```

## 5️⃣ GIT SOZLASH VA DEPLOY

```bash
# Smart repository'da
cd /path/to/smartdars/smartdars

# Git init
git init
git add .
git commit -m "Deploy to Heroku"

# Heroku remote
heroku git:remote --app smartdars-bot

# DEPLOY!
git push heroku main
```

## 6️⃣ TEKSHIRISH

```bash
# Logs
heroku logs --tail --app smartdars-bot

# Telegram'da test
# /start bo'sing

# Hammasi yaxshimi?
# ✅ DEPLOY COMPLETE!
```

---

## 📊 HEROKU LOGS

```bash
# Real-time logs
heroku logs --tail --app smartdars-bot

# Last 100 lines
heroku logs -n 100 --app smartdars-bot

# Errors only
heroku logs --tail --app smartdars-bot | grep -i error
```

---

## 🔄 BOT QAYTA ISHGA TUSHIRISH

```bash
heroku dyno:restart --app smartdars-bot
```

---

## 🔧 CONFIG UPDATE

```bash
# Qiymatni o'zgartirish
heroku config:set BOT_TOKEN="new_token" --app smartdars-bot

# Remove
heroku config:unset BOT_TOKEN --app smartdars-bot
```

---

## 💰 PRICING

```
✅ FREE: $0
   - 550h/oy
   - 30 min ishlagach sleep

💳 PAID: $7+
   - Unlimited
   - Doimo active
```

---

## ⚠️ MUHIM

```
1. BOT_TOKEN va ADMIN_ID'ni heroku config'ga qo'ying!
2. questions.json fayli deploy'ganda saqlanadi
3. SQLite database ephemeral (restart'lanmasa o'chib ketadi)
   → PostgreSQL qo'shish yechim
```

---

## ❌ DEBUGGING

```
"App Error: H10"
→ heroku logs --app smartdars-bot ko'ring

"Bot sleep"
→ Free plan'da 30 min => Paid plan kerak

"Token error"
→ heroku config tekshiring
```

---

## 🎹 SCRIPT'LAR

**Windows:**
```bash
deploy-heroku.bat
# Autocomplete deploy, faqat TOKEN va ADMIN_ID kiriting
```

**Mac/Linux:**
```bash
bash deploy-heroku.sh
```

---

## 📱 TELEGRAM'DA TEST

```
1. Heroku app name + .herokuapp.com
2. @smartdars_bot + username + t.me
3. /start bo'sing
4. Test qiling

✅ Ishlayapti? MUVAFFAQ! 🎉
```

---

## 🎯 XULOSA

```
5 daqiqa:
✅ Heroku app
✅ Config set
✅ Git push
✅ Deploy
✅ TEST COMPLETE!

Bot LIVE! 🚀
```

---

**SmartDars Telegram - Cloud'da Ishlamoqda!** ☁️✨
