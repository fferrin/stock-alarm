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

def get_config_values(parser):
    section = 'Configuration'
    options = parser.options(section)
    values = {}
    for opt in options:
        values[opt] = parser.get(section, opt)
    config = Config(values)
    return config

def get_stock_values(parser, section):
    options = parser.options(section)
    stock_data = {}
    for opt in options:
        stock_data[opt] = parser.get(section, opt)
    stock = Stock(stock_data)
    return stock

def get_bank_values(parser):
    banks = Banks()
    banks.add_fees(parser.items('Fees'))
    banks.add_tna(parser.items('TNA'))
    return banks

def calculate_sell_prices(specie, bank, config):
    if specie.has('stock', 'buy_at'):
        buy_date = specie.get('date')
        sell_date = datetime.now()
        days = (sell_date - buy_date).days
        specie.set_sell_at((1 + bank.get_tna())**(days/365.0) * 
                           specie.get('buy_at') *
                           (1 + bank.get_fee())/(1 - bank.get_fee()))

def update_cfg(parser, species, values, file):
    index = 0
    for section in parser.sections():
        if section.startswith('Specie'):
            specie = species[index]
            if specie.has('sell_at'):
                parser.set(section, 'sell_at', str(specie.get('sell_at')))

            parser.set(section, 'actual_price', values[specie.get('name')])
            index += 1
    with open(file, 'w') as configfile:
        parser.write(configfile)

def notify_with_title(title, message):
    subprocess.Popen(['notify-send', title, message])
    return

def notify(message):
    subprocess.Popen(['notify-send', message])
    return
    
def sleep_until_market_open():
    now = datetime.now()
    weekday = now.weekday()
    if weekday < 5:
        if now.hour < 11:
            open_market = now.replace(hour = 11, 
                                     minute = 00, 
                                     second = 00, 
                                     microsecond = 00)
        elif 17 <= now.hour:
            open_market = (now + timedelta(days=1)).replace(hour = 11, 
                                                            minute = 00, 
                                                            second = 00, 
                                                            microsecond = 00)
        else:
            open_market = now
    elif weekday == 5:
        open_market = (now + timedelta(days=2)).replace(hour = 11, 
                                                        minute = 00, 
                                                        second = 00, 
                                                        microsecond = 00)
    else:
        open_market = (now + timedelta(days=1)).replace(hour = 11, 
                                                        minute = 00, 
                                                        second = 00, 
                                                        microsecond = 00)
    time.sleep((open_market - now).seconds)

def open_market():
    now = datetime.now()
    if 11 < now.hour < 17:
        return True
    return False
    