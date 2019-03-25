from django.conf.urls import url

from .views import Guidance, FirstAidDetailsView, Declaration, Summary, RenewFirstAid

urlpatterns = [
    url(r'^first-aid-training/', Guidance.as_view(), name='First-Aid-Guidance'),
    url(r'^first-aid/details/', FirstAidDetailsView.as_view(), name='Training-Details'),
    url(r'^first-aid/certificate/', Declaration.as_view(), name='First-Aid-Declaration'),
    url(r'^first-aid/check-answers/', Summary.as_view(), name='First-Aid-Summary'),
    url(r'^first-aid/renew/', RenewFirstAid.as_view(), name='First-Aid-Renew')
]
