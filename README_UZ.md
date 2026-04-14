# 🎓 SmartDars - O'quvchi Testlash Boti

O'ta-onalar uchun o'quvchi bilikni tekshiruvchi professional Telegram bot.

## 📋 Bot Xususiyatlari

✅ **Sinf va fanni tanlash** - 1-4 sinflar uchun mavjud  
✅ **Mavzu bo'yicha testlar** - Har fan uchun turli mavzular  
✅ **Avtomatik tekshirish** - Real-vaqtda natijalar  
✅ **Statistika** - Barcha natijalarni saqlanadi  
✅ **Tezkor interface** - Emoji va tugmalar bilan foydalanish oson  
✅ **SQLite Database** - Barcha ma'lumotlar xavfsiz saqlanadi  

---

## 🚀 O'rnatish

### 1. Python o'rnatish
```bash
# Python 3.8+ kerak
python --version
```

### 2. Repository klonlash yoki papkani yaratish
```bash
mkdir smartdars
cd smartdars
```

### 3. Virtual Environment yaratish (ixtiyoriy lekin tavsiya qilinadi)
```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 4. Kerakli paketlarni o'rnatish
```bash
pip install -r requirements.txt
```

### 5. Telegram Bot Token olish

- Telegram da [@BotFather](https://t.me/botfather) bilan suhbat qo'zing
- `/newbot` buyrug'ini kiriting
- Bot nomi va username kiriting
- Olingan **TOKEN**ni `config.py` fayliga qo'ying

```python
# config.py
TOKEN = "YOUR_ACTUAL_BOT_TOKEN"  # O'z tokeningizni qo'ying
```

### 6. Botni ishga tushirish
```bash
python bot.py
```

---

## 💬 Bot Buyruqlari

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Bot bilan ishlashni boshlash |
| `/test` | Yangi test boshlash |
| `/cancel` | Joriy operatsiyani bekor qilish |

---

## 📊 Bot Jarayoni

```
/start
   ↓
[Salomlashuv + tushuntirish]
   ↓
Sinf tanlash (1-4)
   ↓
Fan tanlash (Matematika, Ona tili)
   ↓
Mavzu tanlash (Qo'shish, Ayirish, Ko'paytirish...)
   ↓
5 ta savolga javob berish
   ↓
Natija ko'rsatish (% bilan)
   ↓
Yana test yoki Bosh menyu
```

---

## 📁 Loyha Tuzilishi

```
smartdars/
├── bot.py                 # Asosiy bot kodi
├── database.py            # Database operatsiyalari
├── config.py             # Konfiguratsiya (TOKEN va boshqalar)
├── questions.json        # Test savollari
├── requirements.txt      # Paket bog'liq vakollar
├── README.md            # Bu fayl
└── smartdars.db         # SQLite database (avtomatik yaratiladi)
```

---

## 🗄️ Database Struktura

### users
```
- id: Identifikator
- telegram_id: Telegram ID
- first_name: Ism
- last_name: Familiya
- created_at: Yaratilgan vaqt
```

### test_sessions
```
- id: Sessiya ID
- user_id: Foydalanuvchi ID
- sinf: Sinf (1, 2, 3, 4)
- fan: Fan (matematika, ona_tili)
- mavzu: Mavzu (qoshish, ayirish...)
- correct_answers: To'g'ri javoblar soni
- total_answers: Umumiy javoblar soni
- percentage: Foizda natija
- started_at: Boshlanish vaqti
- finished_at: Tugatish vaqti
```

### answers
```
- id: Javob ID
- session_id: Sessiya ID
- question_id: Savol ID
- selected_answer: Tanlangan javob
- is_correct: To'g'rimi?
```

### statistics
```
- id: ID
- user_id: Foydalanuvchi ID
- total_tests: Jami testlar
- correct_answers: To'g'ri javoblar
- wrong_answers: Noto'g'ri javoblar
- average_percentage: O'rtacha foiz
- last_test_at: Oxirgi test vaqti
```

---

## 📝 questions.json Format

```json
{
  "1": {
    "matematika": {
      "qoshish": [
        {
          "id": 1,
          "savol": "2 + 3 = ?",
          "variantlar": ["4", "5", "6", "7"],
          "togri": "5"
        }
      ]
    }
  }
}
```

### Struktura:
- **Sinf**: "1", "2", "3", "4"
- **Fan**: "matematika", "ona_tili" (va boshqalar)
- **Mavzu**: "qoshish", "ayirish", "kopaytirish" (va boshqalar)
- **Savol xossalari**:
  - `id`: Unikal raqam
  - `savol`: Savol matni
  - `variantlar`: 4 ta variant
  - `togri`: To'g'ri javob

---

## 🎯 Statistika Xususiyatlari

Bot quyidagini saqlab qoladi:

1. **Har test uchun natija**
   - Necha savolga javob berdi
   - Nechta to'g'ri javob
   - Foiqda natija

2. **Umumiy statistika**
   - Jami o'tgan testlar soni
   - O'rtacha ball
   - Eng yomon mavzular

3. **Fan bo'yicha statistika**
   - Fan bo'yicha o'rtacha ball
   - Eng yaxshi/yomon mavzular

---

## 🔧 Kengaytirish (Advanced)

### Yangi fan qo'shish
```python
# questions.json ga qo'shish:
{
  "1": {
    "fizika": {
      "harakat": [
        {"id": 26, "savol": "...", "variantlar": [...], "togri": "..."}
      ]
    }
  }
}
```

### Yangi mavzu qo'shish
```python
# questions.json ga qo'shish:
{
  "fan_nomi": {
    "mavzu_nomi": [
      {"id": X, "savol": "...", "variantlar": [...], "togri": "..."}
    ]
  }
}
```

### Admin paneli (Kelisini)
```python
# Foydalanuvchilarga statistika yuborish
# Test natijalarini tahlil qilish
# Yangi savolllarni qo'shish (bot ichida)
```

---

## 🐛 Muammolarni bartaraf qilish

### Bot ulanmayapti
```
✓ Tokenni to'g'ri kiritganingiz tekshiring
✓ Internet aloqasi bor-yo'q tekshiring
✓ BotFather'dan tokenni yangilang
```

### Database xatosi
```
✓ smartdars.db faylini o'chiring va qayta ishga tushiring
✓ SQLite o'rnatganingiz tekshiring
```

### questions.json xatosi
```
✓ JSON formatini tekshiring (jsonlint.com)
✓ Kodlashuv UTF-8 ekaniga ishonch hosil qiling
```

---

## 📈 O'tmis Rejalar (Future Plans)

- [ ] **Admin paneli** - Yangi savolllarni qo'shish
- [ ] **Grafik statistika** - Natijalarni visuallash
- [ ] **Tavsiyalar** - Kuchli bo'lmagan mavzularni tavsiya qilish
- [ ] **Gruppalar** - Bir nechta o'quvchi uchun
- [ ] **Ratinglar** - O'quvchilar o'rtasida musobaqalar
- [ ] **Audio/Video** - Mavzular uchun video qo'shish
- [ ] **Dinamik savolllar** - Qiynaliklari turli savolllar
- [ ] **Parent Dashboard** - Ota-onalar uchun veb-interfeyz

---

## 📞 Bog'lanish va Yordam

Agar muammoga duch kelsangiz yoki taklifingiz bo'lsa, menga yozing!

---

## 📜 Tarjima va Kengaytirish

Bot hozirda **O'zbek tilida** yozilgan. Boshqa tillarga tarjima qilish oson:

```python
# Faqat bot.py faylidagi string'larni o'zgartiring
# Masalan:
# "👋 Salom" → "👋 Привет" (Ruscha)
```

---

## ⚠️ Muhim Eslatmalar

1. **Token xavfsiyi** - Token fayl'ni Repository'ga yuklamang
2. **Database backup** - Muntazam `smartdars.db` ning zaxirasini oling
3. **questions.json** - Savolllarni muntazam yangilang
4. **Python versiyasi** - 3.8 yoki undan yuqori foydalaning

---

## 📄 Litsenziya

Bu priyekt **O'z shaxsiy ishlat** uchun qayta taqdim etilgan. Har qanday to'liq replika yoki nusxalashni o'z o'rniga qoldiring.

---

## 🎓 O'rganing va Kengaytiring!

Bu bot - **Python, Telegram API va SQLite** ni o'rganishning ajoyib usuli! Kodni o'zlashtiring va kengaytiring! 🚀

---

**SmartDars - Bilim qirg'oqlari uchun!** 🌟
