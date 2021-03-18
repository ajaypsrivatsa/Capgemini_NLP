# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class XActuItem(scrapy.Item):
    titre_article = scrapy.Field()
    lien_article = scrapy.Field()
    date_article = scrapy.Field()
    content = scrapy.Field()
    related_subject = scrapy.Field()
    related_subject_links = scrapy.Field()



class ReviewRestoItem(scrapy.Item):
        
    resto = scrapy.Field()
    review_rating = scrapy.Field()
    review_title = scrapy.Field()
    review_date = scrapy.Field()
    review_text = scrapy.Field()
    review_link = scrapy.Field()
    
    pass