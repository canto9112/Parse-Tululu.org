from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_urls(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector_url = '.d_book a'
    book_tags = soup.select(selector_url)

    urls = []
    for tag_url in book_tags:

        if tag_url.get('href').endswith('/'):
            id_book = tag_url.get('href')

            if id_book.startswith('/b'):
                book_url = urljoin(url, id_book)

                urls.append(book_url)
    return set(urls)


def fetch_all_page_urls(start_page, end_page):
    all_urls = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l55/{page}/'
        all_urls.extend(get_book_urls(url))
    return all_urls
