# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    metafields = scrapy.Field()
    #path = scrapy.Field()

class PdfDownloadItem(scrapy.Item):
    pdf_url = scrapy.Field()
    pdf_folder = scrapy.Field()
    pdf_filename = scrapy.Field()
