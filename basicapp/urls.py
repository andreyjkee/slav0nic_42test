#coding: utf-8

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'basicapp.views.index', name='index'),
)