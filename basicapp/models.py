#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    '''
      Basic user profile model
    '''

    user = models.OneToOneField(User, verbose_name=_('User'))
    birthday = models.DateField(_('Date of birth'))
    bio = models.TextField(_('Bio'), help_text=_("Html supported"))
    skype = models.CharField(_('Skype'), validators=[MinLengthValidator(6)],
                             max_length=255, blank=True) # skypename must be > 6 & < ? :)
    jabber = models.EmailField(_('Jabber'), blank=True)
    other_contacts = models.TextField(_('Other contacts'), blank=True)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return self.user.username
