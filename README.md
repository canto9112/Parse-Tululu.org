# Парсер книг с сайта tululu.org
Парсер скачивает книги жанра ```Фантастика``` с сайта [tululu.org](http://tululu.org)

## Запуск
Для запуска скрипта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`


## Пример сайта
[Онлайн библиотека](https://canto9112.github.io/Parse-Tululu.org/pages/index1.html)

## Аргументы парсера

1. С какой страницы начать скачивание ```--start_page``` (по умолчанию указана страницы 1);
2. Закончить скачивание на этой странице ```--end_page``` (по умолчанию указан номер последней страницы в категории);     
3. Путь к каталогу с результатами парсинга: картинкам, книгам, JSON файл ```--dest_folder``` (по умолчанию папка ```result``` );   
4. Путь к *.json файлу с результатами ```--json_path``` (по умолчанию папка ```result``` );       
5. Не скачивать картинки ```--skip_imgs``` (по умолчанию папка ```False``` );
6. Не скачивать книги ```--skip_txt``` (по умолчанию папка ```False``` ).


Пример 1: ```>>> python main.py``` Скачает книги с 1 по 2 страницу;

Пример 2: ```>>> python main.py --start_page 1 --end_page 30 --dest_folder My_folder``` Скачает книги с 1 по 30 страницу;

Пример 3: ```>>> python main.py --dest_folder My_folder``` Скачает книги с 1 по последнюю страницу в папку ```My_folder```;

Пример 4: ```>>> python main.py --json_path folder_json``` Скачает книги с 1 по последнюю  страницу в папку ```result``` а JSON файл с результатами в папку ```folder_json```;

Пример 5: ```>>> python main.py --skip_imgs``` Скачает книги без картинок с 1 по последнюю  страницу в папку ```result```;

Пример 6: ```>>> python main.py --dest_folder My_folder --skip_txt``` Скачает книги без .txt файлов с 1 по последнюю  страницу в папку ```My_folder```.


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
