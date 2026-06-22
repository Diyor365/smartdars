#!/bin/bash
# SmartDars Bot - Heroku Deployment Script
# Windows (Git Bash) yoki Mac/Linux'da ishlatish

echo "🚀 SmartDars Bot - HEROKU DEPLOYMENT"
echo "===================================="
echo ""

# Heroku CLI tekshirish
echo "1️⃣  Heroku CLI tekshirilmoqda..."
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI o'rnatilmagan!"
    echo "   https://devcenter.heroku.com/articles/heroku-cli'dan o'rnating"
    exit 1
fi
echo "✅ Heroku CLI: $(heroku --version)"

# Git tekshirish
echo ""
echo "2️⃣  Git tekshirilmoqda..."
if ! command -v git &> /dev/null; then
    echo "❌ Git o'rnatilmagan!"
    echo "   https://git-scm.com/download'dan o'rnating"
    exit 1
fi
echo "✅ Git: $(git --version)"

# Login
echo ""
echo "3️⃣  Heroku'ga login..."
heroku login
echo ""

# App nomi
echo "4️⃣  App nomi kiriting (masalan: smartdars-bot):"
read APP_NAME

echo "Creating Heroku app: $APP_NAME..."
heroku create $APP_NAME

# Config
echo ""
echo "5️⃣  CONFIGURATION"
echo "BOT_TOKEN'ni @BotFather'dan olganingizni tekshirdi!"
echo "BOT_TOKEN kiriting:"
read BOT_TOKEN

echo "ADMIN_ID'ni @userinfobot'dan olganingizni tekshirdi!"
echo "ADMIN_ID kiriting:"
read ADMIN_ID

echo ""
echo "Config variables sozlanmoqda..."
heroku config:set BOT_TOKEN="$BOT_TOKEN" --app $APP_NAME
heroku config:set ADMIN_ID="$ADMIN_ID" --app $APP_NAME

echo ""
echo "✅ Config variables set:"
heroku config --app $APP_NAME

# Git
echo ""
echo "6️⃣  Git sozlanmoqda..."
git init
git add .
git commit -m "Initial SmartDars Bot deployment to Heroku"
heroku git:remote --app $APP_NAME

# Deploy
echo ""
echo "7️⃣  HEROKU'GA DEPLOY QILINYAOPTI..."
echo "   (Bu 2-3 daqiqa vaqt oladi...)"
echo ""
git push heroku main

# Verification
echo ""
echo "8️⃣  Tekshirilmoqda..."
sleep 5
echo ""
echo "📊 LOGS:"
heroku logs --tail -n 20 --app $APP_NAME

echo ""
echo "✅ DEPLOYMENT TUGANDI!"
echo ""
echo "🎯 Keyingi qadam:"
echo "   Telegram'da https://t.me/@$APP_NAME botini izlaing"
echo "   /start bo'sing"
echo ""
echo "📖 Qo'shimcha:"
echo "   Real-time logs: heroku logs --tail --app $APP_NAME"
echo "   Restart bot: heroku dyno:restart --app $APP_NAME"
echo ""
echo "🎉 MUVAFFAQ!"
