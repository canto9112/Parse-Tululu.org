import argparse
import logging

import requests


def get_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def get_arguments():
    parser = argparse.ArgumentParser(
                        description='Скрипт скачивает книги с сайта tululu.org')
    parser.add_argument('--start_page',
                        help='С какой страницы начать скачивание',
                        type=int,
                        default=1)
    parser.add_argument('--end_page',
                        help='Закончить скачивание на этой странице',
                        type=int,
                        default=2)
    parser.add_argument('--dest_folder',
                        help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON',
                        type=str,
                        default='result')
    parser.add_argument('--json_path',
                        help='Путь к *.json файлу с результатами',
                        type=str,
                        default='result')
    parser.add_argument('--skip_img',
                        help='Не скачивать картинки',
                        default=False)
    parser.add_argument('--skip_txt',
                        help='Не скачивать книги',
                        default=False)
    args = parser.parse_args()
    return {'start_page': args.start_page,
            'end_page': args.end_page,
            'dest_folder': args.dest_folder,
            'json_path': args.json_path,
            'skip_img': args.skip_img,
            'skip_txt': args.skip_txt}


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError