#coding: utf-8
from django.db import models


class RequestLogManager(models.Manager):
    def save_from_request(self, request, commit=True):
        '''
           Save RequesLog object from HTTP Request objecs.
           Return and save RequesLog entry to DB (save only if `commit` set).
        '''
        pass
