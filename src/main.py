import scrapy

class BlogSpider(scrapy.Spider):
    name = 'kimovil'
    allowed_domains = ["www.kimovil.com"]
    start_urls = ['https://www.kimovil.com/es/']
    