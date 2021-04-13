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
    selector_title = 'h1'
    title, author = soup.select_one(selector_title).text.split('::')
    return title, author.lstrip()


def fetch_book_image_url(url, soup):
    selector_image_url = '.bookimage img'
    image_url_tag = soup.select_one(selector_image_url).get('src')
    image_url = urljoin(url, image_url_tag)
    return image_url


def get_comments(soup):
    selector_comment = '.texts .black'
    comment_tags = soup.select(selector_comment)

    comments = []
    for comment_tag in comment_tags:
        comments.append(comment_tag.get_text())
    return comments


def get_genres(soup):
    selector_genres = 'span.d_book'
    genres_tags = soup.select_one(selector_genres)
    return genres_tags.text.replace('Жанр книги:', '').lstrip()


def save_book(filename, response, path_folder, skip_txt, default_folder='books'):
    if not skip_txt:
        Path(f'{path_folder}/{default_folder}').mkdir(parents=True, exist_ok=True)
        path = os.path.join(f'{path_folder}/{default_folder}', sanitize_filename(filename))

        with open(path, 'w') as file:
            file.write(response.text)
        return path
    else:
        return 'Пользователь предпочел не скачивать тексты'


def download_book_cover(url, book_id, path_folder, skip_img, default_folder='img'):
    if not skip_img:
        Path(f'{path_folder}/{default_folder}').mkdir(parents=True, exist_ok=True)

        cover_path = urlsplit(url).path
        _, imagename = os.path.split(cover_path)
        if imagename != 'nopic.gif':
            path = os.path.join(f'{path_folder}/{default_folder}', sanitize_filename(unquote(f'{book_id}-{imagename}')))
        else:
            path = os.path.join(f'{path_folder}/{default_folder}', sanitize_filename(unquote(imagename)))
        response = requests.get(url, verify=False)
        response.raise_for_status()
        with open(path, 'wb') as file:
            file.write(response.content)
        return path
    else:
        return 'Пользователь предпочел не скачивать картинки'


def parse_book_page(book_url, index_url):
    soup = get_soup(book_url)
    title, author = fetch_title_and_author(soup)
    image_url = fetch_book_image_url(index_url, soup)
    genres = get_genres(soup)
    comments_text = get_comments(soup)
    book_page = {'title': title.rstrip(),
                 'author': author,
                 'image_link': image_url,
                 'genres': genres,
                 'commets': comments_text}
    return book_page
