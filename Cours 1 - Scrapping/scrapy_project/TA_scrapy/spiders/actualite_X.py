import scrapy
import logging
import logzero
from logzero import logger

from TA_scrapy.spiders import get_info
from TA_scrapy.items import XActuItem


class actuXSpider(scrapy.Spider):
    name = "actuX_init"

    def __init__(self, *args, **kwargs):
        super(actuXSpider, self).__init__(*args, **kwargs)

        # Set logging level
        logzero.loglevel(logging.DEBUG)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls = [
                'https://www.tripadvisor.co.uk/Restaurant_Review-g187147-d9806534-Reviews-ASPIC-Paris_Ile_de_France.html'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        # To track the evolution of scrapping
        self.main_nb = 0
        self.article_nb = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """MAIN PARSING : Start from a classical restaurant page
            - Usually there are 30 restaurants per page
        """
        logger.warn('> PARSING NEW MAIN PAGE OF ARTICLES ({})'.format(self.main_nb))

        self.main_nb += 1

        # Get the list of the articles
        xpath = '//div[@class="quote"]'
        my_urls = response.xpath(xpath).css('::attr(href)').extract()
        for urls in my_urls:
            yield response.follow(url=urls, callback=self.parse_article)

        # Deal with next page
        css_locator = '//a[@class ="nav next ui_button primary"]/@href'
        next_page = response.css(css_locator).extract_first()
        try:
            next_page_number = next_page.split('=')[-1]
            next_page_number = int(next_page_number)
        except:
            next_page_number = self.main_nb + 1

        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        """REAL PARSING : Open a specific page with restaurant description
            - Read these data and store them
        """
        # Ex : https://www.tripadvisor.co.uk/Restaurant_Review-g504169-d7221903-Reviews-Mezzet_Dar-East_Molesey_Molesey_Surrey_England.html
        self.article_nb += 1

        # Intitiate storing object
        actu_item = XActuItem()

        xpath = '//span[@class="noQuotes"]//text()'
        actu_item['Review_Title'] = response.xpath(xpath).extract_first()

        actu_item['Review_Link'] = response.url

        xpath = '//span[@class="ratingDate relativeDate"]//p//text()'
        actu_item['Review_Date'] = response.xpath(xpath).extract_first()

        xpath = '//div[@class="entry"]//p//text()'
        actu_item['Content'] = response.xpath(xpath).extract()[:-7]
        yield actu_item
