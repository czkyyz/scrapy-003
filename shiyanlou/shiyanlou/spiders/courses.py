# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import CourseItem

class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url1 = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url1.format(i) for i in range(1,5))

    def parse(self, response):
        for i in response.css('li.col-12'):
            item = CourseItem({
                "name": i.css('a::text').re_first('\s*(\w*)'),
                "update_time":i.css('relative-time::attr(datetime)').extract_first()
            })
            course_url = response.urljoin(i.xpath('.//a/@href').extract_first())
            #print(course_url)
            request = scrapy.Request(url=course_url,callback=self.parse_code)
            request.meta['item'] = item
            yield request

    def parse_code(self,response):
        item = response.meta['item']
       # print('--------------------------------------')
       # print(item)
        if not response.xpath('//span[contains(@class,"num")]/text()').extract():
            pass
        else:
            item['commits'] = response.xpath('//span[contains(@class,"num")]/text()').extract()[0].strip()
            item['branches'] = response.xpath('//span[contains(@class,"num")]/text()').extract()[1].strip()
            item['releases'] = response.xpath('//span[contains(@class,"num")]/text()').extract()[2].strip()
            yield item
