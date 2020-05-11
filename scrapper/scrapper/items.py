# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsList(scrapy.Item):
    name = scrapy.Field()
    days = scrapy.Field()

class DaysNews(NewsList):
    # define the fields for your item here like:
    day = scrapy.Field()

class Article(DaysNews):
    name = scrapy.Field()
    text = scrapy.Field()
