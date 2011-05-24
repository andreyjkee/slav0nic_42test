# coding:utf-8
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from basicapp.models import RequestLog, UserProfile
from basicapp.forms import EditProfileForm

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


def logs(request):
    '''
      Show first 10 http requests 
    '''
    logs = RequestLog.objects.all()[:10]
    return render(request, 'basicapp/logs_list.html', {'logs': logs})


@login_required
def edit_form(request, profile_id):
    '''
      ticket:5 Edit form view
    '''
    uprofile = get_object_or_404(UserProfile, pk=profile_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=uprofile)
        if form.is_valid():
            form.save()
            return redirect('basicapp:index')
    else:
        form = EditProfileForm(instance=uprofile)
    return render(request, 'basicapp/edit_form.html', {'form': form, 'profile': uprofile})