from django.conf import settings
from django.urls import path, re_path, include

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('simple_form', simple_form, name='simple_form'),
    path('long_form', long_form, name='long_form'),
    path('fieldset_form', fieldset_form, name='fieldset_form'),
    path('revealing_form', revealing_form, name='revealing_form')
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

