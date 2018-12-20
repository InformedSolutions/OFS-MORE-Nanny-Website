from django.conf import settings
from django.conf.urls import url, include

from first_aid_app.views import Guidance, FirstAidDetailsView, Declaration, Summary

urlpatterns = [
    url(r'^first-aid-training/', Guidance.as_view(), name='First-Aid-Guidance'),
    url(r'^first-aid/details/', FirstAidDetailsView.as_view(), name='Training-Details'),
    url(r'^first-aid/certificate/', Declaration.as_view(), name='First-Aid-Declaration'),
    url(r'^first-aid/check-answers/', Summary.as_view(), name='First-Aid-Summary'),
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
