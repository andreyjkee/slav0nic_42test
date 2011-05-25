#coding: utf-8
from django.db import models
from django.http import HttpRequest


# maybe will be more correct do this via @classmethod
class RequestLogManager(models.Manager):
    def save_from_request(self, request, commit=True):
        '''
           Save RequesLog object from HTTPRequest objecs.
           Return and save RequesLog entry to DB (save only if `commit` set).
        '''
        assert isinstance(request, HttpRequest), u"Request must be HttpRequest instance"
        path = request.path_info
        encoding = request.encoding or ''
        method = request.method
        qs = request.META.get('QUERY_STRING', '')[:2083]
        remote_addr = request.META.get('REMOTE_ADDR', '')
        referer = request.META.get('HTTP_REFERER', '')[:2083]
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        req_log = self.model(encoding=encoding,
                             method=method,
                             qs=qs,
                             path=path,
                             remote_addr=remote_addr,
                             referer=referer,
                             user_agent=user_agent)
        if commit:
            req_log.save()
        return req_log
