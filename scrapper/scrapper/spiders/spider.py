# this is where most of the scrapy logic is going to go
import scrapy
from datetime import datetime
import json
import pickle
import os
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapper.items import*
from scrapy.http import Request

# scrapy.spider is a required input for our classes 
class scrapper(scrapy.Spider):
    name = "myscrapper" #this is how u will refer to my spiderling

    bad = [
        'disclaimer',
        'Disclaimer',
        'author',
        'Author',
        '©',
        'Last modified:',
        'last modified:',
        'Last Modified:',
        'We use cookies',
        '|',
        'image courtesy',
        'Sign up for our',
        'sign up for our',
        'email',
        'Email',
        'Related:',
        '<p>©',
        'rights reserved',
        'Rights Reserved'
    ]

    failedUrls = [
    ]
    output = {}

    def start_requests(self):
        urls = [
            'https://coinstat.nl/en/archive-news'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseDays)

    
    def parseDays(self, response):
        count = 0
        for link in response.xpath('//div[@class="panel-body form-section"]/ul/li'):
            count += 1
            req = Request(link.xpath('.//a/@href').get()[1:],callback=self.parseDaysArticles,
            priority=count, cb_kwargs=dict(day=link.xpath('.//a/text()').get()))
            yield req


    
    def parseDaysArticles(self, response, day):
        # thisDay = []
        count = 0
        myday = []
        self.output[day] = myday
        for link in response.xpath('//div[@class="panel-body form-section"]/ul/li'):
            text = link.xpath('.//a/text()').get()
            try:
                if text.find("Bitcoin") != -1 or text.find("BTC") != -1:
                    myday.append(None)
                    count += 1
                    req = Request(link.xpath(".//a/@href").get(),
                    callback=self.parseMiddlePage, cb_kwargs=dict(aday=day))
                    req.cb_kwargs['num'] = count
                    yield req
                    # yield response.follow(link.xpath(".//a/@href").get(), callback=self.parseMiddlePage)
                    # yield scrapy.Request(url=link.xpath('.//a/@href').get(), callback=self.parse3)
            except:
                print("error at")
                print(link)
        # self.output[day] = thisDay
 




    def parseMiddlePage(self, response, num, aday):
        try:
            time = response.xpath('//div/span[@class="badge bg-red btn"]/text()').get()
            time = time.strip()
            req = Request(response.xpath('//div[@class="col-lg-8"]/div/a[@target="_blank"]/@href').get(), self.parseArticle)
            req.cb_kwargs['day'] = aday
            req.cb_kwargs['number'] = num
            req.cb_kwargs['timestamp'] = time
            return req
            # yield scrapy.Request(url=response.xpath('//div[@class="col-lg-8"]/div/a[@target="_blank"]/@href').get(), callback=self.parseArticle)
        except:
            self.failedUrls.append(response.url)
            
    
    def parseArticle(self, response, timestamp, day, number):
        art = []
        result = response.xpath('//body//p[not(ancestor::footer or ancestor::header or ancestor::*[\
            (contains(@class, "footer") or contains(@class, "widget") or contains(@class, "tweet") or contains(@class, "author") or contains(@class, "caption")\
                or contains(@class, "related") or contains(@class, "affiliat")\
                    or contains(@id, "author") or contains(@class, "form-") or contains(@class, "prev-next"))\
                        or contains(@class, "disclosure") or contains(@class, "cookies")])]').getall()
        for r in result:
            if not any(x in r for x in self.bad):
                text = Selector(text=r).xpath('//text()').getall()
                text = ''.join(text) + " "
                art.append(text)
        art = ''.join(art)
        art = (response.url, timestamp, art)
        self.output[day][number-1] = art
            
            

            

