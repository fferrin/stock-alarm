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
    """
    Get and save configuration values from configuration file.

    Args:
        parser (ConfigParser object): ConfigParser instance used as parser.

    Returns:
        Config object: Config object with values setting accord to
            the configuration file.

    """
    section = 'Configuration'
    # Get options from ``Configuration`` section
    options = parser.options(section)
    values = {}
    for opt in options:
        values[opt] = parser.get(section, opt)
    config = Config(values)
    return config


def get_bank_values(parser):
    """
    Get and save bank values from configuration file.

    Args:
        parser (ConfigParser object): ConfigParser instance used as parser.

    Returns:
        Banks object: Banks instance with bank's values.

    """
    banks = Banks()
    banks.add_fees(parser.items('Fees'))
    banks.add_tna(parser.items('NIM'))
    return banks


def get_stock_values(parser, section):
    """
    Get and save species values from configuration file.

    Args:
        parser (ConfigParser object): ConfigParser instance used as parser.
        section (str): Name of the section in configuration file corresponding
            to a specie.

    Returns:
        Stock object: Stock instance with specie's values.

    """
    options = parser.options(section)
    stock_data = {}
    for opt in options:
        stock_data[opt] = parser.get(section, opt)
    return Stock(stock_data)
    

def sleep_until_market_open():
    """
    Calculate time left to open market and sleep until then.
    """
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
    """
    Once the market is open, check if it's still open.

    Returns:
        bool: True if market is open. False otherwise.
    """
    now = datetime.now()
    if 11 < now.hour < 17:
        return True
    return False


def calculate_sell_prices(specie, bank):
    """
    Calculate sell prices for now to earn at least the same as NIM of the bank.

    If you bought stock, you want to sell it to give you at least the same
    mnoney that you would earned if you deposit your money in a bank and
    receive the NIM for it.

    Example:
        You bought stock at ``$_b`` in ``date_b``. Now, ``days`` days after
        you want to sell your stocks but you want to know the minimum value
        at you will gain the same as if you have putted your money in a bank
        with a NIM ``NIM``. Bank charge you with the ``%_{fee}``%. So, today
        you have to sell at:

        ``$_s = $_b * (1 + NIM)^{days/365} * \frac{1 + %_{fee}}{1 - %_{fee}}``

    Args:
        specie (Stock object): Stock instance with specie's values.
        bank (Bank object): Bank instance with bank's values.

    """
    if specie.has('stock', 'bought_at'):
        buy_date = specie.get('date')
        sell_date = datetime.now()
        days = (sell_date - buy_date).days
        specie.set_sell_at((1 + bank.get('NIM'))**(days/365.0) * 
                           specie.get('bought_at') *
                           (1 + bank.get('Fee'))/(1 - bank.get('Fee')))


def notify_with_title(title, message):
    """
    Send a message notification to Linux desktop with title.
    """
    subprocess.Popen(['notify-send', title, message])
    return


def notify(message):
    """
    Send a message notification to Linux desktop.
    """
    subprocess.Popen(['notify-send', message])
    return


def update_cfg(parser, species, values, file):
    """
    Update configuration file with ``sell_at`` and ``actual_price`` values.

    Args:
        parser (ConfigParser object): ConfigParser instance used as parser.
        species (list): List of species in configuration file passed in order
            at witch they appear in the file.
        values (dict): Dictionary with specie's name as keys and their 
            corresponding actual price as value.
        file (str): Name of the configuration file.

    """
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
    
    """
    Print log message.

    Args:
        msg: Log message.
    """
    print """[%s %s]: %s""" % (time.strftime("%d/%m/%Y"),
                                    time.strftime("%H:%M:%S"),
                                    msg)