from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView
from viewclass_mixins.views import DeactivateMixin, FilteredListMixin, HttpCacheMixin, LoginMixin, ModelFormSetMixin,\
    ObjectOwnerMixin, OwnershipMixin, StaffRequiredMixin, SuperuserRequiredMixin


class DeactivateView(DeleteView, DeactivateMixin):
    template_name = "home.html"


class FilteredListView(ListView, FilteredListMixin):
    template_name = "home.html"


class HttpCacheView(TemplateView, HttpCacheMixin):
    template_name = "home.html"


class LoginView(TemplateView, LoginMixin):
    template_name = "home.html"


class ModelFormSetView(CreateView, ModelFormSetMixin):
    template_name = "home.html"


class ObjectOwnerView(TemplateView, ObjectOwnerMixin):
    template_name = "home.html"


class OwnershipView(DetailView, OwnershipMixin):
    template_name = "home.html"


class StaffRequiredView(TemplateView, StaffRequiredMixin):
    template_name = "home.html"


class SuperuserRequiredView(TemplateView, SuperuserRequiredMixin):
    template_name = "home.html"