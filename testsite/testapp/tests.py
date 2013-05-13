from datetime import datetime
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


class DeactivateMixinTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@foo.com', '123')
        self.test_model = TestModel.objects.create(user=self.user)
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


class FilteredListMixinTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@foo.com', '123')
        TestModel.objects.create(user=self.user, created=datetime(2013, 1, 1))
        TestModel.objects.create(user=self.user, created=datetime(2012, 1, 1))
        TestModel.objects.create(user=self.user, created=datetime(2011, 1, 1))
        TestModel.objects.create(user=self.user, created=datetime(2010, 1, 1), active=False)
        self.client = Client()

    def test_filtered_list(self):
        url = '%s%s' % (reverse('filtered_list'), '?active=True')
        response = self.client.get(url)
        test_models = response.context_data['testmodel_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_models.count(), 3)

    def test_filtered_list_multiple(self):
        url = '%s%s' % (reverse('filtered_list'), '?active=True&created__gte=2012-1-1')
        response = self.client.get(url)
        test_models = response.context_data['testmodel_list']


class HttpCacheMixinTestCase(TestCase):

    def setUp(self):
        pass


class LoginMixinTestCase(TestCase):

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


class ModelFormSetMixinTestCase(TestCase):

    def setUp(self):
        pass


class ObjectOwnerMixinTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('john', 'john@foo.com', '123')
        self.other_user = User.objects.create_user('bob', 'bob@foo.com', '123')
        self.test_model = TestModel.objects.create(user=self.owner)

    def test_object_ownership_get(self):
        url = reverse('object_owner', args=[self.test_model.pk])
        with authenticated_client('john', '123') as owner:
            response = owner.get(url)
            self.assertEqual(response.status_code, 200)

    def test_object_ownership_post(self):
        url = reverse('object_owner', args=[self.test_model.pk])
        with authenticated_client('john', '123') as owner:
            response = owner.post(url)
            self.assertEqual(response.status_code, 200)

    def test_object_not_owner_get(self):
        url = reverse('object_owner', args=[self.test_model.pk])
        with authenticated_client('bob', '123') as owner:
            response = owner.get(url)
            self.assertEqual(response.status_code, 403)

    def test_object_not_owner_post(self):
        url = reverse('object_owner', args=[self.test_model.pk])
        with authenticated_client('bob', '123') as owner:
            response = owner.post(url)
            self.assertEqual(response.status_code, 403)


class OwnershipMixinTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('john', 'john@foo.com', '123')
        self.other_user = User.objects.create_user('bob', 'bob@foo.com', '123')
        self.test_model = TestModel.objects.create(user=self.owner)

    def test_ownership_is_owner(self):
        url = reverse('ownership', args=[self.test_model.pk])
        with authenticated_client('john', '123') as owner:
            response = owner.get(url)
            self.assertEqual(response.status_code, 200)

    def test_ownership_not_owner(self):
        url = reverse('ownership', args=[self.test_model.pk])
        with authenticated_client('bob', '123') as client:
            response = client.get(url)
            self.assertEqual(response.status_code, 403)


class StaffRequiredMixinTestCase(TestCase):

    def setUp(self):
        self.staff_user = User.objects.create_user('staff_john', 'staffjohn@foo.com', '123')
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.user = User.objects.create_user('john', 'john@foo.com', '123')

    def test_staff_required(self):
        url = reverse('staff_required')
        with authenticated_client('staff_john', '123') as staff:
            response = staff.get(url)
            self.assertEqual(response.status_code, 200)

    def test_not_staff_user(self):
        url = reverse('staff_required')
        with authenticated_client('john', '123') as client:
            response = client.get(url)
            self.assertEqual(response.status_code, 403)


class SuperuserRequiredMixinTestCase(TestCase):

    def setUp(self):
        self.super_user = User.objects.create_superuser('super_john', 'superjohn@foo.com', '123')
        self.user = User.objects.create_user('john', 'john@foo.com', '123')

    def test_super_user_required(self):
        url = reverse('superuser_required')
        with authenticated_client('super_john', '123') as super_client:
            response = super_client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_not_super_user(self):
        url = reverse('superuser_required')
        with authenticated_client('john', '123') as client:
            response = client.get(url)
            self.assertEqual(response.status_code, 403)