from django.conf.urls import include, url
from django.conf import settings

import re

from application.presentation import childcare_address, \
    childcare_training, \
    dbs, \
    declaration, \
    first_aid, \
    insurance_cover, \
    login, \
    payment, \
    personal_details, \
    task_list, \
    your_children


urlpatterns = [
    url(r'^', include(childcare_address.urlpatterns)),
    url(r'^', include(task_list.urlpatterns)),
    url(r'^', include(personal_details.urlpatterns, namespace="personal-details")),
    url(r'^', include(login.urlpatterns)),
    url(r'^', include(your_children.urlpatterns, namespace='your-children')),
    url(r'^', include(childcare_training.urlpatterns)),
    url(r'^', include(payment.urlpatterns, namespace="payment")),
    url(r'^', include(declaration.urlpatterns, namespace="declaration")),
    url(r'^', include(first_aid.urlpatterns, namespace='first-aid')),
    url(r'^insurance/', include(insurance_cover.urlpatterns, namespace='insurance')),
    url(r'^criminal-record/', include(dbs.urlpatterns, namespace='dbs')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
