from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json


class Movie:
    def __init__(self, hdrezka_url):
        self._hdrezka_url = hdrezka_url
        self._name = _get_movie_name(hdrezka_url=self.hdrezka_url)
        self._direct_url = _get_movie_direct_url(hdrezka_url=self.hdrezka_url)

    @property
    def hdrezka_url(self):
        return self._hdrezka_url

    @property
    def name(self):
        return self._name

    @property
    def direct_url(self):
        return self._direct_url

    def download_film(self, save_path):
        from .file_utils import download_file
        try:
            download_file(url=self.direct_url, save_path=save_path)
        except Exception as e:
            print(f'error: {e}')


def _get_movie_name(hdrezka_url):
    try:
        browser = _browser()

        browser.get(hdrezka_url)

        movie_name = browser.find_element(By.CLASS_NAME, 'b-post__origtitle').text

        browser.quit()

        return movie_name

    except Exception as e:
        print(f'error: {e}')


def _get_movie_direct_url(hdrezka_url):
    try:
        browser = _browser()
        # Открытие страницы с фильмом
        browser.get(hdrezka_url)

        if not _check_and_reload(browser=browser, max_attempts=10):
            return

        _set_max_quality(browser)

        # Включение фильма ()
        play_button = browser.find_element(By.CLASS_NAME, 'b-player')
        browser.execute_script("arguments[0].click();", play_button)

        mp4_urls = []
        while not mp4_urls:
            logs = browser.get_log('performance')
            for entry in logs:
                message = json.loads(entry['message'])['message']
                if 'method' in message and message['method'] == 'Network.requestWillBeSent':
                    url = message['params']['request']['url']
                    if '.mp4' in url:
                        mp4_urls.append(url.split('.mp4')[0] + '.mp4')

        # Закрываем браузер
        browser.quit()

        url = mp4_urls[-1]
        print(url)

        return url

    except Exception as e:
        print(f'error: {e}')


def _set_max_quality(browser):
    # Найти элемент с id "cdnplayer_settings"
    settings_element = browser.find_element(By.ID, 'cdnplayer_settings')

    browser.execute_script("arguments[0].click();", settings_element.find_element(By.XPATH, '//pjsdiv[@fid="1"]'))

    # Найдите все элементы с атрибутом f2id
    elements_with_f2id = settings_element.find_elements(By.XPATH, '//*[@f2id]')

    # Инициализируйте переменную для хранения максимального значения f2id
    max_f2id = 1

    # Переберите найденные элементы и найдите максимальное значение f2id
    for element in elements_with_f2id:
        f2id_value = int(element.get_attribute('f2id'))
        if f2id_value > max_f2id:
            max_f2id = f2id_value

    browser.execute_script("arguments[0].click();", settings_element.find_element(By.XPATH, f'//pjsdiv[@f2id="{max_f2id}"]'))


def _check_and_reload(browser, max_attempts=3):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    for _ in range(max_attempts):
        try:

            # Попробуйте найти элемент с id "cdnplayer_settings"
            settings_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'cdnplayer_settings'))
            )

            # Если элемент найден, вернитесь
            return True
        except Exception as e:
            print(f"Элемент 'cdnplayer_settings' не найден")

        # Если элемент не найден, перезагрузите страницу
        browser.refresh()

    # Если после нескольких попыток элемент так и не найден, возможно, что что-то не в порядке.
    print("Не удалось найти элемент 'cdnplayer_settings' после нескольких попыток.")

    return False


def _browser():
    # Настройки браузера
    options = webdriver.ChromeOptions()
    options.add_argument('--mute-audio')
    options.add_argument('--headless')  # Включение режима headless (без отображения окна браузера)
    options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

    # Инициализация драйвера Chrome
    service = webdriver.ChromeService(ChromeDriverManager().install())

    driver = webdriver.Chrome(options=options, service=service)

    return driver
