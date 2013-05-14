from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from forms import AuthorForm, BookForm, BookFormSet
from models import Author, Book
from viewclass_mixins.views import DeactivateMixin, FilteredListMixin, HttpCacheMixin, LoginMixin, ModelFormSetMixin,\
    ObjectOwnerMixin, OwnershipMixin, StaffRequiredMixin, SuperuserRequiredMixin


class SuccessView(TemplateView):
    template_name = 'home.html'


class DeactivateView(DeactivateMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('success')
    template_name = 'home.html'


class FilteredListView(FilteredListMixin, ListView):
    model = Author
    template_name = "home.html"


class HttpCacheView(HttpCacheMixin, TemplateView):
    template_name = "home.html"


class LoginView(LoginMixin, TemplateView):
    template_name = "home.html"


class ModelFormSetView(ModelFormSetMixin, CreateView):
    model = Author
    form_class = AuthorForm
    formset_classes = [BookFormSet]
    template_name = "model_form.html"


class ObjectOwnerView(ObjectOwnerMixin, UpdateView):
    model = Author
    owner_model = Author
    owner_field = 'user'
    template_name = "home.html"


class OwnershipView(OwnershipMixin, DetailView):
    model = Author
    template_name = "home.html"


class StaffRequiredView(StaffRequiredMixin, TemplateView):
    template_name = "home.html"


class SuperuserRequiredView(SuperuserRequiredMixin, TemplateView):
    template_name = "home.html"