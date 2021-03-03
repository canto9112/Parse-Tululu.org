import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def fetch_book():
    url = 'https://tululu.org/txt.php?id=32168'
    response = requests.get(url, verify=False)
    response.raise_for_status()
    filename = 'first_book.txt'
    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    fetch_book()