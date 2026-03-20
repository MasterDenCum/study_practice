import sqlite3
from .config import DATABASE_URL


def get_db():
    """Получение подключения к БД"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Таблица Users (1НФ, 2НФ, 3НФ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE,
            email VARCHAR(100) UNIQUE,
            password_hash VARCHAR(255),
            role VARCHAR(20)
        )
    ''')
    
    # Таблица Games (1НФ, 2НФ, 3НФ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100),
            description TEXT,
            price DECIMAL(10,2),
            developer_id INTEGER,
            FOREIGN KEY(developer_id) REFERENCES Users(id)
        )
    ''')
    
    # Таблица Library (1НФ, 2НФ, 3НФ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            game_id INTEGER,
            purchase_date DATETIME,
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(game_id) REFERENCES Games(id)
        )
    ''')

    # Добавляем тестовые данные, если БД пустая
    cursor.execute("SELECT COUNT(*) FROM Games")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ('Valve', 'dev@valve.com', 'hash', 'Разработчик')
        )
        dev_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO Games (title, description, price, developer_id) VALUES (?, ?, ?, ?)",
            ('Half-Life 3', 'Легендарное продолжение', 2000.00, dev_id)
        )
        cursor.execute(
            "INSERT INTO Games (title, description, price, developer_id) VALUES (?, ?, ?, ?)",
            ('Cyber Portal', 'Головоломка в киберпанке', 900.50, dev_id)
        )

    conn.commit()
    conn.close()
