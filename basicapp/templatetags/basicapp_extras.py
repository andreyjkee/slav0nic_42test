#coding: utf-8
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def admin_change_url(obj):
    '''
      ticket:8 Tag return `admin change url` for obj
    '''

    url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.module_name), args=[obj.id])
    return mark_safe(u'<a href="%s">(%s)</a>' % (url, obj.__unicode__()))
