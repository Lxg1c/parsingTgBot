import sqlite3
import logging
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subscribed_users.db")


def init_db():
    """Инициализация базы данных и создание таблицы, если её нет."""
    try:
        # Подключаемся к базе данных (если базы нет, она будет создана)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Создаём таблицу, если её нет
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
        """)

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Ошибка инициализации базы данных: {e}")


def subscribe_user(user_id: int):
    """Подписка пользователя (добавление его в базу данных)."""
    try:
        init_db()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Добавляем пользователя, если его нет в базе
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            logging.info(f"Пользователь {user_id} подписан.")
        else:
            logging.info(f"Пользователь {user_id} уже подписан.")
        conn.close()
    except Exception as e:
        logging.error(f"Ошибка подписки пользователя {user_id}: {e}")
        raise Exception("Не удалось подписать пользователя. Попробуйте позже.")


def unsubscribe_user(user_id: int):
    """Отписка пользователя (удаление его из базы данных)."""
    try:
        init_db()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Удаляем пользователя, если он есть в базе
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        logging.info(f"Пользователь {user_id} отписан.")

        conn.close()
    except Exception as e:
        logging.error(f"Ошибка отписки пользователя {user_id}: {e}")
        raise Exception("Не удалось отписать пользователя. Попробуйте позже.")


def get_subscribed_users():
    """Получение списка подписанных пользователей."""
    try:
        init_db()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Получаем всех подписанных пользователей
        cursor.execute("SELECT user_id FROM users")
        users = [row[0] for row in cursor.fetchall()]

        conn.close()
        return users
    except Exception as e:
        logging.error(f"Ошибка чтения базы данных: {e}")
        return []
