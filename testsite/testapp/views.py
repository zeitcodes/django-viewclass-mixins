from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from forms import AuthorForm, BookForm, BookFormSet
from models import Author, Book
from viewclass_mixins.views import *


class SuccessView(TemplateView):
    template_name = 'home.html'


class DeactivateView(DeactivateMixin, DeleteView):
    model = Author
    template_name = 'home.html'
    success_url = reverse_lazy('success')


class FilteredListView(FilteredListMixin, ListView):
    model = Author
    template_name = 'home.html'


class HttpCacheLastModifiedView(HttpCacheMixin, TemplateView):
    template_name = 'home.html'

    def get_last_modified(self):
        return datetime(2000, 1, 1)


class HttpCacheVariesView(HttpCacheMixin, TemplateView):
    cache_varies = ['Vary']
    template_name = 'home.html'


class HttpCacheTimeoutView(HttpCacheMixin, TemplateView):
    cache_timeout = 300
    template_name = 'home.html'


class HttpCacheETagView(HttpCacheMixin, TemplateView):
    template_name = 'home.html'

    def get_etag(self, ):
        return 'etag_hash'


class LoginView(LoginMixin, TemplateView):
    template_name = 'home.html'


class ModelFormSetView(ModelFormSetMixin, CreateView):
    model = Author
    form_class = AuthorForm
    formset_classes = [BookFormSet]
    template_name = 'model_form.html'
    success_url = reverse_lazy('success')


class ObjectOwnerView(ObjectOwnerMixin, UpdateView):
    model = Author
    owner_model = Author
    owner_field = 'user'
    template_name = 'home.html'


class OwnershipView(OwnershipMixin, DetailView):
    model = Author
    template_name = 'home.html'


class StaffRequiredView(StaffRequiredMixin, TemplateView):
    template_name = 'home.html'


class SuperuserRequiredView(SuperuserRequiredMixin, TemplateView):
    template_name = 'home.html'