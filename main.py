from src.repost.models import create_db, delete_db
from fastapi import FastAPI
from src.repost.router import router
from src.config import logger
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    logger.info('БД создана!')
    yield
    await delete_db()
    logger.info('БД удалена!')


app = FastAPI(title='GithubInfo App', lifespan=lifespan, debug=True)
app.include_router(router)

