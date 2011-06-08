# coding:utf-8
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson as json
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from basicapp.models import RequestLog, UserProfile
from basicapp.forms import EditProfileForm as EditProfileFormOrigin


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
    try:
        c = int(request.GET.get('c', 0))
    except (ValueError, TypeError):
        c = 0
    #if c not in [i[0] for i PRIORITY_CHOICES]:
    #    c = 0
    p = '-priority' if c == 1 else 'priority'
    logs = RequestLog.objects.all().order_by(p, '-date')[:10]
    return render(request, 'basicapp/logs_list.html', {'logs': logs, 'c': c ^ 1, 'cc': c})


@login_required
def edit_form(request, profile_id):
    '''
      ticket:5 Edit form view
      ticket:7
    '''

    class EditProfileForm(EditProfileFormOrigin):
        '''
          ticket:7 New form with changed keyOrder
        '''

        def __init__(self, *args, **kwargs):
            super(EditProfileForm, self).__init__(*args, **kwargs)
            self.fields.keyOrder.reverse()

    uprofile = get_object_or_404(UserProfile, pk=profile_id)
    if request.method == 'POST' and request.is_ajax():
        form = EditProfileForm(request.POST, instance=uprofile)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            errors = ["%s: %s" % (k, ', '.join(map(unicode, v))) for (k, v) in form.errors.iteritems()]
            errors_text = "; ".join(errors)
            return HttpResponse(json.dumps({'success': False, 'errors': errors_text}),
                                content_type='application/json')
    else:
        form = EditProfileForm(instance=uprofile)
    return render(request, 'basicapp/edit_form.html', {'form': form, 'profile': uprofile})


def change_priority(request, lid):
    l = get_object_or_404(RequestLog, pk=lid)
    l.invert_priority()
    l.save()
    if 'c' in request.GET:
        c = request.GET['c']
        redirect_url = reverse('basicapp:logs') + '?c=%s' % c
        return redirect(redirect_url)
    return redirect('basicapp:logs')
