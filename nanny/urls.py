from django.conf.urls import include, url
from django.conf import settings

import re


urlpatterns = [
    url(r'^', include('login_app.urls')),
    url(r'^', include('tasks_app.urls')),
    url(r'^', include('personal_details_app.urls', namespace="personal-details")),
    url(r'^', include('childcare_address_app.urls')),
    url(r'^', include('childcare_training_task_app.urls')),
    url(r'^first-aid/', include('first_aid_app.urls', namespace='first-aid')),
]

if hasattr(settings, 'URL_PREFIX'):
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
