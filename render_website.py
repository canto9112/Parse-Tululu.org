import json
from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from pprint import pprint
import os


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template


def get_books():
    with open('result/JSON.json', 'r') as my_file:
        file_json = my_file.read()
    books = json.loads(file_json)
    return list(chunked(books, 10))


def get_rendered_page(template, books):
    rendered_pages = []
    print(books)
    for page_number, page in enumerate(books, 1):
        print(page_number, page)
        rendered_page = template.render(books=page)
        rendered_pages.append(rendered_page)

    return rendered_pages


def get_index_html(rendered_page, page_number):

    with open(f'pages/index{page_number}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def rebuild():
    template = get_template()
    books = get_books()
    rendered_pages = get_rendered_page(template, books)
    os.makedirs('pages')
    for page_number, rendered_page in enumerate(rendered_pages, 1):
        get_index_html(rendered_page, page_number)

    print("Site rebuilt")


def main():
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()






