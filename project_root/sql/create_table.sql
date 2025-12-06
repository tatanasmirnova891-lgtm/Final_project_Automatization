-- Справочник категорий
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
)
    
-- Чеки
CREATE TABLE IF NOT EXISTS receipts (
    id SERIAL PRIMARY KEY,
    doc_id VARCHAR(50) UNIQUE NOT NULL,
    shop_num INTEGER NOT NULL,
    cash_num INTEGER NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    
-- Позиции чеков
CREATE TABLE IF NOT EXISTS receipt_items (
    id SERIAL PRIMARY KEY,
    receipt_id INTEGER REFERENCES receipts(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id),
    item VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    discount DECIMAL(10,2) DEFAULT 0
)