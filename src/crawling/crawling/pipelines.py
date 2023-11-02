# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import json
import hashlib
from crawling.items import PdfDownloadItem
from random import randint


class CrawlingPipeline:
    def process_item(self, item, spider):
        return item

class JsonFeedPipeline:

    def __init__(self):
        pass
        # self.buffer = []

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        title = item['metafields']['title']
        #проверяем что в мете есть title, потому что если title нет, то нам такой док и не нужен
        if title: 
            title_hash = hashlib.sha256(item['metafields']['title'].encode()).hexdigest()
            date_hash = hashlib.sha256(item['metafields']['date'].encode()).hexdigest()
            file_name = f"{spider.category}_{title_hash}_{date_hash}.json"
            folder_path = f"../../../assets/output/{spider.category}/jsons/"
            full_path = os.path.join(folder_path, file_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Теперь записываем каждый элемент в свой собственный файл, а не ждем, пока буфер будет заполнен
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(item['metafields'], f, indent=4, ensure_ascii=False)

        return item

    def close_spider(self, spider):
        pass
