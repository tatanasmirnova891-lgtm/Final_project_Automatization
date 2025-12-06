import os
import psycopg2
import csv
from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import execute_values

# Проверка воскресенья
if datetime.now().weekday() == 6:
    print("Сегодня воскресенье, скрипт пропущен")
    exit()

def get_connection(): 
    load_dotenv('config.env')
    return psycopg2.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        dbname=os.getenv('DBNAME'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    conn.autocommit = True
    
    # Справочник категорий
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        )
    ''')
    
    # Чеки
    cur.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id SERIAL PRIMARY KEY,
            doc_id VARCHAR(50) UNIQUE NOT NULL,
            shop_num INTEGER NOT NULL,
            cash_num INTEGER NOT NULL,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Позиции чеков
    cur.execute('''
        CREATE TABLE IF NOT EXISTS receipt_items (
            id SERIAL PRIMARY KEY,
            receipt_id INTEGER REFERENCES receipts(id) ON DELETE CASCADE,
            category_id INTEGER REFERENCES categories(id),
            item VARCHAR(255) NOT NULL,
            amount INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            discount DECIMAL(10,2) DEFAULT 0
        )
    ''')
    
    conn.close()
    print("Таблицы созданы!")

def load_files_to_db():
    create_tables()
    
    DATA_FOLDER = os.getenv('DATA_FOLDER', './data')
    
    conn = get_connection()
    cur = conn.cursor()
    
    processed_files = 0
    
    for filename in os.listdir(DATA_FOLDER):
        if not filename.endswith('.csv'):
            continue
            
        # Парсим магазин и кассу из имени файла
        try:
            shop_num, cash_num = map(int, filename[:-4].split('_'))
        except:
            print(f"Пропуск: {filename}")
            continue
        
        filepath = os.path.join(DATA_FOLDER, filename)
        print(f"Обрабатываем: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                doc_id = row['doc_id']
                category = row['category']
                item = row['item']
                amount = int(row['amount'])
                price = float(row['price'])
                discount = float(row['discount'])
                
                # 1. Получаем/создаем категорию
                cur.execute("SELECT id FROM categories WHERE name = %s", (category,))
                cat_result = cur.fetchone()
                if not cat_result:
                    cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id", (category,))
                    category_id = cur.fetchone()[0]
                else:
                    category_id = cat_result[0]
                
                # 2. Получаем/создаем чек
                cur.execute("SELECT id FROM receipts WHERE doc_id = %s", (doc_id,))
                receipt_result = cur.fetchone()
                if not receipt_result:
                    cur.execute("""
                        INSERT INTO receipts (doc_id, shop_num, cash_num) 
                        VALUES (%s, %s, %s) RETURNING id
                    """, (doc_id, shop_num, cash_num))
                    receipt_id = cur.fetchone()[0]
                else:
                    receipt_id = receipt_result[0]
                
                # 3. Добавляем позицию
                cur.execute("""
                    INSERT INTO receipt_items (receipt_id, category_id, item, amount, price, discount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (receipt_id, category_id, item, amount, price, discount))
        
        processed_files += 1
    
    conn.commit()
    conn.close()
    print(f"Готово! Обработано файлов: {processed_files}")

if __name__ == '__main__':
    load_files_to_db()
