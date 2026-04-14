# ✨ SmartDars Bot - Kengaytirilgan Xususiyatlar

Bu fayl botni kengaytirish va yangilash uchun qo'shimcha kodlar va ideyalarni o'z ichiga oladi.

---

## 🎁 Qo'shimcha Kodlar (Copy & Paste)

### 1. Tavsiyalar Beradigan Xususiyat

Saqlang: **recommendations.py** sifatida

```python
from database import Database

class RecommendationEngine:
    """O'quvchi uchun mashq tavsiyalari"""
    
    def __init__(self):
        self.db = Database()
    
    def get_recommendations(self, user_id: int) -> list:
        """Yomon mavzuların tavsiyalarni olish"""
        weak_topics = self.db.get_weak_topics(user_id, limit=5)
        
        recommendations = []
        for topic in weak_topics:
            score = topic['average_percentage']
            attempts = topic['attempts']
            
            if score < 40:
                message = f"🔴 URGENT: {topic['mavzu']} ({score:.0f}%) - {attempts} marta turdi"
            elif score < 60:
                message = f"🟡 MASHQ: {topic['mavzu']} ({score:.0f}%) - Qayta o'rganib ko'ring"
            else:
                message = f"🟢 TO'LAQ: {topic['mavzu']} ({score:.0f}%)"
            
            recommendations.append(message)
        
        return recommendations
    
    def get_motivation_message(self, percentage: float) -> str:
        """Motivatsiya xabarlari"""
        motivations = {
            100: "🏆 AJOYIB! 100% - SIZ ULUG' INSONSIZ!",
            90: "🌟 SUPER! 90% - Davom eting, shuningdek!",
            80: "⭐ YAXSHI! 80% - Mamlakotda ikkinchi qadam!",
            70: "👍 OCHA! 70% - Shoq bormi, yaxshilanadi",
            60: "💪 ORTA! 60% - Ko'proq mashq kifoya - siz qilasiz!",
            0: "📚 BOSHLANG! Hoziroq! Boshqa urinib ko'ring",
        }
        
        if percentage >= 90:
            return motivations[90]
        elif percentage >= 80:
            return motivations[80]
        elif percentage >= 70:
            return motivations[70]
        elif percentage >= 60:
            return motivations[60]
        else:
            return motivations[0]
```

### 2. Notifjikasiya Sistemi

```python
# bot.py ichiga qo'shish

async def send_daily_reminder(application: Application):
    """Har kuni estutirish"""
    from database import Database
    
    db = Database()
    conn = sqlite3.connect(db.db_name)
    cursor = conn.cursor()
    
    # Oxirgi 3 kundan testi bo'lmaganlari
    cursor.execute('''
        SELECT DISTINCT telegram_id 
        FROM users 
        WHERE id NOT IN (
            SELECT DISTINCT user_id 
            FROM test_sessions 
            WHERE datetime(started_at) >= datetime('now', '-3 days')
        )
    ''')
    
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        try:
            await application.bot.send_message(
                chat_id=user[0],
                text="🔔 *SmartDars oromdan xabar*\n\n"
                     "Burun test o'tmaganingiz ekanini ko'rdik. "
                     "O'quvchi bilikni tekshiruvni boshlang!\n"
                     "Nimani ekanini bilib olaling? 😊\n\n"
                     "/test ni bosing!",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
```

### 3. Leaderboard (Reyting)

```python
# database.py ga qo'shish

def get_top_students(self, fan: str = None, limit: int = 10) -> List[Dict]:
    """Eng yaxshi o'quvchilar"""
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    
    if fan:
        query = '''
            SELECT 
                u.first_name,
                AVG(ts.percentage) as avg_score,
                COUNT(ts.id) as tests_taken
            FROM users u
            JOIN statistics s ON u.telegram_id = s.user_id
            JOIN test_sessions ts ON u.telegram_id = ts.user_id
            WHERE ts.fan = ?
            GROUP BY u.telegram_id
            ORDER BY avg_score DESC
            LIMIT ?
        '''
        cursor.execute(query, (fan, limit))
    else:
        query = '''
            SELECT 
                u.first_name,
                s.average_percentage,
                s.total_tests
            FROM users u
            JOIN statistics s ON u.telegram_id = s.user_id
            ORDER BY s.average_percentage DESC
            LIMIT ?
        '''
        cursor.execute(query, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    leaderboard = []
    for i, row in enumerate(results, 1):
        leaderboard.append({
            'rank': i,
            'name': row[0],
            'score': row[1],
            'tests': row[2] if len(row) > 2 else None
        })
    
    return leaderboard
```

### 4. Progress Grafiki

```python
# analysis.py

def generate_progress_chart(user_id: int) -> str:
    """ASCII grafik"""
    db = Database()
    sessions = db.get_test_sessions(user_id, limit=10)
    
    if not sessions:
        return "Hali test o'tmagansiz"
    
    chart = "📈 *SIZNING RIVOJLANISHINGIZ*\n\n"
    
    for session in reversed(sessions):
        percentage = session['percentage']
        bars = int(percentage / 10)
        chart += f"{'█' * bars}{'░' * (10 - bars)} {percentage:.0f}% - {session['mavzu']}\n"
    
    return chart
```

### 5. Export statistika

```python
# reporting.py

import json
from datetime import datetime

def export_user_data(user_id: int) -> dict:
    """Foydalanuvchi ma'lumotlarini export"""
    db = Database()
    
    stats = db.get_user_statistics(user_id)
    sessions = db.get_test_sessions(user_id, limit=100)
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'user_id': user_id,
        'statistics': stats,
        'test_sessions': sessions,
        'weak_topics': db.get_weak_topics(user_id, limit=10)
    }
    
    # JSON sifatida saqlash
    filename = f"smartdars_export_{user_id}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    return filename
```

---

## 🛠️ Kodga Qo'shimchalar

### Bot.py ga qo'shish:

```python
# handlers oqiba

# Statistics handler
async def detailed_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Batafsil statistika"""
    user_id = update.effective_user.id
    
    stats = db.get_user_statistics(user_id)
    
    if not stats['total_tests']:
        await update.message.reply_text("📊 Hali test o'tmagansiz!")
        return
    
    # Fan bo'yicha statistika
    all_fans = ['matematika']
    detailed = ""
    
    for fan in all_fans:
        fan_stats = db.get_statistics_by_subject(user_id, fan)
        if fan_stats['total']:
            detailed += f"📖 *{fan.upper()}* ({fan_stats['total']} test)\n"
            detailed += f"  O'rtacha: {fan_stats['average_percentage']:.1f}%\n"
            detailed += f"  Ajoyib(80%+): {fan_stats['excellent']}\n"
            detailed += f"  Yaxshi(60-80%): {fan_stats['good']}\n"
            detailed += f"  Mashq(60%-): {fan_stats['poor']}\n\n"
    
    await update.message.reply_text(
        detailed or "Ma'lumot yok",
        parse_mode=ParseMode.MARKDOWN
    )
```

---

## 📊 Veb Dashboard (Flask)

Agar veb-interface qilishni xohlasangiz:

**Fayl: dashboard.py**

```python
from flask import Flask, render_template, request
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user/<int:user_id>/stats')
def get_stats(user_id):
    stats = db.get_user_statistics(user_id)
    return stats

@app.route('/api/user/<int:user_id>/sessions')
def get_sessions(user_id):
    sessions = db.get_test_sessions(user_id)
    return sessions

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🔐 Xavfsizlik

### 1. Token xavfsiyi
```python
# .env fayliga qo'shish
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
```

### 2. Rate limiting
```python
from telegram.ext import ApplicationBuilder

app = ApplicationBuilder()\
    .token(TOKEN)\
    .rate_limiter(AIORateLimiter())\
    .build()
```

### 3. Input validation
```python
def is_valid_answer(answer: str) -> bool:
    """Javobni tekshirish"""
    return len(answer) > 0 and len(answer) <= 100
```

---

## 📱 Mobile App (Qo'shimcha)

```python
# API endpoint
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/tests/<sinf>')
def get_tests(sinf):
    with open('questions.json') as f:
        questions = json.load(f)
    return jsonify(questions.get(sinf, {}))
```

---

## 🚀 Deploy (Deployment)

### Heroku'ga joylashtirish:

```bash
# Procfile
web: python bot.py

# Runtime python
python-3.9.13
```

### VPS'ga joylashtirish:

```bash
# systemd service
[Unit]
Description=SmartDars Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/smartdars
ExecStart=/usr/bin/python3 /home/ubuntu/smartdars/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📚 Foydalanish Misolllari

### Yangi mavzu qo'shish:
```python
questions_data = {
    "1": {
        "matematika": {
            "minus": [
                {
                    "id": 26,
                    "savol": "10 - 3 = ?",
                    "variantlar": ["5", "6", "7", "8"],
                    "togri": "7"
                }
            ]
        }
    }
}
```

### Yangi fan qo'shish:
```python
questions_data = {
    "1": {
        "fizika": {
            "harakat": [
                {
                    "id": 100,
                    "savol": "Ishqalanish nima?",
                    "variantlar": ["O'sish", "Harakatlanish", "Kuchin", "Yo'llanish"],
                    "togri": "Harakatlanish"
                }
            ]
        }
    }
}
```

---

## 🎯 Oylik Harekat Rejalari

**Haftalik maqsadlar:**
- Hafta 1: Asosiy bot yaratish ✅
- Hafta 2: Database va statistika ✅
- Hafta 3: Admin paneli
- Hafta 4: Veb dashboard

**Oylik maqsadlar:**
- Ayliq: Tajariba testlash
- 2-oy: Yangi fanlar qo'shish
- 3-oy: Mobile app
- 4-oy: Deploy va promotion

---

**SmartDars - Bilimni zarafgan yaqinda ko'tariladi! 🌟**
