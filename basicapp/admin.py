#coding: utf-8
from django.contrib import admin
from basicapp.models import UserProfile, RequestLog


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skype', 'jabber', 'birthday']
    raw_id_fields = ['user'] # whithout this your can get fun on big DB ;)

class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['date', 'method', 'path', 'remote_addr']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RequestLog, RequestLogAdmin)

