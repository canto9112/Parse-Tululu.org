import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os


def fetch_book_url(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response


def save_book(filename, response, folder='books'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = os.path.join(folder, sanitize_filename(filename))
    with open(f'{path}.txt', 'wb') as file:
        file.write(response.content)
    return f'{path}.txt'


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


def get_book_title(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1').text

    if len(title_tag.split('::')) == 2:
        title = title_tag.split('::')[0].strip()
        author = title_tag.split('::')[1].strip()
    else:
        title = title_tag.split('::')[0].strip()
        author = 'Нет автора'
    return title, author


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    id = 0
    for book in range(1, 11):
        id += 1
        txt_url = f'https://tululu.org/txt.php?id={id}'
        book_url = f'https://tululu.org/b{id}/'

        title, author = get_book_title(book_url)
        filename = f'{id}. {title}'
        response = fetch_book_url(txt_url)
        try:
            check_for_redirect(response)
            filepath = save_book(filename, response, folder='books')
            print(filepath)
        except requests.HTTPError:
            print('requests.HTTPError')
            continue

