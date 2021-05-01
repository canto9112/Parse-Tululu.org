import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template


def get_books(books_per_page):
    with open('media/JSON.json', 'r') as file:
        json_file = file.read()
    books = json.loads(json_file)
    return list(chunked(books, books_per_page))


def get_rendered_pages(template, books):
    rendered_pages = []
    for page_number, page in enumerate(books, 1):
        all_pages = len(books)
        rendered_page = template.render(books=page,
                                        all_pages=all_pages,
                                        current_page=page_number)
        page = {
            'page_number': page_number,
            'rendered_page': rendered_page
        }

        rendered_pages.append(page)

    return rendered_pages


def write_index_html(rendered_page):
    with open(f'pages/index{rendered_page["page_number"]}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page['rendered_page'])


def rebuild(books_per_page):
    template = get_template()
    books = get_books(books_per_page)
    rendered_pages = get_rendered_pages(template, books)
    os.makedirs('pages')
    for rendered_page in rendered_pages:
        write_index_html(rendered_page)

    print("Site rebuilt")


def main():
    books_per_page = 20

    rebuild(books_per_page)
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
