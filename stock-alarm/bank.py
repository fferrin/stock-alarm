#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Bank(object):
    """
    Class to store bank values readed from the configuration file.

    Here are important parameters, such as the charge for buying stocks and
    the bank's NIM.

    Args:
        name (str): Name of the bank.

    Attributes:
        name (str): Name of the bank.
        values (dict): Net Interest Margin (NIM) and charges (Fee) values.
        
    """
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
        """
        Get the value of a given option.

        Args:
            attr (str): Attribute of which value will be returned.
        
        Returns:
            float: If ``attr`` is ``Fee`` or ``NIM``.
            str: If ``attr`` is ``name``.
            None: If ``attr`` isn't a bank's attribute.

        """
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
        """
        Add ``NIM`` or ``Fee`` of the bank.

        Args:
            value (float): Value of the attribute
            attr (str): Attribute of which value will be setted.

        """
        if attr in self.allowed_values:
            if attr == "Fee":
                self.values['Fee'] = value
            elif attr == "NIM":
                self.values['NIM'] = value


class Banks(object):
    """
    Class to store bank objects with its corresponding values.

    Attributes:
        banks (dict): Dictionary with bank's name as key and bank object as
            value for each one of the banks in the configuration file.
        
    """
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
        """
        Get bank object.

        Args:
            bank (str): Bank's name.
        
        Returns:
            Bank object: Object of given bank.
            None: Other if ``bank`` isn't in ``banks``.

        """
        if bank in self.banks:
            return self.banks[bank.upper()]
        else:
            return None

    def get(self, bank, attr):
        """
        Get given attribute of given bank.

        Args:
            bank (str): Bank's name.
            attr (str): Attribute of which value will be returned.
        
        Returns:
            Bank object: Object of given bank.
            None: If ``bank`` isn't in ``banks`` or ``attr`` isn't a bank's
                attribute.

        """
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
        """
        Add fees to banks.

        Args:
            values (dict): Dictionary with banks as keys and fees as values.

        """
        for bank, value in values:
            bank = bank.upper()
            if bank not in self.banks:
                self.banks[bank] = Bank(bank)
            self.get_bank(bank).add('Fee', float(value))

    def add_tna(self, values):
        """
        Add NIMs to banks.

        Args:
            values (dict): Dictionary with banks as keys and NIMs as values.

        """
        for bank, value in values:
            bank = bank.upper()
            if bank not in self.banks:
                self.banks[bank] = Bank(bank)
            self.get_bank(bank).add('NIM', float(value))
