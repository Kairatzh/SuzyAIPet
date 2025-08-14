import psycopg2 as ps
import datetime as dt
from src.utils.configs.settings import load_configs

configs = load_configs()


DB_NAME = configs["db"]["db_name"]
DB_USER = configs["db"]["db_user"]
DB_PASSWORD = configs["db"]["db_password"]
DB_HOST = configs["db"]["db_host"]
DB_PORT = configs["db"]["db_port"]


"""Создает базу данных если она не существует"""
def create_database(db_name: str):
    conn = ps.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"База данных {db_name} создана.")
    else:
        print(f"База данных {db_name} уже существует.")
    
    cur.close()
    conn.close()

"""Настройка базы данных для долгосрочной памяти (дневник)"""
def setup_lt_memory():
    conn = ps.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'diary_entries'
    );
    """)
    table_exists = cur.fetchone()[0]
    
    if not table_exists:
        cur.execute("""
        CREATE TABLE diary_entries (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            entry TEXT NOT NULL,
            emotion TEXT
        );
        """)
        print(f"Таблица diary_entries создана с новой структурой.")
    else:
        cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.columns 
            WHERE table_name = 'diary_entries' 
            AND column_name = 'emotion'
        );
        """)
        emotion_column_exists = cur.fetchone()[0]
        
        if not emotion_column_exists:
            cur.execute("ALTER TABLE diary_entries ADD COLUMN emotion TEXT;")
            print(f"Поле emotion добавлено к существующей таблице diary_entries.")
        else:
            print(f"Таблица diary_entries уже содержит поле emotion.")
    
    conn.commit()
    
    cur.execute("DELETE FROM diary_entries;")
    conn.commit()
    
    test_entries = [
        ("user_1", "2025-01-02 10:00:00", "Сегодня я чувствую себя отлично!", "радость"),
        ("user_1", "2025-01-02 15:30:00", "Пошел на прогулку в парк", "спокойствие"),
        ("user_2", "2025-01-02 12:00:00", "Работаю над новым проектом", "воодушевление"),
        ("user_2", "2025-01-02 18:00:00", "Долгий рабочий день, устал", "усталость")
    ]
    
    for user_id, datetime_str, entry, emotion in test_entries:
        cur.execute(
            "INSERT INTO diary_entries (user_id, datetime, entry, emotion) VALUES (%s, %s, %s, %s)",
            (user_id, datetime_str, entry, emotion)
        )
    
    conn.commit()
    
    print(f"Таблица diary_entries в {DB_NAME} обновлена и заполнена тестовыми данными.")
    
    cur.close()
    conn.close()


"""Показать тестовые данные из базы данных"""
def show_test_data():
    print("\n" + "="*50)
    print("ТЕСТОВЫЕ ДАННЫЕ")
    print("="*50)
    
    print(f"\n📖 Дневник ({DB_NAME}):")
    conn = ps.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT user_id, datetime, entry, emotion FROM diary_entries ORDER BY datetime;")
    rows = cur.fetchall()
    for row in rows:
        emotion_text = f" | 😊 {row[3]}" if row[3] else ""
        print(f"  👤 {row[0]} | {row[1]} | {row[2]}{emotion_text}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("Создание базы данных для AI-питомца Suzy...")
    
    create_database(DB_NAME)
    
    setup_lt_memory()
    
    show_test_data()
    
    print("\n✅ База данных успешно создана и настроена!")
