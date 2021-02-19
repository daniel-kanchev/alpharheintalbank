import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from alpharheintalbank.items import Article


class AlphaSpider(scrapy.Spider):
    name = 'alpha'
    start_urls = ['https://www.alpharheintalbank.ch/news/']

    def parse(self, response):

        articles = response.xpath('//div[@class="news-list-item"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()
            title = article.xpath('.//a/text()').get()
            if title:
                title = title.strip()
            link = article.xpath('.//a/@href').get()
            date = article.xpath('//div[@class="news-list-item"]//time/text()').get()
            if date:
                date = datetime.strptime(date.strip(), '%d.%m.%Y')
                date = date.strftime('%Y/%m/%d')

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('link', response.urljoin(link))

            yield item.load_item()
