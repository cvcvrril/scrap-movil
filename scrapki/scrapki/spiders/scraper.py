import scrapy

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["kimovil.com"]
    start_urls = []

    modelos = [
        "samsung-galaxy-s23",
        "samsung-galaxy-s24",
        "realme-gt-6",
        "realme-gt-6t",
        "pixel-8",
        "pixel-9",
    ]

    def start_requests(self):
        base_url = "https://www.kimovil.com/es/donde-comprar-"
        for model in self.modelos:
            yield scrapy.Request(url=f"{base_url}{model}", callback=self.parse)

    def parse(self, response):

        phone_name = response.css("h1.title-model::text").get()  
        offers = response.css("div.store-offer") 

        for offer in offers:
            yield {
                "phone": phone_name,
                "store": offer.css("div.store-name::text").get(),
                "price": offer.css("div.price span::text").get(),
                "link": offer.css("a.store-link::attr(href)").get(),
            }

        if response.status == 403:
            self.logger.error("Acceso prohibido: 403")
            return
