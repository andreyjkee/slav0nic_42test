#coding: utf-8

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'basicapp.views.index', name='index'),
    url(r'^logs$', 'basicapp.views.logs', name='logs'),
    url(r'^edit/(?P<profile_id>\d+)/', 'basicapp.views.edit_form', name='edit_form'),
    url(r'^p/(?P<lid>\d+)/', 'basicapp.views.change_priority', name='change_priority'),
)
