import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DmmSpider(CrawlSpider):
    name = 'dmm'
    allowed_domains = ['dmm.co.jp']
    start_urls = ['https://www.dmm.co.jp/top/', 'https://www.dmm.co.jp/digital/videoa/-/list/=/device=vr/sort=date/']

    rules = (
        Rule(LinkExtractor(allow=r'/list/'), follow=True),
        Rule(LinkExtractor(allow=r'/mono/dvd/-/detail/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/digital/videoa/-/detail/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/digital/videoa/'), follow=True),
        Rule(LinkExtractor(allow=r'/digital/videovr/'), follow=True),
        Rule(LinkExtractor(allow=r'/digital/videoc/'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
