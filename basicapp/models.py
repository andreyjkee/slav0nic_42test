#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

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

    @property
    def edit_url(self):
        return reverse('basicapp:edit_form', kwargs={'profile_id': self.pk})


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


from basicapp.middleware import get_current_request


def log_changes(sender, obj, flag):
    """
      ticket:10 Log changes to DB
    """
    request = get_current_request()
    if sender is LogEntry or request is None:
        return
    # LogEntry model required user field =*(
    if request.user.is_authenticated():
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(sender).pk,
            object_id=obj.pk,
            object_repr=force_unicode(obj),
            action_flag=flag)


@receiver(post_save)
def post_save_handler(sender, **kwargs):
    obj = kwargs['instance']
    flag = ADDITION if kwargs['created'] else CHANGE
    log_changes(sender, obj, flag)


@receiver(post_delete)
def post_delete_handler(sender, **kwargs):
    obj = kwargs['instance']
    print obj, 'deleted'
    log_changes(sender, obj, DELETION)
