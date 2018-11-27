import sys
import os
sys.path.append(os.path.join('.','ImageCrawler','utils'))
import imgDownloader
from dir_utils import getStartingPage

import scrapy

os.makedirs('data', exist_ok=True)
f = open(os.path.join('data', 'links'), 'a')

class AnimeCharacterSpider(scrapy.Spider):
    name = "animecharacter"

    start_urls = [
        "https://www.anime-planet.com/characters/all"
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(AnimeCharacterSpider, self).__init__(*args, **kwargs)
        self.imageDownloader = imgDownloader.ImageDownloader()

    def parse(self, response):
        links = ['https://www.anime-planet.com' + img_src for img_src in 
        response.css('table.pure-table tbody tr td.tableAvatar a img::attr(src)').extract()]

        for link in links:
            self.imageDownloader.download(link)
            print('URL:', response.url, ' Link:', link)
            f.write(response.url + '\t' + link + '\n')

        f.write('\n')

        next_page = response.css('div.pagination ul.nav li.next a.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
