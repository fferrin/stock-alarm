#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ConfigParser
import helpers as h
from webscrapper import WebScrapper

"""
Main program where the pieces are putted together.
"""

def main():
    parser = ConfigParser.ConfigParser()
    scrapper = WebScrapper()
    # ! TODO (Fuuccker): Add file as an option 
    file = 'stock-alarm.config'
    parser.read(file)
    h.print_log("Reading configuration file")
    cfgValues = h.get_config_values(parser)
    notificate_through_email = cfgValues.has("mail_to")

    # Get banks values (just one time)
    h.print_log("Getting bank's values")
    banks = h.get_bank_values(parser)
    while True:
        if not h.open_market():
            h.print_log("Waiting for open market")
            h.sleep_until_market_open()
        else:
            h.print_log("Market is open!")

        # Get stock values for each specie
        species = []
        h.print_log("Reading configuration file for stock values")
        for section in parser.sections():
            if section.startswith('Specie'):
                specie = str(parser.get(section, 'name'))
                species.append(h.get_stock_values(parser, section))
                h.calculate_sell_prices(species[-1], banks.get_bank('BBVA'))

        stk_val = {}
        # while h.open_market():
        while True:
            # While open market, scrap web page and fire alarms if necessary
            for specie in species:
                h.print_log("Getting values for " + specie.get('name'))
                stk_val[specie.get('name')] = scrapper.get_stock_price(
                                                specie.get('stock_market'),
                                                specie.get('name'))
                
                h.print_log(specie.get('name') + " is at " + str(stk_val[specie.get('name')]))

                trg_alarm = stk_val[specie.get('name')] <= specie.get('alarm_on')
                if trg_alarm:
                    if specie.get('alarm_for_buy'):
                        if notificate_through_email:
                            cfgValues.send_mail(specie, 'buy')
                        title = """
                                Buy %s at %s %.2f
                                """ % (specie.get('name'), 
                                       specie.get('currency'),
                                       stk_val[specie.get('name')])
                        msg = """
                              %s was at %s %.2f a few minutes ago...
                              """ % (specie.get('name'), 
                                     specie.get('currency'), 
                                     stk_val[specie.get('name')])
                        h.notify_with_title(title, msg)
                        h.print_log("Buy " + specie.get('name') + " at " + specie.get('currency') + " " + str(stk_val[specie.get('name')]))
                        specie.alarm_for_buy = False
                else:
                    specie.alarm_for_buy = True
                
                # trg_alarm = specie.get('sell_at') <= stk_val[specie.get('name')] 
                trg_alarm = False
                if trg_alarm:
                    if specie.get('alarm_for_sell'):
                        if notificate_through_email:
                            cfgValues.send_mail(specie, 'sell')
                        title = """
                                Sell %s at %s %.2f
                                """ % (specie.get('name'), 
                                       specie.get('currency'),
                                       stk_val[specie.get('name')])
                        msg = """
                              %s was at %s %.2f a few minutes ago...
                              """ % (specie.get('name'), 
                                     specie.get('currency'), 
                                     stk_val[specie.get('name')])
                        h.notify_with_title(title, msg)
                        h.print_log("Sell " + specie.get('name') + " at " + specie.get('currency') + " " + str(stk_val[specie.get('name')]))
                else:
                    specie.alarm_for_sell = False
            h.print_log("Updating configuration file with new stock prices")
            h.update_cfg(parser, species, stk_val, file)
            h.print_log("Waiting " + str(cfgValues.get('refresh_time')) + "min to update...")
            time.sleep(60 * cfgValues.get('refresh_time'))
    
if __name__  == '__main__':
    main()