from django.conf.urls import include, url
from django.conf import settings

import re

from .presentation import childcare_address, \
    childcare_training, \
    dbs, \
    declaration, \
    first_aid, \
    insurance_cover, \
    login, \
    payment, \
    personal_details, \
    task_list, \
    feedback

urlpatterns = [
    url(r'^', include(childcare_address.urlpatterns)),
    url(r'^', include(task_list.urlpatterns)),
    url(r'^', include((personal_details.urlpatterns, "personal-details"), namespace="personal-details")),
    url(r'^', include(login.urlpatterns)),
    url(r'^', include(childcare_training.urlpatterns)),
    url(r'^', include((payment.urlpatterns, "payment"), namespace="payment")),
    url(r'^', include((declaration.urlpatterns, "declaration"), namespace="declaration")),
    url(r'^', include((first_aid.urlpatterns, "first-aid"), namespace='first-aid')),
    url(r'^insurance/', include((insurance_cover.urlpatterns, "insurance"), namespace='insurance')),
    url(r'^criminal-record/', include((dbs.urlpatterns, "dbs"), namespace='dbs')),
    url(r'^', include(feedback.urlpatterns))
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
