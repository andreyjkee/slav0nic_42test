#coding: utf-8
from datetime import datetime
from tddspry.django import DatabaseTestCase, HttpTestCase, TestCase

from basicapp.models import UserProfile, RequestLog
from basicapp.context_processors import settings_processor


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
