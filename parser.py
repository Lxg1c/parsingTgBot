import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time


def fetch_page(url, headers):
    """Загружает страницу и возвращает её содержимое."""
    response = requests.get(
        url,
        headers=headers,
        verify=False,
    )
    response.encoding = "utf-8"  # Указываем правильную кодировку
    return response.text


def parse_news_section(soup):
    """Извлекает секцию новостей из HTML."""
    news_section = soup.find("section", class_="section-news")
    if not news_section:
        print("Не удалось найти секцию новостей.")
        return None
    return news_section.find("div", class_="section-body")


def extract_article_data(article, base_url):
    """Извлекает данные из статьи."""
    article_title = article.find("h4", class_="article-card-title")
    article_link = article.find("a")
    article_time = article.find("time")

    # Проверка обязательных полей
    if not all([article_title, article_link, article_time]):
        print("Не удалось извлечь данные из статьи.")
        return None

    # Извлечение изображения
    article_img_div = article.find("div", class_="article-img")
    if not article_img_div:
        print("Не найдено изображение статьи.")
        return None

    article_img = article_img_div.find("img")
    if not article_img:
        print("Не найден тег <img> в статье.")
        return None

    article_img_url = f"{base_url}{article_img.get('src')}"

    # Обработка данных
    article_title = article_title.text.strip()
    article_link = f"{base_url}{article_link.get('href')}"
    article_id = article_link.split("/")[-1][:-4]  # Убираем расширение .php

    date_from_iso = datetime.fromisoformat(article_time.get("datetime"))
    article_datetime_timestamp = time.mktime(date_from_iso.timetuple())

    return {
        "id": article_id,
        "time": article_datetime_timestamp,
        "img": article_img_url,
        "title": article_title,
        "link": article_link,
    }


def remove_old_news(news_dict, days=5):
    """Удаляет новости старше указанного количества дней."""
    current_time = time.time()
    threshold = current_time - (days * 24 * 60 * 60)  # Время в секундах

    # Фильтруем новости, оставляя только те, которые новее порога
    return {k: v for k, v in news_dict.items() if v["time"] >= threshold}


def get_first_news():
    """Получает и сохраняет первые новости."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36"
    }
    url = "https://www.securitylab.ru"

    page_content = fetch_page(url, headers)
    soup = BeautifulSoup(page_content, "lxml")

    news_section = parse_news_section(soup)
    if not news_section:
        return

    article_cards = news_section.find_all("div", class_="article-card")
    news_dict = {}

    for article in article_cards:
        article_data = extract_article_data(article, url)
        if article_data:
            news_dict[article_data["id"]] = article_data

    # Удаляем старые новости перед сохранением
    news_dict = remove_old_news(news_dict)

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_updated_news():
    """Проверяет обновления новостей и добавляет новые."""
    try:
        with open("news_dict.json", "r", encoding="utf-8") as file:
            news_dict = json.load(file)
    except FileNotFoundError:
        print("Файл news_dict.json не найден. Сначала выполните get_first_news().")
        return {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36"
    }
    url = "https://www.securitylab.ru"

    page_content = fetch_page(url, headers)
    soup = BeautifulSoup(page_content, "lxml")

    news_section = parse_news_section(soup)
    if not news_section:
        return {}

    article_cards = news_section.find_all("div", class_="article-card")
    fresh_news = {}

    for article in article_cards:
        article_data = extract_article_data(article, url)
        if not article_data:
            continue

        if article_data["id"] not in news_dict:
            news_dict[article_data["id"]] = article_data
            fresh_news[article_data["id"]] = article_data
            # print(f"Добавлена новая статья: {article_data['title']}")

    # Удаляем старые новости перед сохранением
    news_dict = remove_old_news(news_dict)

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return list(fresh_news.values())
