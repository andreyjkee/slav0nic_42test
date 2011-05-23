#coding: utf-8
from datetime import datetime
from tddspry.django import DatabaseTestCase, HttpTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from basicapp.models import UserProfile


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
        uprofile = self.helper('create_profile',
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
        uprofile = self.helper('create_profile',
                               user,
                               UserProfile,
                               bio=TEST_DATA['bio'],
                               birthday=TEST_DATA['birthday']
                               )

    def test_index(self):
        self.go200('/')
        self.find('Bio')
