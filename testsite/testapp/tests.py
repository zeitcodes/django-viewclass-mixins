from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class DeactivateMixinTest(TestCase):

    def setUp(self):
        pass


class FilteredListMixinTest(TestCase):

    def setUp(self):
        pass


class HttpCacheMixinTest(TestCase):

    def setUp(self):
        pass


class LoginMixinTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@foo.com', '123')
        self.client = Client()
        self.client.login(username='john', password='123')

    def test_logged_in(self):
        url = reverse('login')

    def test_logged_out(self):
        pass


class ModelFormSetMixinTest(TestCase):

    def setUp(self):
        pass


class ObjectOwnerTest(TestCase):

    def setUp(self):
        pass


class OwnershipMixinTest(TestCase):

    def setUp(self):
        pass


class StaffRequiredMixinTest(TestCase):

    def setUp(self):
        pass


class SuperuserRequiredMixin(TestCase):

    def setUp(self):
        pass