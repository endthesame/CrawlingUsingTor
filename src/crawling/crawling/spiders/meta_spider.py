import scrapy
import os, json, hashlib
from random import randint

from crawling.items import CrawlingItem, PdfDownloadItem
from crawling.spiders.site_extractors import edp

class MetaSpider(scrapy.Spider):
    name = 'meta'

    #added category where we save meta data
    def __init__(self, category='oxford', *args, **kwargs):
        super(MetaSpider, self).__init__(*args, **kwargs)
        self.category = category

    def print_ip(self, response):
        # Извлечь и распечатать ваш текущий IP из ответа
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
        # Извлечь метаданные. Здесь приведен пример извлечения title.
        # Вы должны модифицировать XPath в соответствии со структурой ваших сайтов.
        item = CrawlingItem()

        meta_data = edp.extract_meta_data(response)
        #хеширует тайтл для названия файла
        title_hash = hashlib.sha256(meta_data['title'].encode()).hexdigest()
        item['metafields'] = meta_data
        yield item

        # Поиск ссылки на PDF
        pdf_link = edp.extract_pdf_link(response)
        
        # Если ссылка на PDF найдена - скачиваем ее
        if pdf_link:
            absolute_pdf_link = response.urljoin(pdf_link)
            
            pdf_folder = f"../../../assets/output/{self.category}"
            pdf_filename = f"{self.category}_{title_hash}_{randint(1,10000000)}.pdf"
            
            yield scrapy.Request(absolute_pdf_link, callback=self.save_pdf, meta={'folder': pdf_folder, 'filename': pdf_filename})

    def save_pdf(self, response):
        folder = response.meta['folder']
        filename = response.meta['filename']
        
        pdf_folder = os.path.join(folder, "pdfs")
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        print("Starting download file:", filename)
        with open(os.path.join(pdf_folder, filename), 'wb') as file:
            file.write(response.body)
