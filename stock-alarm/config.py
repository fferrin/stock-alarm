#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib

class Config(object):
    """
    Class to deal with configuration's parameters.

    Args: 
        values (dict): Options with its corresponding values.

    Attributes:
        allowed_values (list): Allowed settings for the class.
        refresh_time (Optional[int]): Updating time (in minutes) for getting
            stock values.
        mail_to (Optional[str]): Email address for send notifications.
        mail_from (Optional[str]): Email address of notifier.
        mail_pass (Optional[str]): 
    """
    allowed_values = [
        'refresh_time',
        'mail_to',
        'mail_from',
        'mail_pass'
    ]

    def __init__(self, values):
        for item in values:
            self._get_value_of_setting(item, values.get(item))

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

    def _get_value_of_setting(self, item, value):
        """
        Get the value of a setting.

        Args:
            item (str): Setting.
            value (str): Value of the setting.

        """
        if not self._empty_input(value):
            if item == 'refresh_time':
                setattr(self, item, int(value))
            else:
                setattr(self, item, value)

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
        Get the value of a given option (except for email password).

        Args:
            attr (str): Attribute of which value will be returned.
        
        Returns:
            int: If ``attr`` is ``refresh_time``
            str: Otherwise

        """
        if attr != 'mail_pass':
            if hasattr(self, attr):
                return getattr(self, attr)

    def send_mail(self, specie, action):
        """
        Send an email for sell or buy a stock based on configuration file.

        Args:
            specie (Stock object): Object with values from the configuration
                file.
            action (str): Option for buy or sell notification.
        
        Raises:
            ConnectionError: Can't send email.

        """
        gmail_user = self.get('mail_from')
        gmail_password = self.get('mail_pass')
        to = self.get('mail_to')

        # Setup email
        if action == 'buy':     # For buy
            subject = """
                      [ALARM] Buy %s at %s %.2f
                      """ % (specie.get('name'), 
                             specie.get('currency'), 
                             specie.get('actual_price'))
            body = """
                   %s was at %s %.2f a few minutes ago...
                   """ % (specie.get('name'), 
                          specie.get('currency'), 
                          specie.get('actual_price'))
        elif action == 'sell':  # For sell
            subject = """
                    [ALARM] Sell %s at %s %.2f
                    """ % (specie.get('name'), 
                           specie.get('currency'), 
                           specie.get('actual_price'))
            body = """
                   %s was at %s %.2f a few minutes ago...
                   """ % (specie.get('name'), 
                          specie.get('currency'), 
                          specie.get('actual_price'))
        else:                   # Return otherwise
            return 

        email_text = "Subject: %s\n\n%s" % (subject, body)
    
        # Try to send email
        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.mail_from, self.mail_pass)
            server.sendmail(self.mail_from, self.mail_to, email_text)
            server.close()

        except ConnectionError:  
            print 'Something went wrong...'
