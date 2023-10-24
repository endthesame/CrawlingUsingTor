# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import json
from crawling.items import PdfDownloadItem


class CrawlingPipeline:
    def process_item(self, item, spider):
        return item

class JsonFeedPipeline:

    def __init__(self):
        self.items = {'docs': []}
        self.buffer = []
        self.buffer_limit = 10  # Мы записываем данные после того, как буфер достигнет этого размера

    def open_spider(self, spider):
        folder_path = f"../../../assets/output/{spider.category}/"
        file_name = f"{spider.category}.json"
        self.full_path = os.path.join(folder_path, file_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Если файл уже существует, читаем его содержимое
        if os.path.exists(self.full_path):
            with open(self.full_path, 'r') as f:
                self.items = json.load(f)

    def process_item(self, item, spider):
        print("Item is being processed in JsonFeedPipeline!")
        self.buffer.append(dict(item))

        if len(self.buffer) >= self.buffer_limit:
            self.items['docs'].extend(self.buffer)
            with open(self.full_path, 'w') as f:
                json.dump(self.items, f, indent=4)
            self.buffer = []

        return item

    def close_spider(self, spider):
        if self.buffer:
            self.items['docs'].extend(self.buffer)
            with open(self.full_path, 'w') as f:
                json.dump(self.items, f, indent=4)
