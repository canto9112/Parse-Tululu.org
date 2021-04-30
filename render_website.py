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


def get_books():
    with open('result/JSON.json', 'r') as my_file:
        file_json = my_file.read()
    books = json.loads(file_json)
    return list(chunked(books, 20))


def get_rendered_page(template, books):
    rendered_pages = []
    for page_number, page in enumerate(books, 1):
        pages = {}
        all_pages = (len(books))
        rendered_page = template.render(books=page,
                                        all_pages=all_pages,
                                        current_page=page_number)
        pages.update({'page_number': page_number,
                      'rendered_page': rendered_page})
        rendered_pages.append(pages)

    return rendered_pages


def write_index_html(rendered_page):
    with open(f'pages/index{rendered_page["page_number"]}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page['rendered_page'])


def rebuild():
    template = get_template()
    books = get_books()
    rendered_pages = get_rendered_page(template, books)
    os.makedirs('pages')
    for rendered_page in rendered_pages:
        write_index_html(rendered_page)

    print("Site rebuilt")


def main():
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == '__main__':
    main()
