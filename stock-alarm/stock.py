#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class Stock():
    """
    Class to store stock values readed from the configuration file.

    Here are important parameters, such as the date of adquisition, the amount
    of stocks bought, etcetera, witch allow to calculate sell prices at the
    current date to gain at least the same rate than bank fixed deposits.

    Args:
        values (dict): Options with its corresponding values.

    Attributes:
        stock_market (str): Market exchange where found the given specie.
        currency (str): Currency in witch actual stock is measured.
        name (str): Name of the stock.
        actual_price (Optional[float]): Current price of the stock.
        date (Optional[date object]): Date when the stocks were bought.
        buy_at (Optional[float]): Price at witch stocks were bought.
        stock (Optional[int]): Amount of stocks bought.
        sell_at (Optional[float]): Sell price for witch the gain is equals to
            the bank fixed deposit rates.
        alarm_on (Optional[float]): Price at witch we want to get notified.
        alarm_for_buy (bool): True if we want to get notified at ``alarm_on``
            price. False otherwise.
        alarm_for_sell (bool): True if we want to get notified at ``sell_at``
            price. False otherwise.

    """
    def __init__(self, values):
        for item in values:
            self._get_value(item, values.get(item))
        self.alarm_for_sell = True
        if self.has('alarm_on'):
            self.alarm_for_buy = True

    def __str__(self):
        raise NotImplementedError

    def _get_value(self, item, value):
        """
        Get the value of a setting.

        Args:
            item (str): Setting.
            value (str): Value of the setting.

        """
        if not self._empty_input(value):
            if item == 'actual_price':
                setattr(self, item, float(value))
            elif item == 'date':
                setattr(self, item, datetime.strptime(value, '%d/%m/%Y'))
            elif item == 'buy_at':
                setattr(self, item, float(value))
            elif item == 'stock':
                setattr(self, item, int(value))
            elif item == 'sell_at':
                setattr(self, item, float(value))
            elif item == 'alarm_on':
                setattr(self, item, float(value))
            else:
                setattr(self, item, value)

    def _empty_input(self, value):
        """
        Check for setting without value.

        Args:
            value (str): Value of a setting.

        Returns:
            bool: True if setting has value, False otherwise.

        """
        if value == '' or value is None:
            return True
        else:
            return False

    def name(self):
        return self.specie

    def has(self, *attrs):
        """
        Check if class instance has given settings as attributes.

        Args:
            \*attrs (str): List of attributes to check.
        
        Returns:
            bool: True if class instance has all the attributes. False
                otherwise.

        """
        for attr in attrs:
            if not hasattr(self, attr):
                return False
        return True

    def get(self, attr):
        """
        Get the value of a given option.

        Args:
            attr (str): Attribute of which value will be returned.
        
        Returns:
            str: If ``attr`` is ``stock_market``, ``currency`` or ``name``.
            float: If ``attr`` is ``actual_price``, ``buy_at``, ``sell_at`` or
                ``alarm_on``.
            date object: If ``attr`` is ``date``.
            int: If ``attr`` is ``stock``.
            bool: If ``attr`` is ``alarm_for_buy`` or ``alarm_for_sell``.

        """
        if hasattr(self, attr):
            return getattr(self, attr)

    def set_actual_price(self, actual_price):
        """
        Set current price of the specie.

        Args:
            actual_price (float): Current price of the specie.

        """
        self.actual_price = actual_price

    def set_sell_at(self, sell_at):
        """
        Set sell price.

        Args:
            sell_at (float): Sell price of the specie.

        """
        self.sell_at = round(float(sell_at), 4)
