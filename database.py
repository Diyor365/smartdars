import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple

class Database:
    """SQLite database handler"""
    
    def __init__(self, db_name='smartdars.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Database jadvallarini yaratish"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Foydalanuvchilar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Test sessiya jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                sinf TEXT NOT NULL,
                fan TEXT NOT NULL,
                mavzu TEXT NOT NULL,
                correct_answers INTEGER DEFAULT 0,
                total_answers INTEGER DEFAULT 0,
                percentage REAL DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                finished_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')
        
        # Javoblar jadvali (har bir savol)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                selected_answer TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES test_sessions(id)
            )
        ''')
        
        # Statistika (tezkor ma'lumot olish uchun)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                total_tests INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                wrong_answers INTEGER DEFAULT 0,
                average_percentage REAL DEFAULT 0,
                last_test_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, telegram_id: int, first_name: str, last_name: str = None) -> bool:
        """Yangi foydalanuvchi qo'shish"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO users (telegram_id, first_name, last_name)
                VALUES (?, ?, ?)
            ''', (telegram_id, first_name, last_name))
            
            # Statistika jadvali uchun
            cursor.execute('''
                INSERT OR IGNORE INTO statistics (user_id)
                VALUES (?)
            ''', (telegram_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def create_test_session(self, user_id: int, sinf: str, fan: str, mavzu: str) -> int:
        """Test sessiyasini yaratish"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO test_sessions (user_id, sinf, fan, mavzu)
            VALUES (?, ?, ?, ?)
        ''', (user_id, sinf, fan, mavzu))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
    
    def save_answer(self, session_id: int, question_id: int, 
                   selected_answer: str, is_correct: bool) -> bool:
        """Javobni saqlash"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO answers (session_id, question_id, selected_answer, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (session_id, question_id, selected_answer, is_correct))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving answer: {e}")
            return False
    
    def finish_test_session(self, session_id: int, correct_count: int, total_count: int) -> bool:
        """Test sessiyasini tugatish"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            percentage = (correct_count / total_count) * 100 if total_count > 0 else 0
            
            cursor.execute('''
                UPDATE test_sessions
                SET correct_answers = ?, total_answers = ?, percentage = ?, finished_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (correct_count, total_count, percentage, session_id))
            
            # User statistikasini yangilash
            cursor.execute('''
                SELECT user_id FROM test_sessions WHERE id = ?
            ''', (session_id,))
            
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                
                cursor.execute('''
                    UPDATE statistics
                    SET 
                        total_tests = total_tests + 1,
                        correct_answers = correct_answers + ?,
                        wrong_answers = wrong_answers + ?,
                        last_test_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (correct_count, total_count - correct_count, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error finishing session: {e}")
            return False
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """Foydalanuvchi statistikasini olish"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_tests, correct_answers, wrong_answers, average_percentage, last_test_at
            FROM statistics
            WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_tests': result[0],
                'correct_answers': result[1],
                'wrong_answers': result[2],
                'average_percentage': result[3],
                'last_test_at': result[4],
                'total_answers': result[1] + result[2]
            }
        
        return {
            'total_tests': 0,
            'correct_answers': 0,
            'wrong_answers': 0,
            'average_percentage': 0,
            'last_test_at': None,
            'total_answers': 0
        }
    
    def get_test_sessions(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Foydalanuvchining test sessiyalarini olish"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, sinf, fan, mavzu, correct_answers, total_answers, percentage, started_at
            FROM test_sessions
            WHERE user_id = ?
            ORDER BY started_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in results:
            sessions.append({
                'id': row[0],
                'sinf': row[1],
                'fan': row[2],
                'mavzu': row[3],
                'correct_answers': row[4],
                'total_answers': row[5],
                'percentage': row[6],
                'started_at': row[7]
            })
        
        return sessions
    
    def get_statistics_by_subject(self, user_id: int, fan: str) -> Dict:
        """Fan bo'yicha statistika"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                AVG(percentage) as avg_percentage,
                SUM(CASE WHEN percentage >= 80 THEN 1 ELSE 0 END) as excellent,
                SUM(CASE WHEN percentage >= 60 AND percentage < 80 THEN 1 ELSE 0 END) as good,
                SUM(CASE WHEN percentage < 60 THEN 1 ELSE 0 END) as poor
            FROM test_sessions
            WHERE user_id = ? AND fan = ?
        ''', (user_id, fan))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return {
                'total': result[0],
                'average_percentage': result[1] or 0,
                'excellent': result[2] or 0,
                'good': result[3] or 0,
                'poor': result[4] or 0
            }
        
        return {
            'total': 0,
            'average_percentage': 0,
            'excellent': 0,
            'good': 0,
            'poor': 0
        }
    
    def get_weak_topics(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Kuchli bo'lmagan mavzularni olish"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sinf, fan, mavzu, AVG(percentage) as avg_percentage, COUNT(*) as attempts
            FROM test_sessions
            WHERE user_id = ? AND percentage < 70
            GROUP BY sinf, fan, mavzu
            ORDER BY avg_percentage ASC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        topics = []
        for row in results:
            topics.append({
                'sinf': row[0],
                'fan': row[1],
                'mavzu': row[2],
                'average_percentage': row[3],
                'attempts': row[4]
            })
        
        return topics
