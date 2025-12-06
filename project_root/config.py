import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.getenv('PROJECT_ROOT', r"C:\Users\User\Downloads\SIMULATIVE\Final_project_Automatization\project_root") # ЗАМЕНИТЬ ПУТЬ ДО ПАПКИ
DATA_FOLDER = os.getenv('DATA_FOLDER', os.path.join(PROJECT_ROOT, 'data'))
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.env')

DB_CONFIG = {
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'dbname': os.getenv('DBNAME'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD')
}