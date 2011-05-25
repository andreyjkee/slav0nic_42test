#coding: utf-8
from .models import RequestLog
from django.utils._threading_local import local


_thread_locals = local()


class RequestLogMiddleware(object):

    def process_request(self, request):
        RequestLog.objects.save_from_request(request)


def get_current_request():
    """
      returns the request object for this thead
    """
    return getattr(_thread_locals, "request", None)


class ThreadLocalMiddleware(object):
    """
      Simple middleware that adds the request object in thread local storage.
    """

    def process_request(self, request):
        _thread_locals.request = request
