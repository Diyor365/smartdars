"""
SmartDars Bot - Admin Panel
Admin'lar orqali yangi savolllar qo'shish va boshqarish
"""

import json
import os
from typing import Dict, List, Tuple
from datetime import datetime
from config import ADMIN_ID

class AdminPanel:
    """Admin panel uchun main class"""
    
    def __init__(self, questions_file='questions.json'):
        self.questions_file = questions_file
        self.load_questions()
        self.temp_data = {}  # Vaqtinchalik admin ma'lumotlari
    
    def load_questions(self):
        """questions.json yuklash"""
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            self.questions = {}
    
    def save_questions(self):
        """questions.json saqlash"""
        try:
            with open(self.questions_file, 'w', encoding='utf-8') as f:
                json.dump(self.questions, f, ensure_ascii=False, indent=2)
            return True, "✅ Savolllar saqlandi!"
        except Exception as e:
            return False, f"❌ Xato: {e}"
    
    def is_admin(self, user_id: int) -> bool:
        """Admin ekanligini tekshirish"""
        # Hozircha faqat config.py da ADMIN_ID ni tekshiramiz
        if ADMIN_ID and user_id == ADMIN_ID:
            return True
        # Yoki yangi adda qo'shimcha admin ID'larni qo'shish mumkin
        return user_id in self.get_admin_ids()
    
    def get_admin_ids(self) -> List[int]:
        """Admin ID'larni olish"""
        # Foydalanuvchi qo'shilgan adminlar
        try:
            with open('admins.json', 'r') as f:
                admins = json.load(f)
                return admins.get('admin_ids', [])
        except:
            return []
    
    def add_admin(self, user_id: int) -> Tuple[bool, str]:
        """Yangi admin qo'shish"""
        admins = self.get_admin_ids()
        if user_id not in admins:
            admins.append(user_id)
            try:
                with open('admins.json', 'w') as f:
                    json.dump({'admin_ids': admins}, f)
                return True, f"✅ User {user_id} admin qilinidi"
            except Exception as e:
                return False, f"❌ Xato: {e}"
        return False, "⚠️  Bu user allaqachon admin"
    
    def remove_admin(self, user_id: int) -> Tuple[bool, str]:
        """Adminni o'chirish"""
        admins = self.get_admin_ids()
        if user_id in admins:
            admins.remove(user_id)
            try:
                with open('admins.json', 'w') as f:
                    json.dump({'admin_ids': admins}, f)
                return True, f"✅ User {user_id} adminlikdan chiqarildi"
            except Exception as e:
                return False, f"❌ Xato: {e}"
        return False, "⚠️  Bu user admin emas"
    
    # ==================== SAVOL QO'SHISH ====================
    
    def init_add_question(self, user_id: int) -> str:
        """Savol qo'shish protsesini boshlash"""
        self.temp_data[user_id] = {
            'step': 'sinf',
            'data': {}
        }
        return "📚 Savol qo'shish boshlandi!\n\nQaysi sinfga savol qo'shmoqchisiz? (1, 2, 3, 4)"
    
    def get_available_classes(self) -> List[str]:
        """Mavjud sinflarni olish"""
        return list(self.questions.keys())
    
    def get_available_subjects(self, sinf: str) -> List[str]:
        """Sinfning fanlarini olish"""
        if sinf in self.questions:
            return list(self.questions[sinf].keys())
        return []
    
    def get_available_topics(self, sinf: str, fan: str) -> List[str]:
        """Fan uchun mavju'larni olish"""
        if sinf in self.questions and fan in self.questions[sinf]:
            return list(self.questions[sinf][fan].keys())
        return []
    
    def add_question_step(self, user_id: int, input_text: str) -> Tuple[str, bool]:
        """Savol qo'shish qadamlarini bajaring"""
        if user_id not in self.temp_data:
            return "❌ Savol qo'shish boshlang! /add_question", False
        
        data = self.temp_data[user_id]
        step = data['step']
        question_data = data['data']
        
        # SINF TANLASH
        if step == 'sinf':
            if input_text not in ['1', '2', '3', '4']:
                return "❌ Sinfni to'g'ri kiriting (1, 2, 3 yoki 4)", False
            
            question_data['sinf'] = input_text
            data['step'] = 'fan'
            
            fans = self.get_available_subjects(input_text)
            fans_text = "\n".join([f"   • {f}" for f in fans]) if fans else "   Hali fan yo'q"
            
            return f"✅ {input_text}-sinf tanlandi\n\n📖 Qaysi fanin savblni qo'shmoqchisiz?\n{fans_text}\n\n(Yangi fan nomini kiriting yoki mavjud fanni tanlang)", False
        
        # FAN TANLASH
        elif step == 'fan':
            question_data['fan'] = input_text.lower()
            data['step'] = 'mavzu'
            
            topics = self.get_available_topics(question_data['sinf'], question_data['fan'])
            topics_text = "\n".join([f"   • {t}" for t in topics]) if topics else "   Hali mavzu yo'q"
            
            return f"✅ {input_text} fani tanlandi\n\n📝 Qaysi mavzuya savol qo'shmoqchisiz?\n{topics_text}\n\n(Yangi mavzu nomini kiriting yoki mavjud mavzuni tanlang)", False
        
        # MAVZU TANLASH
        elif step == 'mavzu':
            question_data['mavzu'] = input_text.lower()
            data['step'] = 'question'
            
            return f"✅ {input_text} mavzusi tanlandi\n\n❓ Savol matnini kiriting:", False
        
        # SAVOL MATNI
        elif step == 'question':
            question_data['savol'] = input_text
            data['step'] = 'variants'
            question_data['variantlar'] = []
            
            return "✅ Savol saqlandi\n\n4 ta variant kiriting (bitta-bitta):\n\n(Variant 1):", False
        
        # VARIANTLAR
        elif step == 'variants':
            if len(question_data['variantlar']) < 4:
                question_data['variantlar'].append(input_text)
                remaining = 4 - len(question_data['variantlar'])
                
                if remaining > 0:
                    return f"✅ Variant saqlandi\n\n({len(question_data['variantlar'])} / 4)\n\n(Variant {len(question_data['variantlar']) + 1}):", False
                else:
                    data['step'] = 'correct'
                    variants_text = "\n".join([f"{i+1}. {v}" for i, v in enumerate(question_data['variantlar'])])
                    return f"✅ Barcha variantlar saqlandi\n\n{variants_text}\n\nQaysi variant to'g'ri javob? (1, 2, 3 yoki 4):", False
        
        # TO'G'RI JAVOB
        elif step == 'correct':
            try:
                correct_idx = int(input_text) - 1
                if correct_idx < 0 or correct_idx >= 4:
                    return "❌ Raqamni 1-4 orasida kiriting", False
                
                question_data['togri'] = question_data['variantlar'][correct_idx]
                data['step'] = 'confirm'
                
                # To'liq savol
                question_text = (
                    f"📝 *SAVOL XULOSA*\n\n"
                    f"Sinf: {question_data['sinf']}\n"
                    f"Fan: {question_data['fan']}\n"
                    f"Mavzu: {question_data['mavzu']}\n\n"
                    f"❓ {question_data['savol']}\n\n"
                )
                for i, var in enumerate(question_data['variantlar'], 1):
                    marker = "✅" if var == question_data['togri'] else "  "
                    question_text += f"{i}. {var} {marker}\n"
                
                question_text += "\n\nKo'rik va tasdiqlang (ha/yo'q):"
                
                return question_text, False
            except:
                return "❌ Raqamni kiriting (1, 2, 3 yoki 4)", False
        
        # TASDIQLAB
        elif step == 'confirm':
            if input_text.lower() in ['ha', 'yes', 'ok', '✅']:
                # Savol qo'shish
                success, msg = self._add_question_to_data(question_data)
                
                if success:
                    del self.temp_data[user_id]
                    return f"✅ {msg}\n\n🎉 Savol muvaffaqiyatli qo'shildi!" , True
                else:
                    return f"❌ {msg}", False
            
            elif input_text.lower() in ['yo\'q', 'no', 'cancel']:
                del self.temp_data[user_id]
                return "❌ Savol qo'shish bekor qilindi", True
            
            else:
                return "ha yoki yo'q kiriting", False
        
        return "❌ Xato!", False
    
    def _add_question_to_data(self, question_data: Dict) -> Tuple[bool, str]:
        """Savolni ma'lumotlarga qo'shish"""
        sinf = question_data['sinf']
        fan = question_data['fan']
        mavzu = question_data['mavzu']
        
        try:
            # Sinf yo'q bo'lsa yaratish
            if sinf not in self.questions:
                self.questions[sinf] = {}
            
            # Fan yo'q bo'lsa yaratish
            if fan not in self.questions[sinf]:
                self.questions[sinf][fan] = {}
            
            # Mavzu yo'q bo'lsa yaratish
            if mavzu not in self.questions[sinf][fan]:
                self.questions[sinf][fan][mavzu] = []
            
            # Savol ID'sini olish
            max_id = 0
            for s in self.questions.values():
                for f in s.values():
                    for t in f.values():
                        for q in t:
                            if q.get('id', 0) > max_id:
                                max_id = q['id']
            
            new_id = max_id + 1
            
            # Yangi savol
            new_question = {
                'id': new_id,
                'savol': question_data['savol'],
                'variantlar': question_data['variantlar'],
                'togri': question_data['togri']
            }
            
            self.questions[sinf][fan][mavzu].append(new_question)
            
            # Saqlash
            success, msg = self.save_questions()
            if success:
                return True, f"Savol ID: {new_id}"
            else:
                return False, msg
        
        except Exception as e:
            return False, str(e)
    
    # ==================== SAVOL O'CHIRISH ====================
    
    def delete_question(self, sinf: str, fan: str, mavzu: str, question_id: int) -> Tuple[bool, str]:
        """Savolni o'chirish"""
        try:
            if sinf in self.questions and fan in self.questions[sinf] and mavzu in self.questions[sinf][fan]:
                questions = self.questions[sinf][fan][mavzu]
                
                for i, q in enumerate(questions):
                    if q['id'] == question_id:
                        questions.pop(i)
                        
                        # Agar mavzu bo'sh bo'lsa o'chirish
                        if not questions:
                            del self.questions[sinf][fan][mavzu]
                        
                        # Agar fan bo'sh bo'lsa o'chirish
                        if not self.questions[sinf][fan]:
                            del self.questions[sinf][fan]
                        
                        # Saqlash
                        success, msg = self.save_questions()
                        return success, msg
            
            return False, "❌ Savol topilmadi"
        except Exception as e:
            return False, f"❌ Xato: {e}"
    
    # ==================== STATISTIKA ====================
    
    def get_statistics(self) -> str:
        """Board statistikasini ol8sh"""
        total_questions = 0
        classes_count = len(self.questions)
        subjects_count = 0
        topics_count = 0
        
        stats = "📊 *SAVOLLLAR STATISTIKASI*\n\n"
        
        for sinf in self.questions:
            stats += f"📚 *{sinf}-sinf*\n"
            for fan in self.questions[sinf]:
                subjects_count += 1
                fan_questions = 0
                
                for mavzu in self.questions[sinf][fan]:
                    topics_count += 1
                    topic_count = len(self.questions[sinf][fan][mavzu])
                    fan_questions += topic_count
                    total_questions += topic_count
                    
                    stats += f"  📖 {fan}/{mavzu}: {topic_count} ta savol\n"
                
                stats += f"  📊 {fan}: {fan_questions} ta savol\n\n"
        
        stats += f"\n*UMUMIY STATISTIKA*\n"
        stats += f"• Sinflar: {classes_count}\n"
        stats += f"• Fanlar: {subjects_count}\n"
        stats += f"• Mavzular: {topics_count}\n"
        stats += f"• Jami savolllar: {total_questions}"
        
        return stats
    
    # ==================== EXPORT/IMPORT ====================
    
    def export_questions(self, format='json') -> Tuple[bool, str]:
        """Savolllarni export qilish"""
        try:
            if format == 'json':
                filename = f"questions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.questions, f, ensure_ascii=False, indent=2)
                return True, f"✅ Export: {filename}"
            
            return False, "❌ Format notog'ri"
        except Exception as e:
            return False, f"❌ Xato: {e}"
    
    def import_questions(self, filename: str) -> Tuple[bool, str]:
        """Savolllarni import qilish"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            # Merge qilish
            for sinf in imported:
                if sinf not in self.questions:
                    self.questions[sinf] = {}
                
                for fan in imported[sinf]:
                    if fan not in self.questions[sinf]:
                        self.questions[sinf][fan] = {}
                    
                    for mavzu in imported[sinf][fan]:
                        if mavzu not in self.questions[sinf][fan]:
                            self.questions[sinf][fan][mavzu] = []
                        
                        self.questions[sinf][fan][mavzu].extend(imported[sinf][fan][mavzu])
            
            # Saqlash
            success, msg = self.save_questions()
            return success, "✅ Import qilindi" if success else msg
        
        except Exception as e:
            return False, f"❌ Xato: {e}"
    
    # ==================== QIDIRUV ====================
    
    def search_questions(self, query: str) -> str:
        """Savolllarni izlash"""
        results = []
        query_lower = query.lower()
        
        for sinf in self.questions:
            for fan in self.questions[sinf]:
                for mavzu in self.questions[sinf][fan]:
                    for q in self.questions[sinf][fan][mavzu]:
                        if query_lower in q['savol'].lower():
                            results.append({
                                'id': q['id'],
                                'sinf': sinf,
                                'fan': fan,
                                'mavzu': mavzu,
                                'savol': q['savol']
                            })
        
        if not results:
            return "❌ Hech narsa topilmadi"
        
        text = f"🔍 *QIDIRUVNING NATIJALARI ({len(results)} ta)*\n\n"
        for r in results[:10]:  # Birinchi 10 ta
            text += f"ID: {r['id']} | {r['sinf']}-sinf | {r['fan']} | {r['mavzu']}\n"
            text += f"❓ {r['savol']}\n\n"
        
        return text
    
    # ==================== BULK IMPORT ====================
    
    def bulk_import_csv(self, csv_file: str) -> Tuple[bool, str, Dict]:
        """CSV fayildan ko'plab savolllarni import qilish"""
        try:
            import csv
            
            imported_count = 0
            errors = []
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):  # Header shuning uchun 2'dan
                    try:
                        question_data = {
                            'sinf': row.get('sinf', '').strip(),
                            'fan': row.get('fan', '').lower().strip(),
                            'mavzu': row.get('mavzu', '').lower().strip(),
                            'savol': row.get('savol', '').strip(),
                            'variantlar': [
                                row.get('variant1', '').strip(),
                                row.get('variant2', '').strip(),
                                row.get('variant3', '').strip(),
                                row.get('variant4', '').strip(),
                            ],
                            'togri': row.get('togri', '').strip()
                        }
                        
                        # Validation
                        is_valid, error_msg = self._validate_question(question_data)
                        if not is_valid:
                            errors.append(f"Satr {row_num}: {error_msg}")
                            continue
                        
                        # Qo'shish
                        success, msg = self._add_question_to_data(question_data)
                        if success:
                            imported_count += 1
                        else:
                            errors.append(f"Satr {row_num}: {msg}")
                    
                    except Exception as e:
                        errors.append(f"Satr {row_num}: {str(e)}")
            
            result_msg = f"✅ {imported_count} ta savol import qilindi!"
            if errors:
                result_msg += f"\n\n⚠️ {len(errors)} ta xato:\n"
                result_msg += "\n".join(errors[:10])  # Birinchi 10 ta xato
                if len(errors) > 10:
                    result_msg += f"\n... va {len(errors)-10} ta ko'p xato"
            
            return True, result_msg, {'imported': imported_count, 'errors': len(errors)}
        
        except Exception as e:
            return False, f"❌ CSV import xatosi: {e}", {}
    
    def bulk_import_json_array(self, json_file: str) -> Tuple[bool, str, Dict]:
        """JSON (massiv) fayildan ko'plab savolllarni import qilish"""
        try:
            imported_count = 0
            errors = []
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Agar massiv bo'lsa
            if isinstance(data, list):
                questions_list = data
            else:
                return False, "❌ JSON fayil massiv bo'lishi kerak", {}
            
            for idx, question_data in enumerate(questions_list, start=1):
                try:
                    # Normalizatsiya
                    normalized = {
                        'sinf': str(question_data.get('sinf', '1')).strip(),
                        'fan': str(question_data.get('fan', '')).lower().strip(),
                        'mavzu': str(question_data.get('mavzu', '')).lower().strip(),
                        'savol': str(question_data.get('savol', '')).strip(),
                        'variantlar': question_data.get('variantlar', []),
                        'togri': str(question_data.get('togri', '')).strip()
                    }
                    
                    # Variant'larni ensure qilish (4 ta bo'lishi kerak)
                    if len(normalized['variantlar']) < 4:
                        errors.append(f"Savol {idx}: 4 ta variant kerak ({len(normalized['variantlar'])} ta bor)")
                        continue
                    
                    # Validation
                    is_valid, error_msg = self._validate_question(normalized)
                    if not is_valid:
                        errors.append(f"Savol {idx}: {error_msg}")
                        continue
                    
                    # Qo'shish
                    success, msg = self._add_question_to_data(normalized)
                    if success:
                        imported_count += 1
                    else:
                        errors.append(f"Savol {idx}: {msg}")
                
                except Exception as e:
                    errors.append(f"Savol {idx}: {str(e)}")
            
            result_msg = f"✅ {imported_count} ta savol import qilindi!"
            if errors:
                result_msg += f"\n\n⚠️ {len(errors)} ta xato:\n"
                result_msg += "\n".join(errors[:10])
                if len(errors) > 10:
                    result_msg += f"\n... va {len(errors)-10} ta ko'p xato"
            
            return True, result_msg, {'imported': imported_count, 'errors': len(errors)}
        
        except Exception as e:
            return False, f"❌ JSON import xatosi: {e}", {}
    
    def _validate_question(self, question_data: Dict) -> Tuple[bool, str]:
        """Savol ma'lumotlarini tekshirish"""
        
        # Sinf tekshirish
        if question_data['sinf'] not in ['1', '2', '3', '4']:
            return False, "Sinf 1-4 bo'lishi kerak"
        
        # Fan tekshirish
        if not question_data['fan']:
            return False, "Fan nomi kerak"
        
        # Mavzu tekshirish
        if not question_data['mavzu']:
            return False, "Mavzu nomi kerak"
        
        # Savol tekshirish
        if not question_data['savol']:
            return False, "Savol matni kerak"
        
        # Variantlar tekshirish
        if len(question_data['variantlar']) < 4 or any(not v for v in question_data['variantlar']):
            return False, "4 ta variant kerak (bo'sh bo'lmasa)"
        
        # To'g'ri javob tekshirish
        if question_data['togri'] not in question_data['variantlar']:
            return False, "To'g'ri javob variantlar orasida bo'lishi kerak"
        
        return True, "OK"
    
    # ==================== TEMPLATE GENERATSIYA ====================
    
    def generate_csv_template(self) -> str:
        """CSV template yaratish"""
        template = """sinf,fan,mavzu,savol,variant1,variant2,variant3,variant4,togri
1,matematika,qoshish,2 + 3 = ?,4,5,6,7,5
1,matematika,qoshish,1 + 6 = ?,5,6,7,8,7
1,matematika,ayirish,5 - 2 = ?,2,3,4,5,3
2,matematika,kopaytirish,3 × 4 = ?,7,10,12,14,12
2,matematika,bolish,20 ÷ 5 = ?,2,3,4,5,4
"""
        try:
            with open('template.csv', 'w', encoding='utf-8') as f:
                f.write(template)
            return "✅ template.csv yaratildi!"
        except Exception as e:
            return f"❌ Xato: {e}"
    
    def generate_json_template(self) -> str:
        """JSON template yaratish"""
        template = [
            {
                "sinf": "1",
                "fan": "matematika",
                "mavzu": "qoshish",
                "savol": "2 + 3 = ?",
                "variantlar": ["4", "5", "6", "7"],
                "togri": "5"
            },
            {
                "sinf": "1",
                "fan": "matematika",
                "mavzu": "qoshish",
                "savol": "1 + 6 = ?",
                "variantlar": ["5", "6", "7", "8"],
                "togri": "7"
            },
            {
                "sinf": "2",
                "fan": "matematika",
                "mavzu": "kopaytirish",
                "savol": "3 × 4 = ?",
                "variantlar": ["7", "10", "12", "14"],
                "togri": "12"
            }
        ]
        
        try:
            with open('template.json', 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
            return "✅ template.json yaratildi!"
        except Exception as e:
            return f"❌ Xato: {e}"

