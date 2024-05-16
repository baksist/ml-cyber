import scrapy
from serdyukov_bookscrape.items import Book

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = []

    npages = 50

    for i in range (1, npages+1):
        start_urls.append(f"http://books.toscrape.com/catalogue/page-{i}.html")

    rating_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def parse(self, response):
        books = response.css('article')

        for book in books:
            item = Book()

            item['title'] = book.xpath('h3/a').attrib['title']
            item['rating'] = self.rating_dict[book.css('p.star-rating').attrib['class'].split()[1]]
            item['price'] = book.xpath("div[@class='product_price']/p[@class='price_color']/text()").get()
            item['stock'] = book.xpath("div[@class='product_price']/p[@class='instock availability']/i/@class").get() == 'icon-ok'
            
            yield item
