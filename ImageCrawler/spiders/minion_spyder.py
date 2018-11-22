import sys
sys.path.append('./ImageCrawler/utils')
import imgDownloader

import scrapy
import os

os.makedirs('data', exist_ok=True)
f = open('data/links', 'a')

class MinionSpider(scrapy.Spider):
    name = "minion"

    start_urls = [
        "https://pixabay.com/en/photos/minion/"
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(MinionSpider, self).__init__(*args, **kwargs)
        self.imageDownloader = imgDownloader.ImageDownloader()

    def parse(self, response):
        links = [i.split(' ')[0] for i in 
        response.css('div.item a img::attr(srcset), div.item a img::attr(data-lazy-srcset)').extract()]

        for link in links:
            self.imageDownloader.download(link)
            print('URL:', response.url, ' Link:', link)
            f.write(response.url + '\t' + link + '\n')

        f.write('\n')

        next_page = response.css('div.paginator a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
