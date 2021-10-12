# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess

class TitlesspiderSpider(scrapy.Spider):
    name = 'titlesSpider'
    start_urls = ["https://www.lse.co.uk/news/archive.html?page="+str(i) for i in range(0,1000)]

    def parse(self, response):
        if response.status == 200:
            all_links = response.xpath('//a[@class="news__story-title-link"]/@href').extract()
            for link in all_links:
                yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        if response.status == 200:
            title = response.xpath('//h1[@class="title__title"]/text()[1]').extract()[0]
            text = [
                ' '.join(
                    line.strip()
                    for line in p.xpath('.//text()').extract()
                    if line.strip()
                )
                for p in response.xpath('//div[@class="news-article__content"]')
            ][0]

            yield{
                "title": title,
                "article": text,
                "url": response.url
            }