import scrapy


class JavlibrarySpider(scrapy.Spider):
    name = 'javlibrary'
    allowed_domains = ['javlibrary.com']
    start_urls = ['https://www.javlibrary.com/ja/vl_genre.php?g=%s' % c for c in ['amjq', 'da', 'azba', 'am4q', 'ia', 'a46q', 'araa', 'aaxa', 'aqpq', 'a46a', 'arna', 'aqrq', 'a4ra', 'aqla', 'aqkq', 'a47q', 'aqua', 'aa4a', 'j4', 'a5mq', 'azga', 'ka', 'aqya', 'aa3a', 'ayiq', 'di', 'amoa', 'a4hq', 'aqda', 'km', 'aq5q', 'arkq', 'ja', 'ma', 'a5lq', 'ku', 'im', 'a4nq', 'pi', 'arjq', 'ne', 'pe', 'cy', 'a4jq', 'arfq', 'ay', 'amoq', 'a4qa', 'aa3q', 'aa4q', 'a4tq', 'a4ha', 'abpq', 'a4ua', 'amca', 'a4ga', 'arnq', 'area', 'ju', 'azcq', 'aqeq', 'me', 'arlq', 'aqmq', 'ni', 'areq', 'azca', 'o4', 'arja', 'aqea', 'a4lq', 'am3a', 'de', 'i4', 'aq6q', 'a5dq', 'pu', 'aqpa', 'mq', 'a5cq', 'aqaa', 'arcq', 'p4', 'mu', 'aqlq', 'aqaq', 'arfa', 'arca', 'jq', 'aqva', 'aqca', 'a5nq', 'du', 'aqna', 'iy', 'armq', 'arpa', 'nm', 'dm', 'dy', 'aqta', 'aqra', 'aqvq', 'ca', 'a4wa', 'aqsa', 'a4pa', 'aqwa', 'aqbq', 'aqcq', 'aqjq', 'aqha', 'aq2a', 'ai', 'a4wq', 'aqqq', 'a4iq', 'a4da', 'a4oq', 'a4kq', 'ny', 'a4ta', 'aqga', 'a4ca', 'cq', 'ci', 'a4za', 'ajcq', 'aqja', 'kq', 'oy', 'aqqa', 'a5na', 'pm', 'a5aa', 'a4', 'ie', 'a4aa', 'k4', 'na', 'aq2q', 'arba', 'aqiq', 'ii', 'iq', 'nq', 'aqyq', 'pq', 'd4', 'arga', 'aayq', 'aaza', 'ly', 'argq', 'aqsq', 'a5ga', 'aq3q', 'aqoa', 'bm', 'aa7q', 'aqia', 'aqtq', 'aa', 'a4ya', 'dq', 'ke', 'am', 'bu', 'py', 'cm', 'aq6a', 'mm', 'ky', 'ce', 'oi', 'aqoq', 'aqza', 'oa', 'aq5a', 'mi', 'nu', 'arma', 'ardq', 'bq', 'aa7a', 'c4', 'l4', 'aq7q', 'aqma', 'a4xa', 'ou', 'pa', 'arbq', 'b4', 'aq7a', 'li', 'ampa', 'a4cq', 'arpq', 'aqwq', 'aqxa', 'jm', 'iu', 'le', 'araq', 'cu', 'lm', 'aqnq', 'aqhq', 'aqdq', 'la', 'bi', 'ki', 'aq3a', 'ae', 'je', 'ariq', 'aqba', 'ba', 'n4', 'a4ia', 'ayda', 'lu', 'a5ca', 'be', 'a4la', 'a4eq', 'arka', 'arhq', 'oq', 'oe', 'a5aq', 'aqzq', 'aqfa', 'azaa', 'ayla', 'my', 'ayma', 'arda', 'aroa', 'a5ba', 'ayca', 'ayjq', 'a5ka', 'a4oa', 'azgq', 'a5ma', 'ayoq', 'a5gq', 'a4gq', 'a4ja', 'a5bq', 'a4ka', 'a5pq', 'a4sq', 'a4dq', 'azbq', 'aazq', 'aqka', 'a5fq', 'a4pq', 'm4', 'a4vq', 'ayia', 'aypa', 'a5da', 'a4bq', 'ayna', 'a4ma', 'arha', 'lq', 'a4mq', 'jy', 'a4rq', 'a4qq', 'aquq', 'by', 'aaua', 'aqgq', 'a5fa', 'a4zq', 'a4aq', 'aycq']]

    def parse(self, response):
        for sel in response.xpath('//div[@class="video"]/a/@href').extract():
            url = sel.replace('./', 'https://www.javlibrary.com/ja/')
            yield scrapy.Request(url, callback = self.parse_movie_detail)

        next_page = response.xpath('//a[@class="page next"]/@href').extract_first()
        if next_page:
            next_page = 'https://www.javlibrary.com' + next_page
            yield scrapy.Request(next_page, callback = self.parse)

    def parse_movie_detail(self, response):
        title_element = response.xpath('//h3/a/text()').extract_first()
        [product_code, title_jp] = title_element.split(' ', 1)
        
        try:
            poster = response.xpath('//img[@id="video_jacket_img"]/@src').extract_first()
            # Add http if not exist
            if not poster.startswith('http'):
                poster = 'http:' + poster
        except:
            poster = None
        
        try:
            release_date = response.xpath('//td[contains(text(), "発売日:")]/following-sibling::td/text()').extract_first()
        except:
            release_date = None

        try:
            runtime = int(response.xpath('//td[contains(text(), "収録時間:")]/following-sibling::td/span[@class="text"]/text()').extract_first())
        except:
            runtime = None

        try:
            studio = response.xpath('//td[contains(text(), "メーカー:")]/following-sibling::td/a/text()').extract_first()
        except:
            studio = None

        try:
            label = response.xpath('//td[contains(text(), "レーベル:")]/following-sibling::td/a/text()').extract_first()
        except:
            label = None

        try:
            genres = response.xpath('//td[contains(text(), "ジャンル:")]/following-sibling::td/span/a/text()').extract()
        except:
            genres = None

        try:
            models = response.xpath('//td[contains(text(), "出演者:")]/following-sibling::td//a/text()').extract()
        except:
            models = None

        yield {
            'product_code': product_code,
            'release_date': release_date,
            'title_jp': title_jp,
            'title_en': None,
            'studio': studio,
            'label': label,
            'runtime': runtime,
            'series': None,
            'models': models,
            'genres': genres,
            'image_urls': [poster] if poster else [],
        }
