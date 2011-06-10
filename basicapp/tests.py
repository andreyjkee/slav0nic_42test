#coding: utf-8
from datetime import datetime
from StringIO import StringIO

from tddspry.django import DatabaseTestCase, HttpTestCase, TestCase
from django.contrib.auth.models import User
from django.core import management
from django.contrib.admin.models import LogEntry

from basicapp.models import UserProfile, RequestLog
from basicapp.context_processors import settings_processor
from basicapp.templatetags.basicapp_extras import admin_change_url

TEST_DATA = {
    'birthday': datetime(1985, 1, 12).date(),
    'bio': u'lazy clerk from <b>UA</b>',
    'other_contacts': u'root@python.su',
}


class TestT1DB(DatabaseTestCase):
    '''
      ticket:1 database testcase
    '''

    def test_profile(self):
        user = self.helper('create_user', active=False)
        self.helper('create_profile',
                        user,
                        UserProfile,
                        bio=TEST_DATA['bio'],
                        birthday=TEST_DATA['birthday']
                    )
        p = user.get_profile()
        self.assert_equal(p.bio, TEST_DATA['bio'])
        self.assert_equal(p.user.pk, user.pk)


class TestT1View(HttpTestCase):
    '''
      ticket:1 view testcase
    '''
    def setup(self):
        user = self.helper('create_user', active=False)
        self.helper('create_profile',
                        user,
                        UserProfile,
                        bio=TEST_DATA['bio'],
                        birthday=TEST_DATA['birthday']
                    )

    def test_index(self):
        self.go200('/')
        self.find('Bio')


class TestRequestLog(HttpTestCase):
    '''
      ticket:3 testcase for RequestLog model/manager and middleware
    '''
    def test_reqs(self):
        self.go('/')
        r = RequestLog.objects.latest('pk')
        self.assertEqual(r.path, '/')


class TestContextProcessor(TestCase):
    '''
      ticket:4 test context processor for settings
    '''

    def test_settings(self):
        from django.template import RequestContext
        from django.test.client import RequestFactory #goodbye @#$% tddspry :)
        from django.conf import settings as django_settings

        factory = RequestFactory()
        request = factory.get('/')
        c = RequestContext(request, {'foo': 'bar'}, [settings_processor])
        self.assertTrue('settings' in c)
        self.assertEquals(c['settings'], django_settings)


class TestEditForm(TestCase):
    '''
      ticket:5 ticket:6 edit form tests
    '''

    fixtures = ['initial_data.json']

    def test_access(self):
        form_edit_url = self.build_url('basicapp:edit_form', args=[1])
        # unauthorized access

        # wtf, why code==200? O_o
        #self.disable_redirect()
        #self.go(form_edit_url)
        #self.code(301)
        self.go(form_edit_url)
        self.url('/accounts/login/\?next=%s' % form_edit_url)

        self.login('admin', 'admin')
        self.go(form_edit_url)
        self.url(form_edit_url)
        self.find('slav0nic@jabber.ru')


class TestTag(TestCase):
    '''
      ticket:8 test edit tag
    '''

    fixtures = ['initial_data.json']

    def test_tag(self):
        user = User.objects.get(pk=1)
        url = admin_change_url(user)
        self.assertEqual(url, '<a href="/admin/auth/user/1/">(admin)</a>')


class TestCommand(TestCase):
    '''
      ticket:9 test `modelscount` command
    '''

    fixtures = ['initial_data.json']

    def test_modelcount(self):
        out = StringIO()
        management.call_command('modelcount', stdout=out)
        res = out.getvalue()
        self.find_in('User:\t1', res)


class TestSignals(TestCase):
    '''
      ticket:10 test signals
    '''

    fixtures = ['initial_data.json']

    def test_modelchanges(self):
        self.login('admin', 'admin')
        self.go('/')
        l = LogEntry.objects.latest('pk')
        r = RequestLog.objects.latest('pk')
        self.assertEqual(r.pk, int(l.object_id))
        self.assertTrue(l.is_addition())
        self.assertFalse(l.is_deletion())
        self.assertFalse(l.is_change())
