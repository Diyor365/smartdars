@echo off
REM SmartDars Bot - Heroku Deployment Script (Windows)

echo.
echo 🚀 SmartDars Bot - HEROKU DEPLOYMENT (WINDOWS)
echo ================================================
echo.

REM Heroku CLI tekshirish
echo 1️⃣  Heroku CLI tekshirilmoqda...
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI o'rnatilmagan!
    echo    https://devcenter.heroku.com/articles/heroku-cli'dan o'rnating
    pause
    exit /b 1
)
echo ✅ Heroku CLI tekshirildi

REM Git tekshirish
echo.
echo 2️⃣  Git tekshirilmoqda...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git o'rnatilmagan!
    echo    https://git-scm.com/download'dan o'rnating
    pause
    exit /b 1
)
echo ✅ Git tekshirildi

REM Login
echo.
echo 3️⃣  Heroku'ga login...
heroku login
echo.

REM App nomi
echo 4️⃣  App nomi kiriting (masalan: smartdars-bot):
set /p APP_NAME=

echo Creating Heroku app: %APP_NAME%...
heroku create %APP_NAME%

REM Config
echo.
echo 5️⃣  CONFIGURATION
echo BOT_TOKEN'ni @BotFather'dan kiriting:
set /p BOT_TOKEN=

echo ADMIN_ID'ni @userinfobot'dan kiriting:
set /p ADMIN_ID=

echo.
echo Config variables sozlanmoqda...
heroku config:set BOT_TOKEN="%BOT_TOKEN%" --app %APP_NAME%
heroku config:set ADMIN_ID="%ADMIN_ID%" --app %APP_NAME%

echo.
echo ✅ Config variables set:
heroku config --app %APP_NAME%

REM Git
echo.
echo 6️⃣  Git sozlanmoqda...
git init
git add .
git commit -m "Initial SmartDars Bot deployment to Heroku"
heroku git:remote --app %APP_NAME%

REM Deploy
echo.
echo 7️⃣  HEROKU'GA DEPLOY QILINYAOPTI...
echo    (Bu 2-3 daqiqa vaqt oladi...)
echo.
git push heroku main

REM Verification
echo.
echo 8️⃣  Tekshirilmoqda...
timeout /t 5 /nobreak

echo.
echo 📊 LOGS:
heroku logs --tail -n 20 --app %APP_NAME%

echo.
echo ✅ DEPLOYMENT TUGANDI!
echo.
echo 🎯 Keyingi qadam:
echo    Telegram'da https://t.me/@%APP_NAME% botini izlang
echo    /start bo'sing
echo.
echo 📖 Qo'shimcha:
echo    Real-time logs: heroku logs --tail --app %APP_NAME%
echo    Restart bot: heroku dyno:restart --app %APP_NAME%
echo.
echo 🎉 MUVAFFAQ!
echo.
pause
