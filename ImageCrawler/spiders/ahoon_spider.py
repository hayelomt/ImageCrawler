import sys
import os
sys.path.append(os.path.join('.','ImageCrawler','utils'))
import imgDownloader

import scrapy

os.makedirs('data', exist_ok=True)
f = open(os.path.join('data', 'links'), 'a')

class AhoonSpider(scrapy.Spider):
    name = "ahoon"

    start_urls = [
        "http://localhost:4000"
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(AhoonSpider, self).__init__(*args, **kwargs)
        self.imageDownloader = imgDownloader.ImageDownloader()

    def parse(self, response):
        for res in response.css('img::attr(src)').extract():
            print('URL:', response.url, ' RES:', res)
            f.write(response.url + '\t' + res + '\n')
            self.imageDownloader.download(res)  

        f.write('\n')

        navbar = response.css('ul.navbar-nav')
        for link in navbar.css('li a::attr(href)').extract():
            yield scrapy.Request(link, callback=self.parse)
