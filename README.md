# ls_brute

Как использовать:

    Установите зависимости:

    pip install requests

    Создайте файл wordlist.txt с путями для проверки, например:

    /admin
    /login
    /backup
    /config
    /test
    /secret

    Запустите инструмент:
    
    python advanced_dirbuster.py http://example.com wordlist.txt -t 20 -x .php .html -o results.txt

Параметры командной строки:

    url: Базовый URL для сканирования.

    wordlist: Путь к файлу со словарем.

    -t, --threads: Количество потоков (по умолчанию 10).

    -x, --extensions: Расширения файлов для проверки (например, .php, .html).

    -o, --output: Файл для сохранения результатов.

    -p, --proxy: Прокси для использования (например, http://127.0.0.1:8080).

    -T, --timeout: Тайм-аут запроса в секундах (по умолчанию 5).

    -u, --user-agent: Пользовательский заголовок User-Agent.

Особенности:

    Многопоточность: Использует ThreadPoolExecutor для ускорения перебора.

    Расширения файлов: Поддерживает проверку путей с различными расширениями.

    Логирование: Выводит подробные логи в консоль.

    Сохранение результатов: Сохраняет найденные пути в файл.

    Гибкость: Поддерживает прокси, кастомные заголовки и тайм-ауты.

Пример вывода:

2023-10-10 12:00:00 - INFO - [*] Starting directory brute-force on http://example.com
2023-10-10 12:00:00 - INFO - [*] Loaded 1000 paths from the wordlist.
2023-10-10 12:00:05 - INFO - [+] Found: http://example.com/admin (Status: 200)
2023-10-10 12:00:10 - INFO - [+] Found: http://example.com/login (Status: 200)
2023-10-10 12:00:15 - INFO - [*] Scan complete.
2023-10-10 12:00:15 - INFO - [*] Time taken: 15.23 seconds
2023-10-10 12:00:15 - INFO - [+] Found paths:
  - http://example.com/admin
  - http://example.com/login
2023-10-10 12:00:15 - INFO - [*] Results saved to results.txt

Этот инструмент является мощным и гибким решением для поиска скрытых ресурсов на веб-серверах. Используйте его только в законных целях!
