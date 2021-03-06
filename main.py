import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os
from urllib.parse import urljoin, urlparse, urlsplit, unquote


def fetch_book_url(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response


def get_soup(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


def fetch_title_and_author(soup):
    title_tag = soup.find('h1').text
    if len(title_tag.split('::')) == 2:
        title = title_tag.split('::')[0].strip()
        author = title_tag.split('::')[1].strip()
    else:
        title = title_tag.split('::')[0].strip()
        author = 'Нет автора'
    return title, author


def fetch_book_image_url(url, soup):
    title_tag = soup.find('div', class_='bookimage').find('img')['src']
    url_image = urljoin(url, title_tag)
    return url_image


def download_book_cover(url, folder='img'):
    Path(folder).mkdir(parents=True, exist_ok=True)

    name = urlsplit(url).path
    filename = name.split('/')[-1]

    path = os.path.join(folder, sanitize_filename(filename))
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def save_book(filename, response, folder='books'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = os.path.join(folder, sanitize_filename(filename))
    with open(f'{path}.txt', 'wb') as file:
        file.write(response.content)
    return f'{path}.txt'


def downoload_comment(soup):
    title_tag = soup.find_all('div', class_='texts')
    number_comments = len(title_tag)
    comments_text = []
    if title_tag:
        for number in range(0, number_comments):
            comment = title_tag[number].text
            text = comment.split(')')[-1]
            comments_text.append(text)
    else:
        print('Комментариев нет!')
    return comments_text


def get_genres(soup):
    title_tag = soup.find_all('span', class_='d_book')
    text = title_tag[0].text.split(':')[-1].strip()
    genres = text.split(',')
    print(genres)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    index_url = 'https://tululu.org/'

    id = 0
    for book in range(1, 11):
        id += 1
        txt_url = f'https://tululu.org/txt.php?id={id}'
        book_url = f'https://tululu.org/b{id}/'
        soup = get_soup(book_url)
        title, author = fetch_title_and_author(soup)
        filename = f'{id}. {title}'
        response = fetch_book_url(txt_url)

        try:
            check_for_redirect(response)
            image_url = fetch_book_image_url(index_url, soup)
            print('Заголовок', title)
            get_genres(soup)
            # print(image_url)
            # comments_text = downoload_comment(soup)
            # for comment in comments_text:
            #     print(comment)
            # download_book_cover(image_url)
            # filepath = save_book(filename, response, folder='books')
            # print(filepath)
        except requests.HTTPError:
            pass

