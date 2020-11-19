from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from crawler.items import CrawlerItem
from scrapy import Selector
import os
import urllib
import urllib.request
from lxml.html import fromstring

filename = 'lyrics.txt'

class MetroLyricsSpider(CrawlSpider):
    name = 'lyrics'
    
    custom_settings = {
        'LOG_STDOUT': True,
        'LOG_LEVEL': 'ERROR',
    }
    
    allowed_domains = ['metrolyrics.com']
    start_urls = ['http://www.metrolyrics.com/']
    rules = (Rule(LinkExtractor(),callback="save_lyrics",follow=True),)
    if not os.path.isfile(filename):
        open(filename,'w').close()


    def parse_items(self,response):
        hxs = Selector(response)
        titles = hxs.xpath('//p')
        items = []
        for title in titles:
            item = CrawlpageItem()
            item['title'] = titles.xpath('a/text()').extract()
            item['link'] = titles.xpath('a/@href').extract()
            items.append(item)
        
    def save_lyrics(self,response):
        url = response.url
        if not 'printlyric' in url:
            return
        body = fromstring(urllib.request.urlopen(url).read())
        verses = body.xpath("//*[contains(@class, 'verse')]")
        verses = [i.text_content() for i in verses]
        header = body.xpath("//*[contains(@class, 'grid_12 clearfix')]")[0].text_content().strip()
        song = header.split('by')[0].strip()
        artist = header.split('by')[1].strip()
        song_text = '\n\n'.join(verses)
        try:
            with open(filename,'a') as f:
                f.write('#beginentry\n'+url+'\n'+artist+'\n'+song+'\n\n'+song_text+'\n\n')
            print('---- Saved lyrics %s by %s ----' % (song,artist))
        except Exception as e:
            print("Unexpected error:", str(e))



        
