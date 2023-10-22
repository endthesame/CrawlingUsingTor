import scrapy
import os, json

with open('../../../../config.json', 'r') as config_file:
    config = json.load(config_file)

SITES_TO_CRAWL = config["sites_to_crawl"]
RESULTS_FOLDER = config["results_folder"]
RESULTS_FILE = config["results_file"]

class MetaSpider(scrapy.Spider):
    name = 'meta'

    def start_requests(self):
        # Считываем сайты из файла
        with open(SITES_TO_CRAWL, 'r') as file:
            sites = [line.strip() for line in file if line.strip()]
        
        for site in sites:
            yield scrapy.Request(url=site, callback=self.parse)

    def parse(self, response):
        # Извлечь метаданные. Здесь приведен пример извлечения title.
        # Вы должны модифицировать XPath в соответствии со структурой ваших сайтов.
        meta_data = {
            'title': response.xpath('//title/text()').get(),
            'publication_date': response.xpath('//*[@name="citation_publication_date"]/@content').get(),
        }

        # Поиск ссылки на PDF
        pdf_link = response.xpath('//a[contains(@href, "chapter-ag-pdf")]/@href').get()
        
        # Если ссылка на PDF найдена, создаем и возвращаем объект данных
        if pdf_link:
            absolute_pdf_link = response.urljoin(pdf_link)
            
            yield {
                'path': f"/assets/{response.url.split('//')[-1].split('/')[0]}/pdf",
                'metafields': meta_data
            }

            # Здесь также можно добавить код для скачивания PDF, если это требуется.
