#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Bank():
    def __init__(self, name):
        self.name = name.upper()
        self.values = {}

    def name(self):
        return self.name

    def add_fee(self, fee):
        self.values['Fee'] = float(fee)

    def get_fee(self):
        return self.values['Fee']

    def add_tna(self, tna):
        self.values['TNA'] = float(tna)

    def get_tna(self):
        return self.values['TNA']

    def __str__(self):
        s = ""
        s += "\n  Bank: %s" % self.name
        for key, value in self.values.iteritems():
            s += "\n    %s: %.4f%%" % (key, value)
        return s

class Banks():
    def __init__(self):
        self.banks = {}

    def __str__(self):
        s = ""
        s += "-- BANKS --\n"
        for bank in self.banks:
            s += self.banks[bank].__str__()
        return s

    def get_bank(self, bank):
        if bank in self.banks:
            return self.banks[bank]
        else:
            return None

    def add_fees(self, dict_with_values):
        for bank, value in dict_with_values:
            bank = bank.upper()
            if bank not in self.banks:
                self.banks[bank] = Bank(bank)
            self.banks[bank].add_fee(float(value))

    def add_tna(self, dict_with_values):
        for bank, value in dict_with_values:
            bank = bank.upper()
            if bank not in self.banks:
                self.banks[bank] = Bank(bank)
            self.banks[bank].add_tna(float(value))

    def get_tna(self, bank):
        if bank not in self.banks:
            return None
        else:
            return self.banks[bank].get_tna()

    def get_fee(self, bank):
        if bank not in self.banks:
            return None
        else:
            return self.banks[bank].get_fee()
