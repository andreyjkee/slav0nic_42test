#coding: utf-8
from .models import RequestLog

class RequestLogMiddleware(object):

    def process_request(self, request):
        RequestLog.objects.save_from_request(request)
