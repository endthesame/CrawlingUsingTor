import requests, time
from stem import Signal
from stem.control import Controller
import os

CATEGORY = "uspkhim"

class PDFDownloader:

    MAX_RETRIES = 3  # Максимальное количество попыток скачивания
    ERROR_PATTERNS = {'waitforfullt'}  # Множество с ошибками или паттернами для проверки

    def __init__(self):
        # Настройка TOR через Privoxy
        self.session = requests.Session()
        self.session.proxies = {"http": "http://127.0.0.1:8118", "https": "http://127.0.0.1:8118"}

    def has_error(self, response):
        # Проверка на наличие ошибок в URL или статусе
        if any(pattern in response.url for pattern in self.ERROR_PATTERNS):
            return True
        if response.status_code != 200 and not (300 <= response.status_code < 400):
            return True
        return False
    
    def is_tor_available(self):
    # Эта функция проверяет, доступен ли Tor
        try:
            response = self.session.get("https://httpbin.org/ip")
            if response.status_code == 200:
                return True
            return False
        except:
            return False

    def download_pdf(self, pdf_link, filename):
        # Скачивание файла
        path_to_pdf_folder = f"../../../assets/output/{CATEGORY}/pdfs"

        if not os.path.exists(path_to_pdf_folder):
            os.makedirs(path_to_pdf_folder)

        file_path = os.path.join(path_to_pdf_folder, filename)

        retries = 0
        while retries < self.MAX_RETRIES:
            while not self.is_tor_available():
                print("Tor недоступен. Ожидание 2 минуты перед следующей проверкой...")
                time.sleep(120)

            response = self.session.get(pdf_link)

            if not self.has_error(response):
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Successfully downloaded {pdf_link} to {file_path}")  # Сообщение об успешном скачивании
                return  # Успешное скачивание, выход из функции
            else:
                print("Error to downloading: ", pdf_link, "\n Changing IP")
                self.change_ip_and_wait()  # Смена IP и пауза перед следующей попыткой

        print(f"Failed to download {pdf_link} after {self.MAX_RETRIES} attempts.")  # Сообщение, если скачивание не удалось

    def change_ip(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def change_ip_and_wait(self):
        self.change_ip()
        time.sleep(7)

    def run(self, filename):
        with open(filename, 'r') as f:
            links = f.readlines()
        
        for line in links:
            link, filename = line.strip().split(' ')
            try:
                print("Trying to download", link)
                self.download_pdf(link, filename)
            except Exception as e:
                print(f"Error downloading {link}. Retrying with new IP...")
                self.change_ip()
                self.download_pdf(link, filename)

if __name__ == "__main__":
    downloader = PDFDownloader()
    # Тут нужен путь к вашему файлу с ссылками.
    downloader.run("../../../assets/sites_to_crawl/sites.txt")
