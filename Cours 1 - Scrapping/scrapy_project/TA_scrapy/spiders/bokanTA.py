# Logging packages
import logging
import logzero
from logzero import logger

# Scrapy packages
import scrapy
from TA_scrapy.items import ReviewRestoItem     # you can use it if you want but it is not mandatory
from TA_scrapy.spiders import get_info          # package where you can write your own functions


class bokanTA(scrapy.Spider):
    name = "bokanTA"

    def __init__(self, *args, **kwargs): 
        super(bokanTA, self).__init__(*args, **kwargs)

        # Set logging level
        logzero.loglevel(logging.WARNING)

        # To track the evolution of scrapping
        self.main_nb = 0
        self.resto_nb = 0
        self.resto_pg_nb = 0
        self.review_nb = 0
        

    def start_requests(self):
        """ Give the urls to follow to scrapy
        - function automatically called when using "scrapy crawl my_spider"
        """

        # Basic restaurant page on TripAdvisor GreaterLondon
        urls = ['https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d12156905-Reviews-Bokan_37_Restaurant-London_England.html',
                'https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d17415315-Reviews-BOKAN_38_Bar_39_Rooftop-London_England.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_resto)


    def parse_resto(self, response):
        """SECOND PARSING : Given a restaurant, get each review url and get to parse it
            - Usually there are 10 comments per page
        """
        logger.warn(' > PARSING NEW REVIEW PAGE ({})'.format(self.resto_pg_nb))
        self.resto_pg_nb += 1

        # Get the list of reviews on the restaurant page

        ########################
        #### YOUR CODE HERE ####
        ########################
        
        urls_review = get_info.get_urls_review_in_resto(response)
        
        ########################
        ########################

        # For each review open the link and parse it into the parse_review method
        for url_review in urls_review:
             yield response.follow(url=url_review, callback=self.parse_review)

        
        ########################
        #### YOUR CODE HERE ####
        ########################
        
        next_page, next_page_number = get_info.get_urls_next_list_of_reviews(response)
        
        # Follow the page if we decide to
        if get_info.go_to_next_page(next_page, next_page_number, max_page=500):
            yield response.follow(next_page, callback=self.parse_resto)
            
        ########################
        ########################


    def parse_review(self, response):
        """FINAL PARSING : Open a specific page with review and client opinion
            - Read these data and store them
            - Get all the data you can find and that you believe interesting
        """

        # Count the number of review scrapped
        self.review_nb += 1

        ########################
        #### YOUR CODE HERE ####
        ########################

        # You can store the scrapped data into a dictionnary or create an Item in items.py (cf XActuItem and scrapy documentation)
        review_item = ReviewRestoItem()
        
        #Get restaurant
        css_locator = 'a.HEADING ::text'
        review_item['resto'] = response.css(css_locator).extract_first().strip()
        
        # Get date
        css_locator = 'span.ratingDate.relativeDate ::attr(title)'
        review_item['review_date'] = response.css(css_locator).extract_first().strip()
        
        #Get rating
        css_locator = 'div.rating > span ::attr(alt)'
        review_item['review_rating'] = response.css(css_locator).extract_first().strip()[0]
        
        #Get title
        css_locator = 'span.noQuotes ::text'
        review_item['review_title'] = response.css(css_locator).extract_first().strip()

        # Get content
        css_locator = 'p.partial_entry ::text'
        review_item['review_text'] = response.css(css_locator).extract_first().strip()  
        
        # Get link of full article
        review_item['review_link'] = response.url.strip()
        
        ########################
        ########################

        yield review_item


