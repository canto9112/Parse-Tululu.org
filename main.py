import argparse
import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import trange


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
    image_url_tag = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(url, image_url_tag)
    return image_url


def download_book_cover(url, folder='img'):
    Path(folder).mkdir(parents=True, exist_ok=True)

    cover_path = urlsplit(url).path
    filename = cover_path.split('/')[-1]

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


def downoload_comment(soup):
    comment_tag = soup.find_all('div', class_='texts')
    number_comments = len(comment_tag)
    comments_text = []
    if comment_tag:
        for number in range(0, number_comments):
            comment = comment_tag[number].text
            text = comment.split(')')[-1]
            comments_text.append(text)
    return comments_text


def get_genres(soup):
    genres_tag = soup.find_all('span', class_='d_book')
    text = genres_tag[0].text.split(':')[-1].strip()
    genres = text.split(',')
    return genres


def parse_book_page(book_url, index_url):
    book_page = {}
    soup = get_soup(book_url)
    title, author = fetch_title_and_author(soup)
    image_url = fetch_book_image_url(index_url, soup)
    genres = get_genres(soup)
    comments_text = downoload_comment(soup)
    book_page.update({'title': title,
                      'author': author,
                      'image_link': image_url,
                      'genres': genres,
                      'commets': comments_text})
    return book_page


def get_arguments():
    parser = argparse.ArgumentParser(
                        description='Скрипт скачивает книги с сайта tululu.org')
    parser.add_argument('--start_page',
                        help='С какой книги начать скачивание',
                        type=int,
                        default=1)
    parser.add_argument('--end_page',
                        help='Закончить скачивание на этой книге',
                        type=int,
                        default=10)
    args = parser.parse_args()
    return args.start_page, args.end_page


def main():
    start_id, end_id = get_arguments()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    index_url = 'https://tululu.org/'

    for id in trange(start_id, end_id + 1):
        txt_url = 'https://tululu.org/txt.php'
        book_url = f'https://tululu.org/b{id}/'

        url_response = fetch_url_response(txt_url, id)

        try:
            check_for_redirect(url_response)
            book_page = parse_book_page(book_url, index_url)
            title = book_page['title']
            image_link = book_page['image_link']
            author = book_page['author']
            filename = f'{id}. {title}'

            download_book_cover(image_link)
            save_book(filename, url_response, folder='books')
        except requests.HTTPError:
            pass


if __name__ == "__main__":
    main()
