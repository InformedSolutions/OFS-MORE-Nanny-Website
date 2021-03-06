from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^your-details/', CapitaDBSDetailsFormView.as_view(), name='Capita-DBS-Details-View'),
    url(r'^post-certificate/', PostDBSCertificateView.as_view(), name='Post-DBS-Certificate'),
    url(r'^check-answers/', CriminalRecordChecksSummaryView.as_view(), name='Criminal-Record-Check-Summary-View'),
    url(r'^$', CriminalRecordsCheckGuidanceView.as_view(), name='Criminal-Record-Checks-Guidance-View'),
    url(r'^lived-abroad/', LivedAbroadFormView.as_view(), name='Lived-Abroad-View'),
    url(r'^UK/', DBSGuidanceView.as_view(), name='DBS-Guidance-View'),
    url(r'^DBS-check-type/', DBSTypeFormView.as_view(), name='DBS-Type-View'),
    url(r'^DBS-details/', NonCapitaDBSDetailsFormView.as_view(), name='Non-Capita-DBS-Details-View'),
    url(r'^update/', DBSUpdateServiceFormView.as_view(), name='DBS-Update-Service-Page'),
    url(r'^abroad/', CriminalRecordsFromAbroadView.as_view(), name='Criminal-Records-Abroad-View'),
    url(r'^email-certificates/', EmailGoodConductCertificatesView.as_view(),
        name='Email-Good-Conduct-Certificates-View'),
    url(r'^apply-new/', DBSApplyView.as_view(),
        name='DBS-Apply-View'),
    url(r'^DBS-update-check/', DBSUpdateCheckView.as_view(),
        name='DBS-Update-Check-View'),
    url(r'^sign-up-update/', DBSSignUpView.as_view(),
        name='DBS-Sign-Up-View'),
]
