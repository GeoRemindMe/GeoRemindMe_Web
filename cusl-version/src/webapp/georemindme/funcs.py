# coding=utf-8

def make_random_string(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        #"Generates a random string with the given length and given allowed_chars"
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        
        # I take this from django.contrib.auth
        from random import choice
        return ''.join([choice(allowed_chars) for i in xrange(length)])

