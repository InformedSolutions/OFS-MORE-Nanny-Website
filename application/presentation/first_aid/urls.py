from django.conf.urls import url

from .views import Guidance, FirstAidDetailsView, Declaration, Summary

urlpatterns = [
    url(r'^first-aid-training/', Guidance.as_view(), name='First-Aid-Guidance'),
    url(r'^first-aid/details/', FirstAidDetailsView.as_view(), name='Training-Details'),
    url(r'^first-aid/certificate/', Declaration.as_view(), name='First-Aid-Declaration'),
    url(r'^first-aid/check-answers/', Summary.as_view(), name='First-Aid-Summary'),
]
