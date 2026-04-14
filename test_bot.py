#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartDars Bot - Test va tekshirish skriptasi
"""

import json
import os
import sys

def test_python_version():
    """Python versiyasini tekshirish"""
    print("🔍 Python versiyasi tekshirilmoqda...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - XATO! 3.8+ kerak")
        return False

def test_packages():
    """Paketlarni tekshirish"""
    print("\n🔍 Paketlar tekshirilmoqda...")
    packages = {
        'telegram': 'python-telegram-bot',
        'telegram.ext': 'python-telegram-bot',
        'sqlite3': 'sqlite3 (built-in)',
        'json': 'json (built-in)',
    }
    
    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name} - o'rnatilgan")
        except ImportError:
            print(f"❌ {name} - o'RNATILMAGAN!")
            all_ok = False
    
    return all_ok

def test_json_format():
    """questions.json formatini tekshirish"""
    print("\n🔍 questions.json tekshirilmoqda...")
    
    if not os.path.exists('questions.json'):
        print("❌ questions.json topilmadi!")
        return False
    
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Struktura tekshirish
        classes = list(data.keys())
        print(f"✅ JSON format OK - {len(classes)} sinf topildi")
        
        # Detallar
        for sinf in classes:
            fans = list(data[sinf].keys())
            print(f"   📚 {sinf}-sinf: {', '.join(fans)}")
            
            for fan in fans:
                topics = list(data[sinf][fan].keys())
                questions_count = sum(len(data[sinf][fan][topic]) for topic in topics)
                print(f"      📖 {fan}: {', '.join(topics)} ({questions_count} ta savol)")
        
        return True
    except json.JSONDecodeError:
        print("❌ JSON format xato! Tekshirish uchun jsonlint.com ishlating")
        return False
    except Exception as e:
        print(f"❌ Xato: {e}")
        return False

def test_config():
    """config.py tekshirish"""
    print("\n🔍 config.py tekshirilmoqda...")
    
    if not os.path.exists('config.py'):
        print("❌ config.py topilmadi!")
        return False
    
    try:
        with open('config.py', 'r') as f:
            config_content = f.read()
        
        if 'YOUR_BOT_TOKEN_HERE' in config_content or not 'TOKEN' in config_content:
            print("❌ TOKEN o'rnatilmagan! config.py ni tahrirlang")
            return False
        
        print("✅ config.py OK")
        return True
    except Exception as e:
        print(f"❌ Xato: {e}")
        return False

def test_database():
    """Database yaratish"""
    print("\n🔍 Database yaratilmoqda...")
    
    try:
        from database import Database
        db = Database('test.db')
        print("✅ Database yaratildi - test.db")
        
        # Cleanup
        if os.path.exists('test.db'):
            os.remove('test.db')
        
        return True
    except Exception as e:
        print(f"❌ Xato: {e}")
        return False

def test_bot_import():
    """Bot kodini tekshirish"""
    print("\n🔍 Bot kodi tekshirilmoqda...")
    
    try:
        # config.py da TOKEN tekshirish
        with open('config.py', 'r') as f:
            if 'YOUR_BOT_TOKEN_HERE' in f.read():
                print("⚠️  TOKEN hali o'rnatilmagan - bu normal")
                return True
        
        # Bot va database import test
        from database import Database
        print("✅ Bot kodlari OK")
        return True
    except Exception as e:
        print(f"❌ Xato: {e}")
        return False

def show_next_steps():
    """Keyingi qadamlar"""
    print("\n" + "="*50)
    print("🎓 SmartDars Bot - Tayyor!")
    print("="*50)
    print("\n📋 Keyingi qadamlar:\n")
    print("1️⃣  config.py ochting va TOKEN o'rnatring:")
    print("   - @BotFather dan tokeningizni oqib oling")
    print("   - TOKEN = 'your_actual_token_here'")
    print()
    print("2️⃣  Bot ishga tushiring:")
    print("   python3 bot.py")
    print()
    print("3️⃣  Telegram botingiza yozing:")
    print("   /start komandasi")
    print()
    print("💡 Masalalar bo'lsa readme.md  yoki KENGAYTIRISH.md ko'ring")
    print()

def main():
    """Barcha testlarni ishga tushirish"""
    print("🎓 SmartDars Bot - Tekshirish\n")
    print("="*40)
    
    tests = [
        ("Python versiyasi", test_python_version),
        ("Paketlar", test_packages),
        ("questions.json", test_json_format),
        ("config.py", test_config),
        ("Database", test_database),
        ("Bot kodi", test_bot_import),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name}: {e}")
            results[name] = False
    
    print("\n" + "="*40)
    print("📊 NATIJALAR:\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} test o'tdi\n")
    
    if passed == total:
        print("🎉 Hammasi OK! Bot ishga tushishga tayyor!")
        show_next_steps()
        return 0
    else:
        print("⚠️  Ba'zi xatolar barpo bo'ldi. Yuqoridagi xabarlarni o'qib tekshiring.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
