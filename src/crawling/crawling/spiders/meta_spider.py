import scrapy
import os, json, hashlib
from datetime import datetime

from crawling.items import CrawlingItem, PdfDownloadItem
from crawling.spiders.site_extractors import edp, uspkhim
from crawling.downloader.pdf_downloader import PDFDownloader

class MetaSpider(scrapy.Spider):
    name = 'meta'
    marks_css_to_download_pdf = ['.special_article']
    link_buffer = []

    #added category where we save meta data
    def __init__(self, category='oxford', *args, **kwargs):
        super(MetaSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.pdf_links_folder = f"../../../assets/output/{self.category}/links"
        if not os.path.exists(self.pdf_links_folder):
            os.makedirs(self.pdf_links_folder)
        self.file_path = os.path.join(self.pdf_links_folder,self.category + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + '_pdf_links.txt')

    def print_ip(self, response):
        ip_info = response.json()
        self.logger.info(f"Current IP: {ip_info['origin']}")

    def start_requests(self):
        yield scrapy.Request(url="https://httpbin.org/ip", callback=self.print_ip, dont_filter=True)
        # Считываем сайты из файла
        with open('../../../assets/sites_to_crawl/sites.txt', 'r') as file:
            sites = [line.strip() for line in file if line.strip()]
        
        for site in sites:
            yield scrapy.Request(url=site, callback=self.parse)

    def parse(self, response):
        item = CrawlingItem()

        meta_data = edp.extract_meta_data(response) #ТУТ МЕНЯЕТСЯ ЗАДАНИЕ МЕТА ДЛЯ САЙТОВ
        #хеширует тайтл для названия файла
        title_hash = hashlib.sha256(meta_data['202'].encode()).hexdigest()
        date_hash = hashlib.sha256(meta_data['date'].encode()).hexdigest()
        item['metafields'] = meta_data
        yield item

        # Поиск ссылки на PDF
        pdf_link = edp.extract_pdf_link(response)
        
        # Если ссылка на PDF найдена - добавляем ее в буфер
        if pdf_link:
            add_pdf_link = False
            #проверка на соответствие классам css (в данном случае смотрим что док free или openaccess)
            for css_selector in self.marks_css_to_download_pdf:
                if response.css(css_selector):
                    add_pdf_link = True
                    break
            #проверяем что пред условие удоволетворено и тайтл найден
            if add_pdf_link and meta_data['202'] is not None:
                absolute_pdf_link = response.urljoin(pdf_link)
                pdf_filename = f"{self.category}_{title_hash}_{date_hash}.pdf"
                self.link_buffer.append((absolute_pdf_link, pdf_filename))

                if len(self.link_buffer) >= 10:
                    with open(self.file_path, 'a') as f:  # Используем режим 'a' для добавления ссылок, чтобы не перезаписать файл
                        for link, pdf_filename in self.link_buffer:
                            f.write(link + ' ' + pdf_filename + '\n')
                    self.link_buffer = []

    def closed(self, reason):
        # Записываем оставшиеся ссылки из буфера в файл, если они есть
        if self.link_buffer: 
            with open(self.file_path, 'a') as f:
                for link, pdf_filename in self.link_buffer:
                    f.write(link + ' ' + pdf_filename + '\n')
        downloader = PDFDownloader()
        downloader.run(self.file_path)
