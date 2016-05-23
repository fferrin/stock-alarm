#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class Stock():
    def __init__(self, values):
        # print values
        for item in values:
            self.get_value(item, values.get(item))
        self.alarm_for_buy = True
        if self.has('sell_at'):
            self.alarm_for_sell = True

    def __str__(self):
        if not self.has('stock'):
            return ''
        s = ""
        s += "Specie: %s (%s)\n" % (self.specie, self.stock_market)
        s += "   - Buy price: %s %.2f\n" % (self.currency, self.buy_at)
        s += "   - Buy date:  %s\n" % self.date.strftime('%d/%m/%Y')
        s += "   - Stock:     %d" % self.stock
        return s

    # Toma el valor si no es nulo
    def get_value(self, item, value):
        # print "Value: '%s' (%r)" % (value, value == '')
        if not self.empty_input(value):
            # print value
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

    # Ve si el valor de entrada es nulo
    def empty_input(self, value):
        if value == '' or value is None:
            return True
        else:
            return False

    def name(self):
        return self.specie

    def has(self, *attrs):
        for attr in attrs:
            if not hasattr(self, attr):
                return False
        return True

    def get(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)

    def set_actual_price(self, actual_price):
        self.actual_price = actual_price

    def set_sell_at(self, sell_at):
        self.sell_at = round(float(sell_at), 4)
