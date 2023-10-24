import scrapy
import os, json, hashlib

from crawling.items import CrawlingItem, PdfDownloadItem

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

        authors = response.css('.linked-name::text').getall()
        authors_string = ', '.join(authors)

        abstract_texts = response.css('section.abstract p::text').getall()
        full_abstract = ' '.join(abstract_texts).strip()

        keywords = response.css('.kwd-group .kwd-part::text').getall()
        formatted_keywords = ', '.join(keywords).strip()

        meta_data = {
            'title': response.xpath('//title').get(),
            'date': response.xpath('//*[@name="citation_publication_date"]/@content').get(),
            'mf_doi': response.xpath('//*[@name="citation_doi"]/@content').get(),
            'author': authors_string,
            'mf_journal': response.xpath('//*[@name="citation_journal_title"]/@content').get(),
            'volume_info': response.xpath('//*[@name="citation_volume"]/@content').get(),
            'issue_info': response.xpath('//*[@name="citation_issue"]/@content').get(),
            'mf_issn': response.xpath('//*[@name="citation_issn"]/@content').get(),
            'mf_publisher': response.xpath('//*[@name="citation_publisher"]/@content').get(),
            'abstract': full_abstract,
            'keywords': formatted_keywords,
            'mf_url': response.url

        }
        #хеширует тайтл для названия файла
        title_hash = hashlib.sha256(meta_data['title'].encode()).hexdigest()

        item['path'] = f"/assets/output/{self.category}/pdfs/{self.category}_{title_hash}.pdf"
        item['metafields'] = meta_data
        yield item

        # Поиск ссылки на PDF
        pdf_link = response.xpath('//a[contains(@href, ".pdf")]/@href').get()
        
        # Если ссылка на PDF найдена - скачиваем ее
        if pdf_link:
            absolute_pdf_link = response.urljoin(pdf_link)
            
            pdf_folder = f"../../../assets/output/{self.category}"
            pdf_filename = f"{self.category}_{title_hash}.pdf"
            
            yield scrapy.Request(absolute_pdf_link, callback=self.save_pdf, meta={'folder': pdf_folder, 'filename': pdf_filename})

    def save_pdf(self, response):
        folder = response.meta['folder']
        filename = response.meta['filename']
        
        pdf_folder = os.path.join(folder, "pdfs")
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        
        with open(os.path.join(pdf_folder, filename), 'wb') as file:
            file.write(response.body)
