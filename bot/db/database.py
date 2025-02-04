import json
from pathlib import Path
import logging

DB_FILE = Path("subscribed_users.json")


def init_db():
    try:
        if not DB_FILE.exists():
            DB_FILE.write_text("[]", encoding="utf-8")
    except Exception as e:
        logging.error(f"Ошибка инициализации БД: {e}")


def subscribe_user(user_id: int):
    try:
        init_db()
        users = get_subscribed_users()
        if user_id not in users:
            users.append(user_id)
            DB_FILE.write_text(json.dumps(users), encoding="utf-8")
    except Exception as e:
        logging.error(f"Ошибка подписки пользователя {user_id}: {e}")


def unsubscribe_user(user_id: int):
    try:
        init_db()
        users = get_subscribed_users()
        if user_id in users:
            users.remove(user_id)
            DB_FILE.write_text(json.dumps(users), encoding="utf-8")
    except Exception as e:
        logging.error(f"Ошибка отписки пользователя {user_id}: {e}")


def get_subscribed_users():
    try:
        init_db()
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logging.error(f"Ошибка чтения БД: {e}")
        return []
