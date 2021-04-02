import os
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_soup(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def fetch_title_and_author(soup):
    tag = soup.find('h1').text

    if len(tag.split('::')) == 2:
        title = tag.split('::')[0].strip()
        author = tag.split('::')[1].strip()
    else:
        title = tag.split('::')[0].strip()
        author = 'Нет автора'
    return title, author


def fetch_book_image_url(url, soup):
    selector_image_url = '.bookimage img'
    image_url_tag = soup.select_one(selector_image_url).get('src')
    image_url = urljoin(url, image_url_tag)
    return image_url


def download_book_cover(url, folder='img'):
    Path(folder).mkdir(parents=True, exist_ok=True)

    cover_path = urlsplit(url).path
    _, imagename = os.path.split(cover_path)

    path = os.path.join(folder, sanitize_filename(unquote(imagename)))
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_comment(soup):
    selector_comment = '.texts .black'
    new_comment_texts = soup.select(selector_comment)

    comments_text = []

    for comment in new_comment_texts:
        comments_text.append(comment.get_text())
    return comments_text


def get_genres(soup):
    selector_genres = '.d_book'
    new_genres_tag = soup.select(selector_genres)
    genres = []
    for tag in new_genres_tag:
        if tag.get_text().startswith('Жанр книги:'):
            genr = tag.get_text().replace('Жанр книги:', '')
            genres.append(genr.lstrip())
    return genres


def save_book(filename, response, folder='books'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'w') as file:
        file.write(response.text)
    return path


def parse_book_page(book_url, index_url):
    book_page = {}
    soup = get_soup(book_url)
    title, author = fetch_title_and_author(soup)
    image_url = fetch_book_image_url(index_url, soup)
    genres = get_genres(soup)
    comments_text = download_comment(soup)
    book_page.update({'title': title,
                      'author': author,
                      'image_link': image_url,
                      'genres': genres,
                      'commets': comments_text})
    return book_page