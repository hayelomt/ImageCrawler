import sys
sys.path.append('./ImageCrawler/utils')
import imgDownloader

import scrapy
import os

os.makedirs('data', exist_ok=True)
f = open('data/links', 'a')

class AnimeListSpider(scrapy.Spider):
    name = "animelist"

    start_urls = [
        "https://myanimelist.net/character.php"
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(AnimeListSpider, self).__init__(*args, **kwargs)
        self.imageDownloader = imgDownloader.ImageDownloader()

    def parse(self, response):
        links = [img_link for img_link in 
        response.css('table.characters-favorites-ranking-table tr.ranking-list td.people div.information a::attr(href)').extract()]

        for link in links:
            print('URL:', response.url, ' Link:', link)
            f.write(response.url + '\t' + link + '\n')
            yield scrapy.Request(link, callback=self.parse_image)

        f.write('\n')

        next_page = response.css('div.pagination a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_image(self, response):
        """
        parse image from followed link
        """

        link = response.css('div#content div a img::attr(src)').extract_first()
        self.imageDownloader.download(link)
        print('\tImage URL:', response.url, ' Link:', link)
        f.write('\tImage ' + response.url + '\t' + link + '\n')

