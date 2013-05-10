from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from models import TestModel


class authenticated_client(object):
    def __init__(self, username, password):
        self.client = Client()
        self.username = username
        self.password = password

    def __enter__(self):
        self.client.login(username=self.username, password=self.password)
        return self.client

    def __exit__(self, type, value, traceback):
        self.client.logout()


class DeactivateMixinTest(TestCase):

    def setUp(self):
        self.test_model = TestModel.objects.create()
        self.client = Client()

    def test_deactivation_get(self):
        url = reverse('deactivate', args=[self.test_model.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TestModel.objects.get(pk=self.test_model.pk).active)

    def test_deactivation_post(self):
        url = reverse('deactivate', args=[self.test_model.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TestModel.objects.filter(pk=self.test_model.pk).exists())
        self.assertFalse(TestModel.objects.get(pk=self.test_model.pk).active)


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

    def test_logged_in(self):
        url = reverse('login')
        with authenticated_client('john', '123') as client:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_logged_out(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


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