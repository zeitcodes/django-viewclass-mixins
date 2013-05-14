from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from forms import TestModelForm, OtherTestModelForm
from models import TestModel, OtherTestModel
from viewclass_mixins.views import DeactivateMixin, FilteredListMixin, HttpCacheMixin, LoginMixin, ModelFormSetMixin,\
    ObjectOwnerMixin, OwnershipMixin, StaffRequiredMixin, SuperuserRequiredMixin


class SuccessView(TemplateView):
    template_name = 'home.html'


class DeactivateView(DeactivateMixin, DeleteView):
    model = TestModel
    success_url = reverse_lazy('success')
    template_name = 'home.html'


class FilteredListView(FilteredListMixin, ListView):
    model = TestModel
    template_name = "home.html"


class HttpCacheView(HttpCacheMixin, TemplateView):
    template_name = "home.html"


class LoginView(LoginMixin, TemplateView):
    template_name = "home.html"


class ModelFormSetView(ModelFormSetMixin, CreateView):
    model = TestModel
    formset_classes = [TestModelForm, OtherTestModelForm]
    template_name = "home.html"


class ObjectOwnerView(ObjectOwnerMixin, UpdateView):
    model = TestModel
    owner_model = TestModel
    owner_field = 'user'
    template_name = "home.html"


class OwnershipView(OwnershipMixin, DetailView):
    model = TestModel
    template_name = "home.html"


class StaffRequiredView(StaffRequiredMixin, TemplateView):
    template_name = "home.html"


class SuperuserRequiredView(SuperuserRequiredMixin, TemplateView):
    template_name = "home.html"