#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen

class WebScrapper():
    """
    Class to scrap Google Finance web page searching for stock prices.

    WebScrapper class scrap the page using BeautifulSoup4. It reads tags
    to find stock's price.
    """
    def __init__(self):
        pass

    def _make_soup(self, url):
        """
        Return html page parsed with lxml parser as a BeautifulSoup object.

        Args:
            url (str): URL of stock in Google Finance.

        Returns:
            (BeautifulSoup object): Nested data structure of the web page.

        """
        html = urlopen(url).read()          # Open URL and read until EOF
        return BeautifulSoup(html, "lxml")

    def get_stock_price(self, stk_market, specie):
        """
        Extract and return stock's price of a given specie in a given market.

        Args:
            stk_market (str): Market exchange where found the given specie.
            specie (str): Specie for get stock price.

        Returns:
            (float): Stock price for given specie.
            
        """
        url = """
              https://www.google.com/finance?q=%s%20%s
              """ % (stk_market, specie)
        soup = self._make_soup(url)
        topics = soup.findAll('meta', {'itemprop' : 'price'})
        return float(topics[0]['content'])