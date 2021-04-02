import argparse
import logging
import os
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import trange
import parse_tululu_category
import json
from pprint import pprint
import config
import get_books


def fetch_url_response(url, id):
    params = {
        'id': id
    }
    response = requests.get(url, params=params, verify=False)
    response.raise_for_status()
    return response


def get_soup(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def save_book(filename, response, folder='books'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'w') as file:
        file.write(response.text)
    return path


def parse_book_page(book_url, index_url):
    book_page = {}
    soup = get_soup(book_url)
    title, author = get_books.fetch_title_and_author(soup)
    image_url = get_books.fetch_book_image_url(index_url, soup)
    genres = get_books.get_genres(soup)
    comments_text = get_books.downoload_comment(soup)
    book_page.update({'title': title,
                      'author': author,
                      'image_link': image_url,
                      'genres': genres,
                      'commets': comments_text})
    return book_page


def main():
    start_id, end_id, dest_folder = config.get_arguments()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    index_url = 'https://tululu.org/'
    logger = config.get_logging()

    all_fantastic_urls = parse_tululu_category.fetch_all_page_urls(start_id, end_id)

    fantastic_books = []
    for url in all_fantastic_urls:
        id = url.split('b')[1].replace('/', '')

        txt_url = 'https://tululu.org/txt.php'
        book_url = f'https://tululu.org/b{id}/'

        url_response = fetch_url_response(txt_url, id)

        try:
            check_for_redirect(url_response)
            book_page = parse_book_page(book_url, index_url)
            image_link = book_page['image_link']
            img_src = get_books.download_book_cover(image_link)
            title = book_page['title']
            filename = f'{title}.txt'
            book_path = save_book(filename, url_response, folder='books')
            author = book_page['author']
            soup = get_soup(book_url)
            comments = get_books.downoload_comment(soup)
            genres = get_books.get_genres(soup)
            fantastic_books.append({'title': title,
                                    'author': author,
                                    'img_src': img_src,
                                    'book_path': book_path,
                                    'comments': comments,
                                    'genres': genres})
        except requests.HTTPError:
            logger.error(f'книги id-{id} нет на сайте!')

    with open('2new_fantastic_books.json', 'w') as file:
        json.dump(fantastic_books, file,
                                      sort_keys=False,
                                      indent=4,
                                      ensure_ascii=False,
                                      separators=(',', ': '))


if __name__ == "__main__":
    main()
