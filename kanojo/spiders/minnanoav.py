import scrapy


class MinnanoavSpider(scrapy.Spider):
    name = 'minnanoav'
    allowed_domains = ['minnano-av.com']
    start_urls = ['http://www.minnano-av.com/actress_list.php?page=%d' % i for i in range(1, 664)]

    def parse(self, response):
        model_links = response.xpath('//table[@class="tbllist actress"]//tr/td[1]/a/@href').extract()

        for model_link in model_links:
            model_link = 'http://www.minnano-av.com/' + model_link

            yield scrapy.Request(model_link, callback = self.parse_model_detail)

        pass

    def parse_model_detail(self, response):
        details_column = response.xpath('//section[@class="main-column details"]')

        name_jp = details_column.xpath('h1/text()').extract_first()
        name_en = details_column.xpath('h1/span/text()').extract_first().split(' / ')[1]

        # If the name_en has two words, it's likely in last name, first name order, so swap them
        if len(name_en.split(' ')) == 2:
            name_en = ' '.join(name_en.split(' ')[::-1]).title()

        birth_text = details_column.xpath('div[@class="act-profile"]//table//tr/td/span[contains(text(), "生年月日")]/following-sibling::p//text()').extract_first() # '1999年03月03日\r\n\t\t\t\t（現在 '
        
        birthdate = None
        if not (birth_text == '' or birth_text == "\r\n\t\t\t\t\t\t"):
            # Remove everything after day
            birth_text = birth_text.split('日')[0]
            # Replace year, month, day with dashes
            birthdate = birth_text.replace('年', '-').replace('月', '-').replace('日', '')

        blood_type = None
        height = None
        bust = None
        waist = None
        hip = None
        cup_size = None

        measurements_text = details_column.xpath('div[@class="act-profile"]//table//tr/td/span[contains(text(), "サイズ")]/following-sibling::p//text()').extract()
        if not measurements_text == []:
            measurements_text = ''.join(measurements_text) # 'T155 / B100(Gカップ) / W60 / H91 / S'

            # Get the height
            height = measurements_text.split(' / ')[0].replace('T', '')
            if height == '':
                height = None
            else:
                height = int(height)

            # Get the bust
            bust = measurements_text.split(' / ')[1].replace('B', '').split('(')[0]
            if bust == '':
                bust = None
            else:
                bust = int(bust)

            # Get the cup size
            try:
                cup_size = measurements_text.split(' / ')[1].replace('B', '').split('(')[1].replace(')', '').replace('カップ', '')
                if cup_size == '':
                    cup_size = None
            except:
                cup_size = None

            # Get the waist
            waist = measurements_text.split(' / ')[2].replace('W', '')
            if waist == '':
                waist = None
            else:
                waist = int(waist)

            # Get the hip
            hip = measurements_text.split(' / ')[3].replace('H', '')
            if hip == '':
                hip = None
            else:
                hip = int(hip)
            
        blood_type_text = details_column.xpath('div[@class="act-profile"]//table//tr/td/span[contains(text(), "血液型")]/following-sibling::p//text()').extract_first()
        if not (blood_type_text == '' or blood_type_text == None):
            blood_type = blood_type_text.replace('型', '')

        yield {
            'name_jp': name_jp,
            'name_en': name_en,
            'birthdate': birthdate,
            'blood_type': blood_type,
            'height': height,
            'bust': bust,
            'waist': waist,
            'hip': hip,
            'cup_size': cup_size,
            'country': None,
        }
