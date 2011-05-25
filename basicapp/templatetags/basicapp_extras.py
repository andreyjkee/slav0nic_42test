#coding: utf-8
from django import template

register = template.Library()

@register.simple_tag
def admin_change_url(obj):
    '''
      ticket:8 Tag return `admin change url` for obj
    '''


    return ''
