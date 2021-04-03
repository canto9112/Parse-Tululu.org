import json
from pathlib import Path

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import config
import parese_book
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

    start_id, end_id, dest_folder, json_path, skip_imgs = config.get_arguments()
    Path(json_path).mkdir(parents=True, exist_ok=True)
    index_url = 'https://tululu.org/'
    txt_url = 'https://tululu.org/txt.php'
    json_filename = 'JSON'

    category_urls = parse_tululu_category.fetch_all_page_urls(start_id, end_id)
    print(skip_imgs)
    books_json = []
    for url in category_urls:

        id = url.split('b')[1].replace('/', '')
        book_url = f'https://tululu.org/b{id}/'
        url_response = fetch_url_response(txt_url, id)

        try:
            check_for_redirect(url_response)
            book_page = parese_book.parse_book_page(book_url, index_url)
            image_link = book_page['image_link']
            img_src = parese_book.download_book_cover(image_link, dest_folder, skip_imgs)
            title = book_page['title']
            filename = f'{title}.txt'
            book_path = parese_book.save_book(filename, url_response, dest_folder)
            author = book_page['author']
            soup = parese_book.get_soup(book_url)
            comments = parese_book.download_comment(soup)
            genres = parese_book.get_genres(soup)
            books_json.append({'title': title,
                               'author': author,
                               'img_src': img_src,
                               'book_path': book_path,
                               'comments': comments,
                               'genres': genres})
        except requests.HTTPError:
            logger.error(f'книги id-{id} нет на сайте!')

    save_json(books_json, json_filename, json_path)


if __name__ == "__main__":
    main()
