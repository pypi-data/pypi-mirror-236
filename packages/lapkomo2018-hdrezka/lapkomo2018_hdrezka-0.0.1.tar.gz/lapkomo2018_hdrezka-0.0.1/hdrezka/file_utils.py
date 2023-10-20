import requests
from tqdm import tqdm
import re
import os


def download_file_with_progressbar(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Проверяем и создаем директорию, если ее нет
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024  # Размер чанка для записи (1 КБ)

        with open(save_path, 'wb') as file:
            with tqdm(total=total_size, unit="B", unit_scale=True, unit_divisor=1024, desc="Скачивание") as pbar:
                for data in response.iter_content(chunk_size):
                    file.write(data)
                    pbar.update(len(data))
        print(f"Файл успешно скачан и сохранен в {save_path}")
    else:
        print(f"Не удалось скачать файл в {save_path}")


def download_file(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Проверяем и создаем директорию, если ее нет
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Файл успешно скачан и сохранен в {save_path}")
    else:
        print(f"Не удалось скачать файл в {save_path}")


def normalize_filename(filename):
    # Заменить недопустимые символы (например, / и \) на подчеркивания
    filename = re.sub(r'[\/:*?"<>|]', '_', filename)

    # Удалить пробелы в начале и конце
    filename = filename.strip()

    # Если имя файла станет пустым после нормализации, вы можете задать имя по умолчанию
    if not filename:
        movie_name = "default_name"

    return filename
