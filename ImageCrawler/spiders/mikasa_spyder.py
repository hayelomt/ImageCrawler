import sys
import os
sys.path.append(os.path.join('.','ImageCrawler','utils'))
import imgDownloader

import scrapy

os.makedirs('data', exist_ok=True)
f = open(os.path.join('data', 'links'), 'a')

class MikassaSpider(scrapy.Spider):
    name = "mikassa"

    start_urls = [
        "https://wall.alphacoders.com/tags.php?tid=19575"
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(MikassaSpider, self).__init__(*args, **kwargs)
        self.imageDownloader = imgDownloader.ImageDownloader()

    def parse(self, response):
        links = [img_link for img_link in 
        response.css('div#container_page div.thumb-container div.boxgrid a::attr(href)').extract()]

        for link in links:
            print('URL:', response.url, ' Link:', link)
            f.write(response.url + '\t' + link + '\n')
            yield scrapy.Request('https://wall.alphacoders.com/' + link, callback=self.parse_image)

        f.write('\n')

        next_page = response.css('ul.pagination a#next_page::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    
    def parse_image(self, response):
        """
        parse image from followed link
        """

        link = response.css('div#page_container div.img-container-desktop a img::attr(src)').extract_first()
        self.imageDownloader.download(link)
        print('\tImage URL:', response.url, ' Link:', link)
        f.write('\tImage ' + response.url + '\t' + link + '\n')
