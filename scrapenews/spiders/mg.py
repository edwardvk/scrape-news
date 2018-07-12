# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class mgSpider(SitemapSpider):
    name = 'mg'
    allowed_domains = ['mg.co.za']

    sitemap_urls = ['https://mg.co.za/robots.txt']
    # Could not find a way to limit it to South African interest only.
    sitemap_follow = [
        '/article/',
        #'^http(s?):\/\/mg\.co\.za\/(?!(tag|section\/news-world)).*$',
    ]

    publication_name = 'Mail & Guardian'

    def parse(self, response):
        publication_date_str = response.xpath('//meta[@name="publicationdate"]/@content').extract_first()
        publication_date = datetime.strptime(publication_date_str, '%d/%m/%Y')
        publication_date = SAST.localize(publication_date)

        item = ScrapenewsItem()
        item['body_html'] = " ".join(response.css("#body_content p").xpath("text()").extract())
        item['title'] = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        item['byline'] = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        item['published_at'] = publication_date.isoformat()
        item['retrieved_at'] = datetime.utcnow().isoformat()
        item['url'] = response.url
        item['file_name'] = response.url.split('/')[-1]
        item['spider_name'] = self.name
        item['publication_name'] = self.publication_name

        yield item
