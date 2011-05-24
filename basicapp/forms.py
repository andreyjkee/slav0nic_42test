#coding: utf-8

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

from basicapp.models import UserProfile
from basicapp.widgets import JSDataPickerWidget
# magic %)
# user_max_length = User._meta.get_field('first_name').max_length


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return mark_safe(u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self]))


class EditProfileForm(forms.ModelForm):
    '''
      ticket:5 Basic model form
      why i do ticket:1 via 2 models? =\\
    '''

    last_name = forms.CharField(label=_('Last name'), max_length=30)
    first_name = forms.CharField(label=_('First name'), max_length=30)
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ('first_name', 'email', 'last_name', 'jabber', 'birthday',\
                  'skype', 'bio', 'other_contacts')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.fields['birthday'].widget = JSDataPickerWidget()

        self.error_class = DivErrorList

    def save(self, commit=True):
        uprofile = super(EditProfileForm, self).save(commit)

        uprofile.user.last_name = self.cleaned_data['last_name']
        uprofile.user.first_name = self.cleaned_data['first_name']
        uprofile.user.email = self.cleaned_data['email']
        uprofile.user.save(force_update=True)
        return uprofile
