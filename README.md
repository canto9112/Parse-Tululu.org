# Парсер книг с сайта tululu.org
Парсер скачивает книги с сайта [tululu.org](http://tululu.org)

## Запуск
Для запуска скрипта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите сервер командой `python3 manage.py runserver`

## Аргументы
Чтобы скачать книги нужно передать аргументы: ```--start_page и --end_page```

Пример: ```python main.py --start_page 10 --end_page 30```

По умолчанию стоят значения:
 * --start_page = 1
 * --end_page = 10


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
