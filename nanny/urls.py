from django.conf.urls import include, url
from django.conf import settings

import re

from application.presentation import base_views

urlpatterns = [
    url(r'^', include('application.urls')),
]


if hasattr(settings, 'URL_PREFIX'):
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern

handler500 = base_views.error_500