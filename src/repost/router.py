import datetime
from fastapi import APIRouter, HTTPException
from src.config import logger
from src.database import create_conn
from src.repost.parse_info import get_github_top_repo_info, parse_repos_active


router = APIRouter(prefix="/api/repos", tags=["Github Info"])


@router.get("/top100")
async def get_top_repo_info():
    """
    Функция для отображения топ 100 публичных репозиториев.
    """
    try:
        await get_github_top_repo_info()
        conn = await create_conn()
        data = await conn.fetch(
            """
                      SELECT * FROM toprepoinfo"""
        )
        await conn.close()
        return data
    except Exception as ex:
        logger.exception(ex)
    raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{owner}/{repo}/activity")
async def get_activity_repo(
    owner: str, repo: str, since: datetime.date, until: datetime.date
):
    """
    Функция для отображения активности репозитория по коммитам за выбранный промежуток времени по дням.
    :param owner: автор репозитория
    :param repo: имя репозитория
    :param since: дата от
    :param until: дата до
    """
    try:
        if (
            isinstance(owner, str)
            and isinstance(repo, str)
            and isinstance(since, datetime.date)
            and isinstance(until, datetime.date)
        ):
            await parse_repos_active(owner, repo, since, until)
            conn = await create_conn()
            data = await conn.fetch(
                """
                          SELECT * FROM ghrepoactive"""
            )
            await conn.close()
            return data
        else:
            return HTTPException(
                status_code=422, detail="Введены не корректные данные!"
            )
    except Exception as ex:
        logger.exception(ex)
    raise HTTPException(status_code=500, detail="Internal server error")
