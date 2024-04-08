from typing import Any
import asyncpg
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def create_conn() -> Any | None:
    """
    Функция для создания соединения с БД postgresql.
    """
    try:
        connection = await asyncpg.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=DB_PORT
        )
        return connection
    except Exception as ex:
        print(f"Ошибка: {ex}")
