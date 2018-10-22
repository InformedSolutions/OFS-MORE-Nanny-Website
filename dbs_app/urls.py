from django.conf import settings
from django.conf.urls import url, include

from dbs_app.views import *

urlpatterns = [
    url(r'^your-details/', CapitaDBSDetailsFormView.as_view(), name='Capita-DBS-Details-View'),
    url(r'^post-certificate/', PostDBSCertificateView.as_view(), name='Post-DBS-Certificate'),
    url(r'^check-answers/', CriminalRecordChecksSummaryView.as_view(), name='Criminal-Record-Check-Summary-View'),
    url(r'^$', CriminalRecordsCheckGuidanceView.as_view(), name='Criminal-Record-Checks-Guidance-View'),
    url(r'^lived-abroad/', LivedAbroadFormView.as_view(), name='Lived-Abroad-View'),
    url(r'^UK/', DBSGuidanceView.as_view(), name='DBS-Guidance-View'),
    url(r'^type/', DBSTypeFormView.as_view(), name='DBS-Type-View'),
    url(r'^DBS-details/', NonCapitaDBSDetailsFormView.as_view(), name='Non-Capita-DBS-Details-View'),
    url(r'^update/', DBSUpdateServiceFormView.as_view(), name='DBS-Update-Service-Page')
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
