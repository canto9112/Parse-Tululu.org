import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


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
    return books


def get_rendered_page(template, books):
    rendered_page = template.render(
        books=books
    )
    return rendered_page


def get_index_html(rendered_page):
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    template = get_template()
    books = get_books()
    rendered_page = get_rendered_page(template, books)
    get_index_html(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()






