from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_urls(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector_url = '.d_book a'
    new_all_book_tag = soup.select(selector_url)

    urls = []
    for urlic in new_all_book_tag:
        if urlic.get('href').endswith('/'):
            tag = urlic.get('href')
            if tag.startswith('/b'):
                book_url = urljoin(url, tag)
                urls.append(book_url)
    return urls


def fetch_all_page_urls(start_page, end_page):
    all_urls = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l55/{page}/'
        all_urls.extend(get_book_urls(url))
    return all_urls
