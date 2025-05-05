import csv
import requests
import threading
from queue import Queue
from urllib.parse import urlparse
from datetime import datetime
import time
import sys


def check_url_availability(url, timeout=10):
    result = {
        "URL": url,
        "Статус": "Не доступен",
        "Код/Сообщение": None,
        "Время ответа (сек)": None,
        "IP-адрес": None,
        "Загружается контент": False,
        "Редирект": False,
        "Final URL": None,
    }

    try:
        if not urlparse(url).scheme:
            url = "http://" + url

        start_time = time.time()

        response = requests.get(
            url,
            allow_redirects=True,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
        )

        result["Время ответа (сек)"] = round(time.time() - start_time, 2)
        result["Код/Сообщение"] = response.status_code
        result["Final URL"] = response.url

        if response.url != url:
            result["Редирект"] = True

        if response.text.lower().find("<html") != -1:
            result["Загружается контент"] = True

        domain = urlparse(response.url).hostname
        result["IP-адрес"] = domain

        if response.status_code == 200 and result["Загружается контент"]:
            result["Статус"] = "Доступен"
        else:
            result["Код/Сообщение"] = (
                f"HTTP {response.status_code}, контент не загружен"
            )

    except requests.exceptions.SSLError as e:
        result["Код/Сообщение"] = f"SSL-ошибка: {str(e)}"
    except requests.exceptions.ConnectionError as e:
        result["Код/Сообщение"] = f"Ошибка подключения: {str(e)}"
    except requests.exceptions.Timeout as e:
        result["Код/Сообщение"] = f"Таймаут: {str(e)}"
    except requests.exceptions.TooManyRedirects as e:
        result["Код/Сообщение"] = f"Слишком много редиректов: {str(e)}"
    except requests.exceptions.RequestException as e:
        result["Код/Сообщение"] = f"Ошибка запроса: {str(e)}"
    except Exception as e:
        result["Код/Сообщение"] = f"Неизвестная ошибка: {str(e)}"

    return result


def process_urls(urls, results_queue):
    """Обрабатывает список URL и помещает результаты в очередь"""
    for url in urls:
        result = check_url_availability(url)
        results_queue.put((result["URL"], result["Статус"], result["Код/Сообщение"]))


def split_list(input_list, chunks):
    """Разделяет список на примерно равные части"""
    avg = len(input_list) / float(chunks)
    return [input_list[int(avg * i) : int(avg * (i + 1))] for i in range(chunks)]


def main(input_file, output_file=None):
    urls = []
    try:
        with open(input_file, mode="r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден")
        return

    if not urls:
        print("В файле нет URL для проверки.")
        return

    num_threads = min(4, max(1, len(urls) // 2))  # Оптимальное количество потоков

    url_chunks = split_list(urls, num_threads) if num_threads > 1 else [urls]
    results_queue = Queue()
    threads = []

    for chunk in url_chunks:
        thread = threading.Thread(target=process_urls, args=(chunk, results_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    results.sort(key=lambda x: urls.index(x[0]))

    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = input_file.rsplit(".", 1)[0]
        output_file = f"{base_name}_results_{timestamp}.csv"

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Статус", "Код/Сообщение"])
        writer.writerows(results)

    print(f"Проверка завершена. Результаты сохранены в {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python script.py <input_file> [<output_file>]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    main(input_file, output_file)
