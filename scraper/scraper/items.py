# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field



class booksItem(Item):
    title=Field()
    price=Field()
    availability=Field()
    rating=Field()
    
   