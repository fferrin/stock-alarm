#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ConfigParser
import helpers as h
from webscrapper import WebScrapper

####################################################

# Main
parser = ConfigParser.ConfigParser()
scrapper = WebScrapper()
file = 'stock-alarm.config'
parser.read(file)
cfgValues = h.get_config_values(parser)

# # PARA USARLO POSTA DESCOMENTA DESDE ACÁ
# while True:
#     h.sleep_until_market_open()
#     species = []
#     for section in parser.sections():
#         if section.startswith('Specie'):
#             specie = str(parser.get(section, 'name'))
#             species.append(h.get_stock_values(parser, section))

#     banks = h.get_bank_values(parser)
#     for specie in species:
#         h.calculate_sell_prices(specie, banks.get_bank('BBVA'), cfgValues)
#     stock_values = {}
#     while h.open_market():
#         print "Open market!"
#         for specie in species:
#             stock_values[specie.get('name')] = scrapper.get_stock_price(specie.get('stock_market'), specie.get('name'))
#             trigger_alarm = stock_values[specie.get('name')] <= specie.get('alarm_on')
#             if trigger_alarm:
#                 if specie.get('alarm_for_buy'):
#                     cfgValues.send_mail(specie, 'buy')
#                     title = "Buy %s at %s %.2f" % (specie.get('name'), 
#                                                    specie.get('currency'),
#                                                    stock_values[specie.get('name')])
#                     msg = '%s was at %s %.2f a few minutes ago...' % (specie.get('name'), 
#                                                                       specie.get('currency'), 
#                                                                       stock_values[specie.get('name')])
#                     h.notify_with_title(title, msg)
#                     # specie.alarm_for_buy = False
#             # else:
#             #     specie.alarm_for_buy = True
#             trigger_alarm = specie.get('sell_at') <= stock_values[specie.get('name')] 
#             if trigger_alarm:
#                 if specie.get('alarm_for_sell'):
#                     cfgValues.send_mail(specie, 'sell')
#                     title = "Sell %s at %s %.2f" % (specie.get('name'), 
#                                                    specie.get('currency'),
#                                                    stock_values[specie.get('name')])
#                     msg = '%s was at %s %.2f a few minutes ago...' % (specie.get('name'), 
#                                                                       specie.get('currency'), 
#                                                                       stock_values[specie.get('name')])
#                     h.notify_with_title(title, msg)
#             # else:
#             #     specie.alarm_for_sell = False
#         time.sleep(60 * cfgValues.get('refresh_time'))
#         h.update_cfg(parser, species, stock_values, file)
# # HASTA ACÁ

####################################################################

# PARA QUE PROBARLO DESCOMENTA TODA ESTA PARTE
species = []
for section in parser.sections():
    if section.startswith('Specie'):
        specie = str(parser.get(section, 'name'))
        species.append(h.get_stock_values(parser, section))

banks = h.get_bank_values(parser)
for specie in species:
    h.calculate_sell_prices(specie, banks.get_bank('BBVA'), cfgValues)
stock_values = {}
# while True:
for specie in species:
    # print specie.get('name')
    stock_values[specie.get('name')] = scrapper.get_stock_price(specie.get('stock_market'), specie.get('name'))
    trigger_alarm = stock_values[specie.get('name')] <= specie.get('alarm_on')
    if trigger_alarm:
        if specie.get('alarm_for_buy'):
            # cfgValues.send_mail(specie, 'buy')
            title = "Buy %s at %s %.2f" % (specie.get('name'), 
                                           specie.get('currency'),
                                           stock_values[specie.get('name')])
            msg = '%s was at %s %.2f a few minutes ago...' % (specie.get('name'), 
                                                              specie.get('currency'), 
                                                              stock_values[specie.get('name')])
            h.notify_with_title(title, msg)
            # specie.alarm_for_buy = False
    # else:
    #     specie.alarm_for_buy = True
    trigger_alarm = specie.get('sell_at') <= stock_values[specie.get('name')] 
    if trigger_alarm:
        if specie.get('alarm_for_sell'):
            # cfgValues.send_mail(specie, 'sell')
            title = "Sell %s at %s %.2f" % (specie.get('name'), 
                                           specie.get('currency'),
                                           stock_values[specie.get('name')])
            msg = '%s was at %s %.2f a few minutes ago...' % (specie.get('name'), 
                                                              specie.get('currency'), 
                                                              stock_values[specie.get('name')])
            h.notify_with_title(title, msg)
    # else:
    #     specie.alarm_for_sell = False
time.sleep(60 * cfgValues.get('refresh_time'))
h.update_cfg(parser, species, stock_values, file)
# HASTA ACA