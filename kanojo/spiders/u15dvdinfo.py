from scrapy.spiders import SitemapSpider
import pathlib

class MgstageSpider(SitemapSpider):
    name = 'u15dvdinfo'
    allowed_domains = ['u15dvdinfo.com']
    sitemap_urls = [
        pathlib.Path('wp-sitemap-posts-products-1.xml').absolute().as_uri(),
        pathlib.Path('wp-sitemap-posts-products-2.xml').absolute().as_uri(),
        pathlib.Path('wp-sitemap-posts-products-3.xml').absolute().as_uri(),
        pathlib.Path('wp-sitemap-posts-products-4.xml').absolute().as_uri()
    ]
    sitemap_rules = [
        ('/products/', 'parse_product'),
    ]

    def parse_product(self, response):
        # Check class of title to see if it's a DVD or a Blu-ray
        if not response.css('h1::attr(class)').get() in ['dvd', 'blu-ray', 'dvd-box', 'bd-box']:
            return

        title = response.xpath('//th[contains(text(), "商品名")]/following-sibling::td/text()').get()

        # Get the product code
        product_code = response.xpath('//th[contains(text(), "品番")]/following-sibling::td/text()').get()

        # Get the release date
        release_date = response.xpath('//th[contains(text(), "発売日")]/following-sibling::td/text()').get()
        if release_date:
            release_date = release_date.replace('年', '-').replace('月', '-').replace('日', '')

        # Get the studio
        studio = response.xpath('//th[contains(text(), "メーカー")]/following-sibling::td/text()').get()

        models = []

        # Get the table with class idol_info
        model_table = response.xpath('//table[@class="idol_info"]')
        # Check how many columns there are
        num_cols = len(model_table.xpath('.//tr[1]/th'))

        # If there is only one column
        if num_cols == 1:
            # Iterate through the rows, skipping the header row
            for index, row in enumerate(model_table.xpath('.//tr')):
                if index == 0:
                    continue

                # If the row has a th element, it's a header row
                if row.xpath('.//th'):
                    continue

                # Get the model name
                model = row.xpath('.//td/a/text()').get()
                if model:
                    models.append(model)
        # If there are 3 columns
        elif num_cols == 3:
            # Iterate through the rows, skipping the header row
            for index, row in enumerate(model_table.xpath('.//tr')):
                if index == 0:
                    continue

                # Get the model name
                model = row.xpath('.//td[1]/a/text()').get()
                if model:
                    models.append(model)

        # Get the cover image, it's the image inside the div with class p_image
        cover_image = response.xpath('//div[@class="p_image"]//img/@src').get()

        yield {
            'product_code': product_code,
            'release_date': release_date,
            'title_jp': title,
            'title_en': None,
            'studio': studio,
            'label': None,
            'runtime': None,
            'series': None,
            'models': models,
            'genres': None,
            'image_urls': [cover_image] if cover_image else [],
        }
