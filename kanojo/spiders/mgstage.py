from scrapy.spiders import SitemapSpider
from string import digits

class MgstageSpider(SitemapSpider):
    name = 'mgstage'
    allowed_domains = ['mgstage.com']
    sitemap_urls = ['http://www.mgstage.com/sitemap.xml']
    sitemap_rules = [
        ('/product/product_detail/', 'parse_product'),
    ]
    sitemap_follow = ['/product_detail']

    def parse_product(self, response):
        has_table = response.xpath('//div[@class="detail_data"]/table[2]').get()

        table_index = 1
        if has_table is not None:
            table_index = 2

        models = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "出演：")]/following-sibling::td/a/text()').getall()
        # Clean actress names
        models = [model.replace('\n', '').strip() for model in models]

        genres =  response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "ジャンル")]/following-sibling::td/a/text()').getall()
        # Clean genres
        genres = [genre.replace('\n', '').strip() for genre in genres]

        poster = response.xpath('//div[@class="detail_photo"]/h2/img/@src').get()
        if poster:
            poster = poster.replace('_o1_', '_e_')

        product_code = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "品番")]/following-sibling::td/text()').get()
        # If product code doesn't start with 3DSVR, strip leading digits
        if product_code and not product_code.startswith('3DSVR'):
            product_code = product_code.replace('\n', '').strip().lstrip(digits)

        release_date = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "配信開始日")]/following-sibling::td/text()').get()
        if release_date:
            release_date = release_date.replace('\n', '').strip().replace('/', '-')

        studio = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "メーカー")]/following-sibling::td/a/text()').get()
        if studio:
            studio = studio.replace('\n', '').strip()

        label = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "レーベル")]/following-sibling::td/a/text()').get()
        if label:
            label = label.replace('\n', '').strip()

        runtime = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "収録時間")]/following-sibling::td/text()').get()
        if runtime:
            runtime = runtime.replace('\n', '').replace('min', '').strip()

        series = response.xpath(f'//div[@class="detail_data"]/table[{table_index}]/tr/th[contains(text(), "シリーズ")]/following-sibling::td/a/text()').get()
        if series:
            series = series.replace('\n', '').strip()

        yield {
            'product_code': product_code,
            'release_date': release_date,
            'title_jp': response.xpath('//div[@class="common_detail_cover"]/h1/text()').get().replace('\n', '').strip(),
            'title_en': '',
            'studio': studio,
            'label': label,
            'runtime': runtime,
            'series': series,
            'models': models,
            'genres': genres,
            'image_urls': [poster] if poster else [],
        }
