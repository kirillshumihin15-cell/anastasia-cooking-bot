import aiosqlite
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from config import config

DB_PATH = config.DB_PATH


async def init_db():
    """Инициализация таблиц базы данных SQLite"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_states (
                user_id INTEGER PRIMARY KEY,
                state TEXT,
                data TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_name TEXT,
                payload TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_or_update_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    source: str = "direct"
):
    """Добавить или обновить пользователя при активности"""
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, source, created_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = COALESCE(excluded.username, users.username),
                first_name = COALESCE(excluded.first_name, users.first_name),
                last_name = COALESCE(excluded.last_name, users.last_name),
                last_active = excluded.last_active
        """, (user_id, username, first_name, last_name, source, now, now))
        await db.commit()


async def log_event(user_id: int, event_name: str, payload: Optional[Dict[str, Any]] = None):
    """Зафиксировать аналитическое событие воронки"""
    payload_str = json.dumps(payload, ensure_ascii=False) if payload else None
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO analytics_events (user_id, event_name, payload, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, event_name, payload_str, now))
        await db.commit()


async def set_user_state(user_id: int, state: str, data: Optional[Dict[str, Any]] = None):
    """Сохранить состояние пользователя"""
    data_str = json.dumps(data, ensure_ascii=False) if data else None
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_states (user_id, state, data, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                state = excluded.state,
                data = excluded.data,
                updated_at = excluded.updated_at
        """, (user_id, state, data_str, now))
        await db.commit()


async def get_user_state(user_id: int) -> Optional[Dict[str, Any]]:
    """Получить последнее состояние пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM user_states WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "state": row["state"],
                    "data": json.loads(row["data"]) if row["data"] else {},
                    "updated_at": row["updated_at"]
                }
            return None


async def get_stats() -> Dict[str, Any]:
    """Получить общую статистику по пользователям и воронке"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            total_users = (await cursor.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM users WHERE source = 'chat_join_request'") as cursor:
            join_requests = (await cursor.fetchone())[0]

        async with db.execute("""
            SELECT event_name, COUNT(*) as cnt 
            FROM analytics_events 
            GROUP BY event_name 
            ORDER BY cnt DESC
        """) as cursor:
            events = await cursor.fetchall()

    return {
        "total_users": total_users,
        "join_requests": join_requests,
        "events": {event[0]: event[1] for event in events}
    }
