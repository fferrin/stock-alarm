#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib

class Config():
    def __init__(self, values):
        for item in values:
            self.get_value(item, values.get(item))

    # Ve si el valor de entrada es nulo
    def empty_input(self, value):
        if value == '' or value is None:
            return True
        else:
            return False

    def get_value(self, item, value):
        if not self.empty_input(value):
            if item == 'refresh_time':
                setattr(self, item, int(value))
            else:
                setattr(self, item, value)

    def has(self, *attrs):
        for attr in attrs:
            if not hasattr(self, attr):
                return False
        return True

    def get(self, attr):
        if attr != 'mail_pass':
            if hasattr(self, attr):
                return getattr(self, attr)

    def send_mail(self, specie, action):
        # Credentials (if needed)
        gmail_user = self.mail_from
        gmail_password = self.mail_pass

        to = [self.mail_to]  
        if action == 'buy':
            subject = '[ALARM] Buy %s at %s %.2f' % (specie.get('name'), specie.get('currency'), specie.get('actual_price'))
            body = '%s was at %s %.2f a few minutes ago...' % (specie.get('name'), specie.get('currency'), specie.get('actual_price'))
        elif action == 'sell':
            subject = '[ALARM] Sell %s at %s %.2f' % (specie.get('name'), specie.get('currency'), specie.get('actual_price'))
            body = '%s was at %s %.2f a few minutes ago...' % (specie.get('name'), specie.get('currency'), specie.get('actual_price'))
        else:
            return 

        email_text = "Subject: %s\n\n%s" % (subject, body)
    
        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.mail_from, self.mail_pass)
            server.sendmail(self.mail_from, self.mail_to, email_text)
            server.close()

            print 'Email sent!'
        except:  
            print 'Something went wrong...'
