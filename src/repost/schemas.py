import datetime
from pydantic import BaseModel


class GithubTopInfoRead(BaseModel):
    """
    Схема для валидации исходных данных toprepoinfo.
    """

    id: int
    position_cur: int
    owner: str
    repo: str
    stars: int
    forks: int
    language: str
    open_issues: int
    description: str
    last_commit: datetime.date

    class Config:
        from_attributes = True


class GithubRepoActivityRead(BaseModel):
    """
    Схема для валидации исходных данных ghrepoactive.
    """

    id: int
    date: datetime.date
    commits: int
    authors: list[str]

    class Config:
        from_attributes = True
