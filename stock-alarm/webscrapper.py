#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen

class WebScrapper():
    def __init__(self):
        pass

    # url: Direccion de la pagina web
    # return: String en formato html de la pagina 
    def make_soup(self, url):
        # Abro la direccion con urlopen y con read() leo hasta EOF
        html = urlopen(url).read()
        return BeautifulSoup(html, "lxml")

    # url: Direccion de la pagina web
    # return: Direccion desde raiz de cada tema del foro
    def get_stock_price(self, stk_market, specie):
        url = 'https://www.google.com/finance?q=' + stk_market + '%20' + specie
        # Genero el archivo en formato html de la direccion en cuestion
        soup = self.make_soup(url)
        # Busco en el archivo todas las etiquetas 'a' que tengan un atributo 
        # 'class' con valor 'topictitle'
        topics = soup.findAll('meta', {'itemprop' : 'price'})
        return float(topics[0]['content'])