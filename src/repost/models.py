from src.database import create_conn


async def create_db() -> None:
    """
    Функция для создания таблиц БД.
    """
    try:
        conn = await create_conn()
        await conn.execute(
            """ CREATE TABLE IF NOT EXISTS toprepoinfo (id SERIAL PRIMARY KEY NOT NULL, position_cur INTEGER NOT NULL, 
                                owner VARCHAR NOT NULL, repo VARCHAR NOT NULL, stars INTEGER NOT NULL, forks INTEGER NOT NULL, 
                                language VARCHAR NOT NULL, open_issues INTEGER NOT NULL, description VARCHAR NOT NULL, last_commit VARCHAR NOT NULL) """
        )
        await conn.execute(
            """ CREATE TABLE  IF NOT EXISTS ghrepoactive (id SERIAL PRIMARY KEY NOT NULL,
                            date TIMESTAMPTZ NOT NULL DEFAULT NOW(), commits INTEGER NOT NULL, authors VARCHAR [] NOT NULL) """
        )
        await conn.close()
    except Exception as ex:
        print(f"Ошибка: {ex}")


async def delete_db() -> None:
    """
    Функция для удаления таблиц БД.
    """
    try:
        cursor = await create_conn()
        await cursor.execute("DROP TABLE toprepoinfo")
        await cursor.execute("DROP TABLE ghrepoactive")
        await cursor.close()
    except Exception as ex:
        print(f"Ошибка: {ex}")
