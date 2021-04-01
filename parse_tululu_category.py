import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urljoin, urlsplit
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
import os
from pathvalidate import sanitize_filename


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_book_urls(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector_url = '.d_book a'
    url_book_tags = soup.select(selector_url)
    urls = []
    for tag_url in url_book_tags:
        if tag_url.get('href').endswith('/'):
            book_url_tag = tag_url.get('href')
            book_url = urljoin(url, book_url_tag)
            urls.append(book_url)
    return urls


def fetch_all_page_urls():
    all_urls = []
    for page in range(1, 2):
        url = f'https://tululu.org/l55/{page}/'
        all_urls.extend(get_book_urls(url))
    return all_urls
