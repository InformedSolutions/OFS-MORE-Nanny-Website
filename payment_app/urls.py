from django.conf import settings
from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^payment/details/', card_payment_details, name='payment-details'),
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
