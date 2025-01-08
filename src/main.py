import scrapy

class BlogSpider(scrapy.Spider):
    name = 'kimovil'
    allowed_domains = ["www.kimovil.com"]
    start_urls = ['https://www.kimovil.com/es/']


    def parse(self, response):
        # get all HTML product elements
        products = response.css(".product")
        # iterate over the list of products
        for product in products:
            # get the two price text nodes (currency + cost) and
            # contatenate them
            price_text_elements = product.css(".price *::text").getall()
            price = "".join(price_text_elements)
           
           # return a generator for the scraped item
            yield {
                "Url": product.css("a").attrib["href"],
                "Image": product.css("img").attrib["src"],
                "Name": product.css("h2::text").get(),  
                "Price": price,
            }
    