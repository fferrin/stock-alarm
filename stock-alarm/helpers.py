#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from stock import Stock
from bank import Banks
from datetime import date
from datetime import datetime
from datetime import timedelta
import subprocess
import time
    

"""
Module containing useful functions needed to run the program.
"""

def get_config_values(parser):
    section = 'Configuration'
    # Get options from ``Configuration`` section
    options = parser.options(section)
    values = {}
    for opt in options:
        values[opt] = parser.get(section, opt)
    config = Config(values)
    return config


def get_bank_values(parser):
    banks = Banks()
    banks.add_fees(parser.items('Fees'))
    banks.add_tna(parser.items('NIM'))
    return banks


def get_stock_values(parser, section):
    options = parser.options(section)
    stock_data = {}
    for opt in options:
        stock_data[opt] = parser.get(section, opt)
    return Stock(stock_data)
    

def sleep_until_market_open():
    now = datetime.now()
    weekday = now.weekday()
    if weekday < 5: # If is weekday
        if now.hour < 11:   # Before 11am
            open_market = now.replace(hour = 11, 
                                     minute = 00, 
                                     second = 00, 
                                     microsecond = 00)
        elif 17 <= now.hour:    # After 5pm
            open_market = (now + timedelta(days=1)).replace(hour = 11, 
                                                            minute = 00, 
                                                            second = 00, 
                                                            microsecond = 00)
        else:   # Market is open
            open_market = now
    elif weekday == 5:  # If is saturday
        open_market = (now + timedelta(days=2)).replace(hour = 11, 
                                                        minute = 00, 
                                                        second = 00, 
                                                        microsecond = 00)
    else:   # If is sunday
        open_market = (now + timedelta(days=1)).replace(hour = 11, 
                                                        minute = 00, 
                                                        second = 00, 
                                                        microsecond = 00)
    time.sleep((open_market - now).seconds) # Sleep until market open


def open_market():
    now = datetime.now()
    if 11 < now.hour < 17:
        return True
    return False


def calculate_sell_prices(specie, bank):
    if specie.has('stock', 'bought_at'):
        buy_date = specie.get('date')
        sell_date = datetime.now()
        days = (sell_date - buy_date).days
        specie.set_sell_at((1 + bank.get('NIM'))**(days/365.0) * 
                           specie.get('bought_at') *
                           (1 + bank.get('Fee'))/(1 - bank.get('Fee')))


def notify_with_title(title, message):
    subprocess.Popen(['notify-send', title, message])
    return


def notify(message):
    subprocess.Popen(['notify-send', message])
    return


def update_cfg(parser, species, values, file):
    index = 0
    for section in parser.sections():
        if section.startswith('Specie'):
            specie = species[index]
            if specie.has('sell_at'):
                parser.set(section, 'sell_at', str(specie.get('sell_at')))
            parser.set(section, 'actual_price', values[specie.get('name')])
            index = index + 1
    with open(file, 'w') as configfile:
        parser.write(configfile)

def print_log(msg):
    print """[%s %s]: %s""" % (time.strftime("%d/%m/%Y"),
                                    time.strftime("%H:%M:%S"),
                                    msg)