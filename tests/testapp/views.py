from .forms import AuthorForm, BookFormSet
from .models import Author
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from viewclass_mixins.views import (
    FilteredListMixin,
    LoginMixin,
    StaffRequiredMixin,
    SuperuserRequiredMixin,
    OwnershipMixin,
    ObjectOwnerMixin,
    DeactivateMixin,
    ModelFormSetMixin,
    HttpCacheMixin,
)


class SuccessView(TemplateView):
    template_name = 'base.html'


class DeactivateView(DeactivateMixin, DeleteView):
    model = Author
    template_name = 'base.html'
    success_url = reverse_lazy('success')


class FilteredListView(FilteredListMixin, ListView):
    model = Author
    template_name = 'base.html'


class HttpCacheLastModifiedView(HttpCacheMixin, TemplateView):
    template_name = 'base.html'

    def get_last_modified(self):
        return datetime(2000, 1, 1)


class HttpCacheVariesView(HttpCacheMixin, TemplateView):
    cache_varies = ['Vary']
    template_name = 'base.html'


class HttpCacheTimeoutView(HttpCacheMixin, TemplateView):
    cache_timeout = 300
    template_name = 'base.html'


class HttpCacheETagView(HttpCacheMixin, TemplateView):
    template_name = 'base.html'

    def get_etag(self, ):
        return 'etag_hash'


class LoginView(LoginMixin, TemplateView):
    template_name = 'base.html'


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
    template_name = 'base.html'


class OwnershipView(OwnershipMixin, DetailView):
    model = Author
    template_name = 'base.html'


class StaffRequiredView(StaffRequiredMixin, TemplateView):
    template_name = 'base.html'


class SuperuserRequiredView(SuperuserRequiredMixin, TemplateView):
    template_name = 'base.html'
