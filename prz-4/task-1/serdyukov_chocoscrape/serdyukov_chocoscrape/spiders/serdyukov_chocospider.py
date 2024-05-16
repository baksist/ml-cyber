import scrapy
from serdyukov_chocoscrape.items import SerdyukovChocoscrapeItem
from serdyukov_chocoscrape.itemloaders import ChocolateProductLoader

class SerdyukovChocospiderSpider(scrapy.Spider):
    name = "serdyukov_chocospider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css('product-item')

        for product in products:
            loader = ChocolateProductLoader(item=SerdyukovChocoscrapeItem(), selector=product)
            loader.add_css('name', "a.product-item-meta__title::text")
            loader.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            loader.add_css('url', 'div.product-item-meta a::attr(href)')

            yield loader.load_item()
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback=self.parse)
        
    