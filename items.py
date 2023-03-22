# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SunnyScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    collection = scrapy.Field()
    original_price = scrapy.Field()
    product_page_url = scrapy.Field()
    product_category = scrapy.Field()
    stock = scrapy.Field()
    brand = scrapy.Field()