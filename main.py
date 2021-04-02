import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import config
import get_books
import parse_tululu_category


def fetch_url_response(url, id):
    params = {
        'id': id
    }
    response = requests.get(url, params=params, verify=False)
    response.raise_for_status()
    return response


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def save_json(books, filename):
    with open(f'{filename}.json', 'w') as file:
        json.dump(books, file,
                  sort_keys=False,
                  indent=4,
                  ensure_ascii=False,
                  separators=(',', ': '))


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    logger = config.get_logging()

    start_id, end_id, dest_folder = config.get_arguments()

    index_url = 'https://tululu.org/'
    txt_url = 'https://tululu.org/txt.php'
    json_filename = 'JSON'

    catefory_urls = parse_tululu_category.fetch_all_page_urls(start_id, end_id)

    books_json = []
    for url in catefory_urls:

        id = url.split('b')[1].replace('/', '')
        book_url = f'https://tululu.org/b{id}/'
        url_response = fetch_url_response(txt_url, id)

        try:
            check_for_redirect(url_response)
            book_page = get_books.parse_book_page(book_url, index_url)
            image_link = book_page['image_link']
            img_src = get_books.download_book_cover(image_link)
            title = book_page['title']
            filename = f'{title}.txt'
            book_path = get_books.save_book(filename, url_response, folder='books')
            author = book_page['author']
            soup = get_books.get_soup(book_url)
            comments = get_books.download_comment(soup)
            genres = get_books.get_genres(soup)
            books_json.append({'title': title,
                                    'author': author,
                                    'img_src': img_src,
                                    'book_path': book_path,
                                    'comments': comments,
                                    'genres': genres})
        except requests.HTTPError:
            logger.error(f'книги id-{id} нет на сайте!')

    save_json(books_json, json_filename)


if __name__ == "__main__":
    main()
