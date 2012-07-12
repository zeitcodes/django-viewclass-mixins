from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class FilteredListMixin(object):
    def filtered_queryset(self, request):
        queryset = self.get_queryset()
        if 'search' in request.GET:
            queryset = queryset.search(request.GET['search'])
        filters = {}
        field_names = queryset.model._meta.get_all_field_names()
        for field, value in request.GET.items():
            field_name = field.split('__')[0]
            if field_name in field_names:
                filters[field] = value
        queryset = queryset.filter(**filters)
        return queryset

    def get(self, request, *args, **kwargs):
        self.queryset = self.filtered_queryset(request)
        return super(FilteredListMixin, self).get(request, *args, **kwargs)


class LoginMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginMixin, self).dispatch(*args, **kwargs)


class DeactivateMixin(object):
    deactivation_field = 'active'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        setattr(self.object, self.deactivation_field, False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
