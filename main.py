import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path


def fetch_book(url, filename, path):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(f'{path}/{filename}', 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    path = 'books'
    Path(path).mkdir(parents=True, exist_ok=True)
    id = 0

    for book in range(1, 11):
        id += 1
        print(id)
        filename = f'id{id}.txt'
        url = f'https://tululu.org/txt.php?id={id}'
        fetch_book(url, filename, path)