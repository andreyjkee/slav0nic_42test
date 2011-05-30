#coding: utf-8
from django.contrib import admin
from basicapp.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skype', 'jabber', 'birthday']
    raw_id_fields = ['user'] # whithout this your can get fun on big DB ;)


admin.site.register(UserProfile, UserProfileAdmin)
