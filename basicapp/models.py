#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _

from basicapp.managers import RequestLogManager


class UserProfile(models.Model):
    '''
      Basic user profile model
    '''

    user = models.OneToOneField(User, verbose_name=_('User'))
    birthday = models.DateField(_('Date of birth'))
    bio = models.TextField(_('Bio'), help_text=_("Html supported"))
    skype = models.CharField(_('Skype'), validators=[MinLengthValidator(6)],
                             max_length=255, blank=True, default='') # skypename must be > 6 & < ? :)
    jabber = models.EmailField(_('Jabber'), blank=True, default='')
    other_contacts = models.TextField(_('Other contacts'), blank=True, default='')

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return self.user.username


class RequestLog(models.Model):
    path = models.CharField(_('Path info'), max_length=2083) # size from mostly browser; RFC sucks
    encoding = models.CharField(_('Encoding'), max_length=64, blank=True, default='')
    method = models.CharField(_('Request method'), max_length=64)
    qs = models.CharField(_('Query string'), max_length=2083, blank=True, default='')
    remote_addr = models.IPAddressField(_('Client IP'))
    referer = models.CharField(_('Refferer'), max_length=2083, blank=True, default='')
    user_agent = models.CharField(_('User agent'), max_length=255, blank=True, default='')
    date = models.DateTimeField(_('Date'), auto_now_add=True)

    objects = RequestLogManager()

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')
        ordering = ['-date']

    def __unicode__(self):
        return u" ".join((str(self.date), self.method, self.path))
