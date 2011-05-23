# coding:utf-8
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    '''
      Main page view.
      Return info about user with pk=1
    '''

    user = get_object_or_404(User, pk=1)
    try:
        uprofile = user.get_profile()
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'basicapp/profile_detail.html', {'profile': uprofile})
