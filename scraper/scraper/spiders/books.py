import scrapy
from .categories import get_categories

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    #response.css('ul.nav.nav-list li ul li a::attr(href)').getall()
    categorie=get_categories()
    path='https://books.toscrape.com/'
    ful_path=path+categorie
    
    
    
    
    def start_requests(self):
        yield scrapy.Request(url=self.ful_path, callback=self.parse)

    def parse(self, response):
        products = response.css("article.product_pod")
        
        for product in products:
            availability_texts = product.css("p.instock.availability::text").getall()
            availability = ''.join(availability_texts).strip()

            rating_classes = product.css("p.star-rating::attr(class)").get()
            rating = rating_classes.replace("star-rating", "").strip() if rating_classes else None

            item = {
                "title": product.css("h3 a::attr(title)").get(),
                "price": product.css("p.price_color::text").get(),
                "availability": availability,
                "rating": rating,
            }
            yield item

        # Pagination logic
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            if "catalogue" in response.url:
                full_path = response.urljoin(next_page)
            else:
                full_path = response.urljoin( next_page)
            yield scrapy.Request(url=full_path, callback=self.parse)
