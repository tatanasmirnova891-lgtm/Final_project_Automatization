import csv
import os
import random
import string
from datetime import datetime
from dotenv import load_dotenv
from config import DATA_FOLDER

from datetime import datetime
if datetime.now().weekday() == 6:  # 6 = воскресенье
    print("Сегодня воскресенье, скрипт пропущен")
    exit()

BASE_DIR = os.getenv('PROJECT_ROOT', r"C:\Users\User\Downloads\SIMULATIVE\Final_project_Automatization\project_root") # ЗАМЕНИТЬ ПУТЬ ДО ПАПКИ
DATA_FOLDER = os.path.join(BASE_DIR, 'data')

CATEGORIES = [
    'бытовая химия', 'текстиль', 'посудa', 'продукты', 'электроника',
    'одежда', 'обувь', 'косметика', 'товары для детей', 'здоровье и спорт',
    'мебель', 'инструменты', 'автотовары', 'канцтовары', 'сезонные товары'
]

ITEMS = {
    'бытовая химия': ['моющее средство', 'средство для мытья посуды', 'чистящее средство', 'освежитель воздуха', 'универсальный пятновыводитель'],
    'текстиль': ['полотенце', 'скатерть', 'покрывало', 'шторы', 'простыни'],
    'посудa': ['тарелка', 'вилка', 'ложка', 'кастрюля', 'столовый набор'],
    'продукты': ['хлеб', 'молоко', 'сыр', 'колбаса', 'овощи', 'фрукты'],
    'электроника': ['лампочка', 'зарядное устройство', 'наушники', 'телевизор', 'смартфон'],
    'одежда': ['футболка', 'джинсы', 'куртка', 'платье', 'толстовка'],
    'обувь': ['кроссовки', 'ботинки', 'тапочки', 'сандалии', 'ботильоны'],
    'косметика': ['шампунь', 'крем для лица', 'помада', 'туалетная вода', 'тушь для ресниц'],
    'товары для детей': ['подгузники', 'игрушки', 'книжки', 'детское питание', 'памперсы'],
    'здоровье и спорт': ['витамины', 'йога-коврик', 'гантели', 'фитнес-браслет', 'спортивная бутылка'],
    'мебель': ['стул', 'стол', 'шкаф', 'кровать', 'кресло'],
    'инструменты': ['отвертка', 'молоток', 'дрель', 'пила', 'набор гаечных ключей'],
    'автотовары': ['масло моторное', 'насос для шин', 'автомобильный пылесос', 'аксессуары для авто', 'запчасти'],
    'канцтовары': ['ручка', 'тетрадь', 'клей', 'маркер', 'альбом для рисования'],
    'сезонные товары': ['зонтик', 'морозилка', 'кондиционер', 'обогреватель', 'рождественские украшения']
}

def random_doc_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_csv(shop_num, cash_num, num_receipts=50):
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    filename = f"{shop_num}_{cash_num}.csv"
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['doc_id', 'item', 'category', 'amount', 'price', 'discount'])
        for _ in range(num_receipts):
            doc_id = random_doc_id()
            category = random.choice(CATEGORIES)
            item = random.choice(ITEMS[category])
            amount = random.randint(1, 5)
            price = round(random.uniform(10, 1000), 2)
            discount = round(random.uniform(0, price * amount * 0.3), 2)  # скидка до 30%
            writer.writerow([doc_id, item, category, amount, price, discount])


if __name__ == "__main__":
    N = 12  # количество магазинов
    CASHES_PER_SHOP = 7  # количество касс в магазине
    for shop in range(1, N+1):
        for cash in range(1, CASHES_PER_SHOP+1):
            generate_csv(shop, cash)
    print(f"Генерация файлов завершена")
