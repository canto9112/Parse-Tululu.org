import argparse
import logging


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
                        default=10)
    parser.add_argument('--dest_folder',
                        help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON,',
                        type=str,
                        default='result')
    parser.add_argument('--json_path',
                        help='Путь к *.json файлу с результатами',
                        type=str,
                        default='result')
    parser.add_argument('--skip_imgs',
                        help='Не скачивать картинки',
                        action='store_false')
    parser.add_argument('--skip_txt',
                        help='Не скачивать книги',
                        action='store_false')
    args = parser.parse_args()
    return args.start_page, args.end_page, args.dest_folder, args.json_path, args.skip_imgs, args.skip_txt