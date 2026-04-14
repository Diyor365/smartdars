# 🚀 SmartDars Bot - TEZDA O'RNATISH QOLLANMASI

O'ta-onalar uchun o'quvchi testlash botini **5 DAQIQADA** ishga tushirish!

---

## 📋 TAHLAB OLINGAN NARSA

✅ **Bizda bor:**
- Python 3.8+ o'rnatilgan kompyuter
- Telegram hisobi
- Internet aloqasi

---

## 🎯 SODDALASHTIRGAN QADAMLAR

### QADAM 1: O'RNATIShni Tayyorlash (2 daqiqa)

**Windows:**
```bash
# Buyruq satriga qo'yish
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### QADAM 2: Token Olish (2 daqiqa)

1. **Telegram da @BotFather ga savdo qiling**
2. **/newbot ni yozing**
3. **Bot nomini kiriting** (masalan: "SmartDarsBot")
4. **Username kiriting** (masalan: "smartdars_bot_123")
5. **Olingan TOKEN ni nusxalab oling**

### QADAM 3: Bot Konfiguratsiyasi (1 daqiqa)

**config.py faylni oching:**

```python
# ESKI:
TOKEN = "YOUR_BOT_TOKEN_HERE"

# YANGI (o'z tokenni qo'y):
TOKEN = "5921954XXX:AAH-a7Xda6pXXXXXXXXXXXXX"
```

### QADAM 4: BOT ISHGA TUSHIRISH (0 daqiqa!)

```bash
python bot.py
```

Agar OK bo'lsa:
```
🤖 Bot ishga tushdi! Ctrl+C bilan to'xtating...
```

### QADAM 5: TEST QILING

Telegram da botingizni toping va **/start ni bosing** ✅

---

## 🎓 Bot Ishlashi

```
👨‍👩‍👦 OTA-ONA        →  [Botga yozadi]  →  👦 O'QUVCHI
                    ↓
              SINFNI TANLASH (1-4)
                    ↓
              FANNI TANLASH (Matematika/Ona tili)
                    ↓
              MAVZUNI TANLASH (Qo'shish/Ayirish...)
                    ↓
              5 TA SAVOL -> TEST
                    ↓
              NATIJA VA TAVSIYA ✅
                    ↓
              STATISTIKA SAQLANADI 📊
```

---

## 📁 LOYHA TUZILISHINI TUSHUNISH

| Fayl | Nima Uchun |
|------|-----------|
| **bot.py** | 🤖 Asl bot - Barcha ishlari buni qiladi |
| **database.py** | 💾 Yozilmalarni saqlanadi va oladi |
| **config.py** | ⚙️ Token va sozlamalar |
| **questions.json** | 📝 Test savollari (yangilash mumkin) |
| **requirements.txt** | 📦 Kerakli paketlar |
| **README_UZ.md** | 📖 Batafsilroq qo'llanma |
| **KENGAYTIRISH.md** | 🎁 Yangi xususiyatlar uchun kod |
| **test_bot.py** | ✅ Barcha narsa tekshirish |

---

## ❓ MUAMMOLAR VA YECHIMLAR

### ❌ "Bot ulanmayapti"

```
✓ config.py da TOKEN to'g'rimi? (bosmang copy-paste)
✓ Internet bor-yo'q?
✓ Token to'g'rimi? (@BotFather'dan yangilang)
```

### ❌ "Python topilmadi"

```bash
# O'rnatish:
# Windows: https://python.org dan o'rnating
# Mac: brew install python3
# Linux: sudo apt install python3
```

### ❌ "ImportError xatosi"

```bash
# Paketlarni qayta o'rnating:
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ "questions.json xatosi"

```
✓ JSON formatni tekshiring: jsonlint.com
✓ Kodlashuv UTF-8 ekaniga ishonch hosil qiling
```

---

## 📊 STATISTIKA NIMA?

Bot quyidagini saqlaydi:

```
📈 Test natijalarini     (To'g'ri/Noto'g'ri)
📊 Mavzu bo'yicha          (Qaysi mavzu yomon?)
📚 Taraqqiyot                (O'quvchi yaxshilanayapti?)
🎯 Tavsiyalar             (Nimani mashq qilish kerak?)
```

**DATABASE FILE: smartdars.db** (Avtomatik yaratiladi)

---

## 🎯 QADAM-BO'LAJON TEST IT

### Test 1: Asosiy
```bash
python test_bot.py
```
**Natija:** ✅ Barcha OK yoki ❌ Xato - ko'rsatiladi

### Test 2: Telegram'da
1. Bot username ini Telegram'da izlang
2. **/start ni bosing**
3. **Testni boshlang** ✅

---

## 🚀 KELLOQ MAQSADLAR

**BUGUN:**
- [x] Bot yaratish
- [x] Database sozlash
- [ ] TOKEN o'rnatish (SHUNING UCHUN!)

**ERTAGA:**
- [ ] Testni sinab ko'rish
- [ ] Yangi savolllar qo'shish
- [ ] Ota-onalarga bot ijosini yo'yish

**HAFTALIK:**
- [ ] Yangi fanlar qo'shish
- [ ] Statistikani tahlil qilish
- [ ] Ixtisosilar' fikrini olish

---

## 💡 MAXFIY FOYDALAR

🔓 **TOKEN ni xavfsiz saqlash:**
```bash
# .env fayliga qo'ying (ya'ni):
BOT_TOKEN=5921954XXX:AAH-a7Xda...

# Keyin config.py:
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
```

🔓 **Bot backup:**
```bash
# Muntazam smartdars.db nusxasini oling:
cp smartdars.db smartdars_backup_$(date +%Y%m%d).db
```

---

## 📞 YOKI'Z SAVOLLAR?

1. **README_UZ.md** - To'liq qo'llanma
2. **KENGAYTIRISH.md** - Yangi xususiyatlar
3. **Bot kodidagi # Kommentlar** - Tushuntirish

---

## 🏁 OXIRGI QADAM

```bash
# Terminalda:
python bot.py

# Telegram'da:
/start bo'sning

# OTASIGA AYTDIG ✅
```

---

**SmartDars - BOSHLANDI!** 🎓🌟
