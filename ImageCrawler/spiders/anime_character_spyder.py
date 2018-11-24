import sys
sys.path.append('./ImageCrawler/utils')
import imgDownloader
# from dir_utils import getStartingPage

import scrapy
import os

os.makedirs('data', exist_ok=True)
f = open('data/links', 'a')
# URL = getStartingPage('https://www.anime-planet.com/characters/all')

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

        next_page = response.css('div.pagination ul.nav li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
