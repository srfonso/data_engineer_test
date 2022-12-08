# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Exercice3Item(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    media = scrapy.Field()
    height_cm = scrapy.Field()
    width_cm = scrapy.Field()
    price_gbp = scrapy.Field()
