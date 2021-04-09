import json
from pathlib import Path

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import config
import parse_book
import parse_tululu_category


def fetch_download_link(url, id):
    params = {
        'id': id
    }
    response = requests.get(url, params=params, verify=False)
    response.raise_for_status()
    return response


def save_json(books, filename, path):
    with open(f'{path}/{filename}.json', 'w') as file:
        json.dump(books, file,
                  sort_keys=False,
                  indent=4,
                  ensure_ascii=False,
                  separators=(',', ': '))


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    logger = config.get_logging()

    arguments = config.get_arguments()

    Path(arguments['json_path']).mkdir(parents=True, exist_ok=True)
    index_url = 'https://tululu.org/'
    txt_url = 'https://tululu.org/txt.php'
    json_filename = 'JSON'

    books_urls = parse_tululu_category.fetch_all_page_urls(arguments['start_page'], arguments['end_page'])

    books_json = []
    for url in books_urls:
        id = url.split('b')[1].replace('/', '')
        book_url = f'https://tululu.org/b{id}/'
        download_link = fetch_download_link(txt_url, id)
        try:
            config.check_for_redirect(download_link)
            book_page = parse_book.parse_book_page(book_url, index_url)
            image_link = book_page['image_link']
            img_src = parse_book.download_book_cover(image_link, arguments['dest_folder'], arguments['skip_imgs'])
            title = book_page['title']
            filename = f'{title}.txt'
            book_path = parse_book.save_book(filename, download_link, arguments['dest_folder'], arguments['skip_txt'])
            author = book_page['author']
            soup = parse_book.get_soup(book_url)
            comments = parse_book.get_comments(soup)
            genres = parse_book.get_genres(soup)
            books_json.append({'title': title,
                               'author': author,
                               'img_src': img_src,
                               'book_path': book_path,
                               'comments': comments,
                               'genres': genres})
        except requests.HTTPError:
            logger.error(f'книги id-{id} нет на сайте!')

    save_json(books_json, json_filename, arguments['json_path'])


if __name__ == "__main__":
    main()
