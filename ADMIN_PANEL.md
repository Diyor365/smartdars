# 👨‍💼 SmartDars Bot - ADMIN PANEL QOLLANMASI

Admin paneli orqali bot uchun yangi savolllar qo'shish, o'chirish va boshqarish!

---

## 🔐 ADMIN BO'LISH

### QADAM 1: O'z Telegram ID'ni Olish

```
1. Telegram: @userinfobot'ga yozing
2. /start bo'sing
3. "User ID"ni ko'ring (Masalan: 123456789)
```

### QADAM 2: config.py ni Tahrirlash

```python
# OLD:
ADMIN_ID = None

# NEW (o'z ID'ng):
ADMIN_ID = 123456789  # O'z raqamingizni kiriting
```

**Yoki, bir nechta adminlar:**

```python
ADMIN_IDS = [123456789, 987654321, 555555555]
```

### QADAM 3: Bot Qayta Ishga Tushirish

```bash
python bot.py
```

---

## 🚀 ADMIN PANEL'GA KIRISH

Telegram bot'da:

```
/admin
```

**Yoki qiymat yoki tugmalar orqali:**

```
👨‍💼 ADMIN PANEL
├─ ➕ Savol qo'shish
├─ 🔍 Savol izlash
├─ 📊 Statistika
├─ 📥 Import/Export
├─ ⚙️ Admin boshqarish
└─ 🚪 Chiqish
```

---

## 📝 YANGI SAVOL QO'SHISH

### Qadam-bo'lajon

**1. "➕ Savol qo'shish" ni bosing**

```
📚 Savol qo'shish boshlandi!

Qaysi sinfga savol qo'shmoqchisiz? (1, 2, 3, 4)
```

**2. Sinfni kiriting** (1, 2, 3 yoki 4)

```
(O'rni: 1)

✅ 1-sinf tanlandi!

📖 Qaysi fanin savblni qo'shmoqchisiz?
   • matematika
   • ona_tili

(Yangi fan nomini kiriting yoki mavjud fanni tanlang)
```

**3. Fan nomini kiriting**

```
(O'rni: matematika)

✅ matematika fani tanlandi!

📝 Qaysi mavzuya savol qo'shmoqchisiz?
   • qoshish
   • ayirish
   • kopaytirish

(Yangi mavzu nomini kiriting yoki mavjud mavzuni tanlang)
```

**4. Mavzu nomini kiriting**

```
(O'rni: bolish)

✅ bolish mavzusi tanlandi!

❓ Savol matnini kiriting:
```

**5. Savol matnini kiriting**

```
(O'rni: 10 + 5 = ?)

✅ Savol saqlandi

4 ta variant kiriting (bitta-bitta):

(Variant 1):
```

**6. 4 ta variant kiriting**

```
(O'rni: 15)
✅ Variant saqlandi (1 / 4)

(Variant 2):
(O'rni: 16)
✅ Variant saqlandi (2 / 4)

(Variant 3):
(O'rni: 17)
✅ Variant saqlandi (3 / 4)

(Variant 4):
(O'rni: 18)
✅ Variant saqlandi (4 / 4)
```

**7. To'g'ri javobni tanlang**

```
✅ Barcha variantlar saqlandi

1. 15
2. 16 
3. 17
4. 18

Qaysi variant to'g'ri javob? (1, 2, 3 yoki 4):
(O'rni: 1)
```

**8. Tasdiqlang**

```
📝 SAVOL XULOSA

Sinf: 1
Fan: matematika
Mavzu: bolish

❓ 10 + 5 = ?

1. 15 ✅
2. 16
3. 17
4. 18

Ko'rik va tasdiqlang (ha/yo'q):
(O'rni: ha)

✅ Savol qo'shish boshlandi!
🎉 Savol muvaffaqiyatli qo'shildi!
```

**questions.json avtomatik yangilanadi!** ✅

---

## 🔍 SAVOL IZLASH

### Qo'llash

```
"🔍 Savol izlash" ni bosing

🔍 Izlanish uchun so'z kiriting:
(Masalan: "bolish" yoki "10")

(O'rni: bolish)
```

**Natija:**

```
🔍 QIDIRUVNING NATIJALARI (3 ta)

ID: 19 | 3-sinf | matematika | bolish
❓ 12 ÷ 3 = ?

ID: 20 | 3-sinf | matematika | bolish
❓ 20 ÷ 5 = ?

ID: 21 | 3-sinf | matematika | bolish
❓ 18 ÷ 6 = ?
```

---

## 📊 STATISTIKA

"📊 Statistika" ni bosing:

```
📊 SAVOLLLAR STATISTIKASI

📚 1-sinf
  📖 matematika/qoshish: 5 ta savol
  📖 matematika/ayirish: 3 ta savol
  📖 matematika/kopaytirish: 2 ta savol
  📊 matematika: 10 ta savol

📚 2-sinf
  📖 matematika/qoshish: 3 ta savol
  📖 matematika/ayirish: 2 ta savol
  📖 matematika/kopaytirish: 3 ta savol
  📖 matematika/bolish: 2 ta savol
  📊 matematika: 10 ta savol

UMUMIY STATISTIKA
• Sinflar: 4
• Fanlar: 2
• Mavzular: 8
• Jami savolllar: 25
```

---

## 📥 IMPORT/EXPORT

### Export (Backup)

questions.json faylini backup qilish:

```bash
# questions.json avtomatik backup
# Vaqtlik: questions_backup_20260413_153045.json
```

### Import (Qayta yuklash)

Backup dari questions.json faylini qayta yuklash:

```
"📥 Import" ni bosing

backup.json faylini tanlang va import qiling
```

---

## ⚙️ ADMINISTRATOR BOSHQARISH

Admin bo'lmagan foydalanuvchilari admin qilish (faqat super-admin):

```
"⚙️ Admin boshqarish" ni bosing

Admin qo'shish uchun USER_ID kiriting:
(O'rni: 987654321)

✅ User 987654321 admin qilinidi
```

---

## 📋 ADMIN COMMANDS

| Buyruq | Tavsif |
|--------|--------|
| `/admin` | Admin paneli |
| `/admin_stats` | Statistika |
| `/admin_add` | Savol qo'shish |
| `/admin_search <so'z>` | Savol izlash |
| `/admin_export` | Backup |

---

## 🛠️ ADMIN.PY - PYTHON KODIDA

Admin panel Python kodida qo'llash:

```python
from admin import AdminPanel

admin = AdminPanel()

# Admin'ni tekshirish
if admin.is_admin(user_id):
    print("U admin!")

# Savol qo'shish
question_data = {
    'sinf': '1',
    'fan': 'matematika',
    'mavzu': 'qoshish',
    'savol': '2 + 2 = ?',
    'variantlar': ['3', '4', '5', '6'],
    'togri': '4'
}
success, msg = admin._add_question_to_data(question_data)

# Statistika
stats = admin.get_statistics()
print(stats)

# Qidiruv
results = admin.search_questions("qoshish")
```

---

## ⚠️ MUHIM ESLATMALAR

### Xavfsizlik

```
🔐 ADMIN_ID secret!
❌ GitHub'ga config.py yuklamang
❌ TOKEN public bo'lmasin
✅ .gitignore da mavjud
```

### Default Questions

```
questions.json hozirda:
✅ 4 sinf
✅ 2 fan (matematika)
✅ 8 mavzu
✅ 25 savol
```

### JSON Format

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

---

## 🐛 MUAMMOLAR VA YECHIMI

### ❌ "Siz admin emassiz!"

```
✓ config.py da ADMIN_ID to'g'rimi?
✓ Telegram ID'ni @userinfobot dan tekshiring
✓ Bot qayta ishga tushiring (python bot.py)
```

### ❌ "Savol qo'shilmadi"

```
✓ Barcha qadamlarni to'g'ri kiriting
✓ Variantlarni aniq tanlang
✓ JSON format tekshiring
```

### ❌ "questions.json yangilanmadi"

```
✓ Fayl permissions'ni tekshiring
✓ Disk spa'si xavfsiz ekaniga ishonch hosil qiling
✓ Python proceflora yetarli ruhsat bor
```

---

## 🎓 MISOLLAR

### 1-sinf, Matematika, Qo'shish:

```
❓ 3 + 4 = ?
1. 6
2. 7 ✅
3. 8
4. 9
```

### 2-sinf, Ona tili, O'qish:

```
❓ "Qush" so'zi nechta harfdan iborat?
1. 3
2. 4 ✅
3. 5
4. 6
```

### 3-sinf, Matematika, Bolish:

```
❓ 15 ÷ 3 = ?
1. 4
2. 5 ✅
3. 6
4. 7
```

---

## 📱 ANDROID/iOS'DAN

Telegram mobile'dan:

```
1. Bot'a bosing: @smartdars_bot
2. /admin yozing
3. Tugmalarni bosing
4. Savollar qo'shing
```

**SO'LADI!** ✨

---

## 🚀 KENGAYTIRILGAN XUSUSIYATLAR

```
Hozir:           Kelajakda:
─────           ──────────
✅ Savol qo'shish    ✅ Bulk import
✅ Savol izlash      ✅ Savol o'chirish
✅ Statistika        ✅ Savol tahrirlash
✅ Import/Export     ✅ Video qo'shish
✅ Admin boshqarish  ✅ PDF export
                     ✅ Excel import
```

---

## 📞 ADMIN SUPPORT

Agar muammo bo'lsa:

1. **ADMIN_PANEL.md** - Bu fayl
2. **KENGAYTIRISH.md** - Kodo'shish
3. **README_UZ.md** - Asosiy qo'llanma
4. **admin.py** - Source kod

---

## 🎁 TIPS & TRICKS

### Tezkor qo'shish (Python CLI)

```python
# admin_add_questions.py
from admin import AdminPanel

admin = AdminPanel()

# Ko'plab savolllar qo'shish
questions_list = [
    {'sinf': '1', 'fan': 'matematika', 'mavzu': 'qoshish', ...},
    {'sinf': '1', 'fan': 'matematika', 'mavzu': 'qoshish', ...},
]

for q in questions_list:
    admin._add_question_to_data(q)
```

### Backup Avtomatik

```bash
# Kundalik backup
0 2 * * * cp questions.json questions_backup_$(date +\%Y\%m\%d).json
```

### Admin Grupp

```
Bir nechta admin'ni config.py ga qo'shing:
ADMIN_IDS = [123456789, 987654321, 555555555]
```

---

**Admin Panel - Savolllarni boshqarish oson qilish!** 👨‍💼✨

---

*SmartDars Admin Panel - Professional savol boshqarish sistemi!* 🎓
