from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_urls(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector_url = '.bookimage a'
    book_tags = soup.select(selector_url)

    urls = []
    for tag_url in book_tags:
        if tag_url.get('href').endswith('/'):
            book_id = tag_url.get('href')
            if book_id.startswith('/b'):
                book_url = urljoin(url, book_id)
                urls.append(book_url)
    return set(urls)


def fetch_all_page_urls(start_page, end_page):
    urls = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l55/{page}/'
        urls.extend(get_book_urls(url))
    return urls


def get_last_page_number():
    url = 'https://tululu.org/l55/'
    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector_page = '.center .npage'
    page_tags = soup.select(selector_page)
    return page_tags[-1].text



