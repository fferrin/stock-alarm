#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Bank(object):
    allowed_values = [
        'name',
        'Fee',
        'NIM'
    ]
    
    def __init__(self, name):
        self.name = name.upper()
        self.values = {}

    def __str__(self):
        raise NotImplementedError

    def get(self, attr):
        if attr in self.allowed_values:
            if attr == "Fee":
                return self.values['Fee']
            elif attr == "NIM":
                return self.values['NIM']
            else:
                return getattr(self, attr)
        else:
            return None

    def add(self, attr, value):
        if attr in self.allowed_values:
            if attr == "Fee":
                self.values['Fee'] = value
            elif attr == "NIM":
                self.values['NIM'] = value


class Banks(object):
    allowed_values = [
        'name',
        'Fee',
        'NIM'
    ]

    def __init__(self):
        self.banks = {}

    def __str__(self):
        raise NotImplementedError

    def get_bank(self, bank):
        if bank in self.banks:
            return self.banks[bank.upper()]
        else:
            return None

    def get(self, bank, attr):
        if bank not in self.banks:
            return None
        elif attr in self.allowed_values:
            if attr == "NIM":
                return self.get_bank(bank).get('NIM')
            elif attr == "Fee":
                # print self.get_bank(bank).get('Fee')
                return self.get_bank(bank).get('Fee')
            else:
                return None

    def add_fees(self, values):
        for bank, value in values:
            bank = bank.upper()
            if bank not in self.banks:
                self.banks[bank] = Bank(bank)
            self.get_bank(bank).add('Fee', float(value))

    def add_tna(self, values):
        for bank, value in values:
            bank = bank.upper()
            if bank not in self.banks:
                self.banks[bank] = Bank(bank)
            self.get_bank(bank).add('NIM', float(value))
