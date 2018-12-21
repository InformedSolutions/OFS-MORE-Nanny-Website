from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^payment/details/', card_payment_details, name='payment-details'),
]
