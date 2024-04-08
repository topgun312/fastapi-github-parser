import datetime
import json
import re
from typing import List
import aiohttp
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from src.config import SITE_URL, logger
from src.database import create_conn


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


owner_list = []
commits_list = []
author_list = []


async def get_github_top_repo_info() -> None:
    """
    Функция для получения информации о топ 100 репозиторием о количеству звезд (stars) на github.com,
    записи в файл .csv
    """
    logger.info("Начинаю загрузку информации о топ 100 репозиторием о количеству звезд")
    driver.get(SITE_URL)
    mydata = pd.DataFrame(
        columns=[
            "position_cur",
            "repo",
            "stars",
            "forks",
            "language",
            "open_issues",
            "description",
            "last_commit",
        ]
    )
    table = driver.find_element(By.TAG_NAME, "table")
    for j in table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr"):
        row_data = j.find_elements(By.TAG_NAME, "td")
        row = [i.text for i in row_data]
        mydata.loc[len(mydata)] = row
        dop_url = [a.get_attribute("href") for a in j.find_elements(By.TAG_NAME, "a")]
        owner = get_owner(dop_url)
    mydata.insert(loc=1, column="owner", value=owner)
    mydata[["position_cur", "stars", "forks", "open_issues"]] = mydata[
        ["position_cur", "stars", "forks", "open_issues"]
    ].astype(int)
    mydata.to_csv(
        f"/home/topgun/PycharmProjects/fastapi_github_parse_project/src/csv_files/top_repos_data_{datetime.datetime.utcnow()}.csv",
        index=False,
    )
    await load_data_from_csv_to_bd(mydata)
    logger.info("Данные загружены в БД и в файл .csv")


def get_owner(urls: list) -> List[str]:
    """
    Функция для получения списка авторов репозиториев.
    :param urls: список url-адресов репозиториев
    """
    try:
        for url in urls:
            response = requests.get(url)
            soup = bs(response.content, "lxml")
            owner_name = soup.find("span", class_="author flex-self-stretch")
            cor_owner_name = owner_name.text if owner_name else "Нет данных."
            cor_owner = re.sub("\n", "", cor_owner_name.strip())
            owner_list.append(cor_owner)
            return owner_list
    except Exception as ex:
        logger.exception(f"Ошибка: {ex}", exc_info=True)


async def load_data_from_csv_to_bd(df) -> None:
    """
    Фукция для загрузки данных в БД.
    :param df: Датафрейм данных
    """
    conn = await create_conn()
    await conn.copy_records_to_table(
        "toprepoinfo",
        records=df.itertuples(index=False),
        columns=df.columns.to_list(),
        timeout=10,
    )


async def parse_repos_active(
    owner: str, repo: str, since: datetime.date, until: datetime.date
) -> None:
    """
    Функция для получения информации об активности репозитория по коммитам за выбранный промежуток времени по дням,
    записи в файл .csv.
    :param owner: автор репозитория
    :param repo: имя репозитория
    :param since: дата от
    :param until: дата до
    """
    logger.info("Начинаю загрузку информации об активности репозитория по коммитам")
    mydata = pd.DataFrame(columns=["commits", "authors"])
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.github.com/repos/{owner}/{repo}/activity"
        ) as response:
            data = await response.text()
            result = json.loads(data)
            for res in result:
                date_str = res["timestamp"][:10]
                cor_date = datetime.date.fromisoformat(date_str)
                if cor_date >= since and cor_date <= until:
                    commits_list.append(res)
        for actor in commits_list:
            author_list.append(actor["actor"]["login"])
        res_dict = {"commits": len(commits_list), "authors": author_list}
        mydata.loc[len(mydata)] = res_dict
        mydata.to_csv(
            f"/home/topgun/PycharmProjects/fastapi_github_parse_project/src/csv_files/repos_active_{datetime.datetime.utcnow()}.csv",
            index=False,
        )
        await load_repos_active_from_csv_to_bd(mydata)
        logger.info("Данные загружены в БД и в файл .csv")


async def load_repos_active_from_csv_to_bd(df) -> None:
    """
    Фукция для загрузки данных в БД.
    :param df: Датафрейм данных
    """
    conn = await create_conn()
    await conn.copy_records_to_table(
        "ghrepoactive",
        records=df.itertuples(index=False),
        columns=df.columns.to_list(),
        timeout=10,
    )
