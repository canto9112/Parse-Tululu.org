import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
                        description='Скрипт скачивает книги с сайта tululu.org')
    parser.add_argument('--start_page',
                        help='С какой книги начать скачивание',
                        type=int,
                        default=1)
    parser.add_argument('--end_page',
                        help='Закончить скачивание на этой книге',
                        type=int,
                        default=10)
    parser.add_argument('--dest_folder',
                        help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON,',
                        type=str,
                        default='result')
    args = parser.parse_args()
    return args.start_page, args.end_page, args.dest_folder