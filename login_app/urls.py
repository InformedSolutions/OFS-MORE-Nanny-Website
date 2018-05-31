from django.conf import settings
from django.conf.urls import url, include

from login_app import views


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^simple_form/', views.simple_form, name='simple_form'),
    # url(r'^long_form/', views.long_form, name='long_form'),
    # url(r'^fieldset_form/', views.fieldset_form, name='fieldset_form'),
    # url(r'^revealing_form/', views.revealing_form, name='revealing_form')
    url(r'service-unavailable/', views.ServiceUnavailableView.as_view(), name="Service-Unavailable"),
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
