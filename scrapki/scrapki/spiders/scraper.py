import scrapy, random, requests, os
from scrapy.exceptions import IgnoreRequest

def load_user_agents(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]
    
def load_proxies(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

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
        "nord-4"
    ]

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        user_agents_path = os.path.join(base_dir, '../resources/user-agents.txt')
        proxies_path = os.path.join(base_dir, '../resources/proxies.txt')
        self.user_agents = load_user_agents(user_agents_path)
        self.proxies = load_proxies(proxies_path)

    def start_requests(self):
        base_url = "https://www.kimovil.com/es/donde-comprar-"
        headers = {'User-Agent': random.choice(self.user_agents)}
        meta = {'proxy': random.choice(self.proxies)}
        for model in self.modelos:
            yield scrapy.Request(
                url=f"{base_url}{model}",
                callback=self.parse,
                headers=headers,
                meta=meta
            )

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
