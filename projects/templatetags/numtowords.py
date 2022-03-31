from num2words import num2words
from django import template

register = template.Library()


def numtowords(value):
    return num2words(value, )


register.filter('numtowords', numtowords)