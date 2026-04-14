#!/bin/bash
# smartdars-setup.sh - Bot tezda o'rnatish skriptasi (Linux/Mac uchun)

echo "🎓 SmartDars Bot - O'rnatish skriptasi"
echo "======================================"
echo ""

# Python tekshirish
echo "1️⃣  Python tekshirilmoqda..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 o'rnatilmagan! Iltimos python3 o'rnating"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Virtual Environment yaratish
echo ""
echo "2️⃣  Virtual Environment yaratilmoqda..."
python3 -m venv venv
source venv/bin/activate
echo "✅ Virtual Environment yaratildi"

# Paketlarni o'rnatish
echo ""
echo "3️⃣  Kerakli paketlar o'rnatilmoqda..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Paketlar o'rnatildi"

# Config
echo ""
echo "4️⃣  Konfiguratsiya"
echo "config.py fayldagi TOKEN o'rnini o'z Telegram Bot tokeni bilan almashtirig!"
echo ""
echo "Token olish uchun:"
echo "  1. Telegram dan @BotFather ni toping"
echo "  2. /newbot ni yozing"
echo "  3. Bot nomini va usernameni kiriting"
echo "  4. Olingan tokenni config.py ga qo'ying"
echo ""

# Database tekshirish
echo "5️⃣  Database yaratilmoqda..."
python3 -c "from database import Database; Database()"
echo "✅ Database tayyor"

echo ""
echo "🚀 TAYYOR!"
echo "Bot ishga tushirish uchun quyidagini kiriting:"
echo ""
echo "  python3 bot.py"
echo ""
echo "Buning oldidan config.py da TOKEN ni o'zgartirishni unutmang!"
