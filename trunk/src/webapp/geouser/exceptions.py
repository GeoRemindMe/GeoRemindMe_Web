# coding:utf-8


class OutdatedCode(Exception):
    value = "This code is outdated"


class BadCode(Exception):
    value = "This code is invalid"

    
class RegistrationException(Exception):
    value = "Problems with registration. Please, try again later"
