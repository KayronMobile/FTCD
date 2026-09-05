import scrapy


class NewsItem(scrapy.Item):
    titulo = scrapy.Field()
    ano = scrapy.Field()
    url = scrapy.Field()
