from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', SuccessView.as_view(), name='success'),
    url(r'^deactivate/(?P<pk>\d+)$', DeactivateView.as_view(), name='deactivate'),
    url(r'^filtered-list/$', FilteredListView.as_view(), name='filtered_list'),
    url(r'^http-cache/$', HttpCacheView.as_view(), name='http_cache'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^model-form-set/$', ModelFormSetView.as_view(), name='model_form_set'),
    url(r'^object-owner/(?P<pk>\d+)$', ObjectOwnerView.as_view(), name='object_owner'),
    url(r'^ownership/(?P<pk>\d+)$', OwnershipView.as_view(), name='ownership'),
    url(r'^staff-required/$', StaffRequiredView.as_view(), name='staff_required'),
    url(r'^superuser-required/$', SuperuserRequiredView.as_view(), name='superuser_required'),
)