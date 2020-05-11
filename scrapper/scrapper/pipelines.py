# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pickle

class ScrapperPipeline:
    def process_item(self, item, spider):
        return item
    
    def close_spider(self, spider):
        with open("failedUrls.txt", 'w') as f:
            for x in spider.failedUrls:
                f.write(x)
        with open("output.p", 'wb') as f:
            pickle.dump(spider.output, f)