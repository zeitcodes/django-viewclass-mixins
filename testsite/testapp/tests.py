from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from models import Author


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
        self.test_model = Author.objects.create(user=self.user)
        self.client = Client()

    def test_deactivation_get(self):
        url = reverse('deactivate', args=[self.test_model.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Author.objects.get(pk=self.test_model.pk).active)

    def test_deactivation_post(self):
        url = reverse('deactivate', args=[self.test_model.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.filter(pk=self.test_model.pk).exists())
        self.assertFalse(Author.objects.get(pk=self.test_model.pk).active)


class FilteredListMixinTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@foo.com', '123')
        Author.objects.create(user=self.user, created=datetime(2013, 1, 1))
        Author.objects.create(user=self.user, created=datetime(2012, 1, 1))
        Author.objects.create(user=self.user, created=datetime(2011, 1, 1))
        Author.objects.create(user=self.user, created=datetime(2010, 1, 1), active=False)
        self.client = Client()

    def test_filtered_list(self):
        url = '%s%s' % (reverse('filtered_list'), '?active=True')
        response = self.client.get(url)
        test_models = response.context_data['author_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_models.count(), 3)

    def test_filtered_list_multiple(self):
        url = '%s%s' % (reverse('filtered_list'), '?active=1&created__gte=2012-1-1')
        response = self.client.get(url)
        test_models = response.context_data['author_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_models.count(), 2)

    def test_filtered_list_ignores(self):
        url = '%s%s' % (reverse('filtered_list'), '?random=1')
        response = self.client.get(url)
        test_models = response.context_data['author_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_models.count(), 4)


class HttpCacheMixinTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_http_cache_last_modified(self):
        url = reverse('http_cache_last_modified')
        response = self.client.get(url)
        self.assertEqual(response.get('last-modified'), datetime(2000, 1, 1).strftime('%Y-%m-%d %H:%M:%S'))

    def test_http_cache_varies(self):
        url = reverse('http_cache_varies')
        response = self.client.get(url)
        self.assertEqual(response.get('vary'), 'Vary')

    def test_http_cache_timeout(self):
        url = reverse('http_cache_timeout')
        response = self.client.get(url)
        self.assertEqual(response.get('cache-control'), 'max-age=300')

    def test_http_cache_etag(self):
        url = reverse('http_cache_etag')
        response = self.client.get(url)
        self.assertEqual(response.get('etag'), 'etag_hash')


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
        self.user = User.objects.create_user('john', 'john@foo.com', '123', pk=1)
        self.author = Author.objects.create(user=self.user)
        self.client = Client()

    def test_model_form_set_get(self):
        url = reverse('model_form_set')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_model_form_set_post(self):
        field_info = {
            'name': 'John',
            'book_set-TOTAL_FORMS': 1,
            'book_set-INITIAL_FORMS': 0,
            'book_set-MAX_NUM_FORMS': 1000,
            'book_set-0-title': 'Title',
            'book_set-0-created': datetime.now(),
        }
        url = reverse('model_form_set')
        response = self.client.post(url, field_info)
        self.assertEqual(response.status_code, 302)


class ObjectOwnerMixinTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('john', 'john@foo.com', '123')
        self.other_user = User.objects.create_user('bob', 'bob@foo.com', '123')
        self.test_model = Author.objects.create(user=self.owner)

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
        self.test_model = Author.objects.create(user=self.owner)

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