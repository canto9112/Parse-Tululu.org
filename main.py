import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path


def fetch_book_url(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response


def save_book(filename, path, response):
    with open(f'{path}/{filename}', 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    path = 'books'
    Path(path).mkdir(parents=True, exist_ok=True)

    id = 0
    for book in range(1, 11):
        id += 1
        filename = f'id{id}.txt'
        url = f'https://tululu.org/txt.php?id={id}'

        response = fetch_book_url(url)
        try:
            check_for_redirect(response)
            save_book(filename, path, response)
        except requests.HTTPError:
            print('requests.HTTPError')
            continue

