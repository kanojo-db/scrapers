import scrapy

class ActressSpider(scrapy.Spider):
    name = "dmm_actress"
    allowed_domains = ["dmm.co.jp"]
    start_urls = ["https://actress.dmm.co.jp/-/list/=/keyword=%s/" % c for c in ['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko', 'sa', 'si', 'su', 'se', 'so', 'ta', 'ti', 'tu', 'te', 'to', 'na', 'ni', 'nu', 'ne', 'no', 'ha', 'hi', 'hu', 'he', 'ho', 'ma', 'mi', 'mu', 'me', 'mo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro', 'wa']]

    def parse(self, response):
        for sel in response.xpath('//a[@class="p-list-actress__link"]/@href'):
            url = response.urljoin(sel.extract())
            yield scrapy.Request(url, callback = self.parse_actress_detail)

        next_page = response.xpath('//div[@class="p-box-pagenationArea"]/ul/li[@class="p-box-pagenation__btn p-box-pagenation__btn--arrow"][@style="display:;"]/a/@href')
        if next_page:
            next_page = response.urljoin(next_page.extract())
            yield scrapy.Request(next_page, callback = self.parse)


    def parse_actress_detail(self, response):
        name_jp = response.xpath('//h1[@class="c-tx-actressName"]/text()').extract_first().replace('\n', '').strip()
        if name_jp == '---': name_jp = None

        birthdate = response.xpath('//dl[@class="p-list-profile"]/dt[contains(text(), "生年月日")]/following-sibling::dd/text()').get().replace('\n', '').strip().replace('年', '-').replace('月', '-').replace('日', '')
        if birthdate == '---': birthdate = None

        bloodtype = response.xpath('//dl[@class="p-list-profile"]/dt[contains(text(), "血液型")]/following-sibling::dd/text()').get().replace('\n', '').strip()
        if bloodtype == '---': bloodtype = None

        dimensions = response.xpath('//dl[@class="p-list-profile"]/dt[contains(text(), "サイズ")]/following-sibling::dd/text()').get().replace('\n', '').strip()

        height = None
        bust = None
        waist = None
        hip = None
        cup_size = None

        if dimensions == '---': dimensions = None
        else:
            dimensions = dimensions.split(' ')
            # Iterate over dimensions
            for i, dim in enumerate(dimensions):
                # Remove cm from dimension
                dim = dim.replace('cm', '')

                # If it starts with T, it's the height
                if dim.startswith('T'):
                    height = int(dim.replace('T', ''))

                # If it starts with B, it's the bust
                if dim.startswith('B'):
                    # Bust sizes sometimes have the cup size in parentheses
                    if '(' in dim:
                        cup_size = dim[dim.find('(')+1:dim.find(')')]
                        bust = int(dim.replace('B', '').replace('(', '').replace(')', '').replace(cup_size, '').replace('カップ', ''))
                    else:
                        bust = int(dim.replace('B', ''))

                # If it starts with W, it's the waist
                if dim.startswith('W'):
                    waist = int(dim.replace('W', ''))

                # If it starts with H, it's the hip
                if dim.startswith('H'):
                    hip = int(dim.replace('H', ''))

        yield {
            'name_jp': name_jp,
            'name_en': None,
            'birthdate': birthdate,
            'blood_type': bloodtype,
            'height': height,
            'bust': bust,
            'waist': waist,
            'hip': hip,
            'cup_size': cup_size,
            'country': 'Japan',
        }

        """ item = Actress()
        url = resposne.url
        name = sel.xpath('tr[3]/td/table/tr/td[1]/img/@alt').extract()
        item['name'] = name[0].encode('utf-8')
        item['name_en'] = sel.xpath('tr[3]/td/table/tr/td[1]/img/@src').extract()
        birth = sel.xpath('tr[3]/td/table/tr/td[2]/table/tr[1]/td[2]/text()').extract()
        item['birth'] = birth[0].encode('utf-8')
        starsign = sel.xpath('tr[3]/td/table/tr/td[2]/table/tr[2]/td[2]/text()').extract()
        item['starsign'] = starsign[0].encode('utf-8')
        bloodtype = sel.xpath('tr[3]/td/table/tr/td[2]/table/tr[3]/td[2]/text()').extract()
        item['bloodtype'] = bloodtype[0].encode('utf-8')
        boobs = sel.xpath('tr[3]/td/table/tr/td[2]/table/tr[4]/td[2]/text()').extract()
        item['boobs'] = boobs[0].encode('utf-8')
        home = sel.xpath('tr[3]/td/table/tr/td[2]/table/tr[5]/td[2]/text()').extract()
        item['home'] = home[0].encode('utf-8')
        hobby = sel.xpath('tr[3]/td/table/tr/td[2]/table/tr[6]/td[2]/text()').extract()
        item['hobby'] = hobby[0].encode('utf-8')
        item['image_urls'] = sel.xpath('tr[3]/td/table/tr/td[1]/img/@src').extract()
        request = scrapy.Request(url, callback=self.parse_actress_detail2, meta={'item':item})
        yield request """

