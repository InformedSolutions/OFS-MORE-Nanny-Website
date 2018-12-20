from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import PersonalDetailNameView, PersonalDetailDOBView, PersonalDetailHomeAddressView, \
    PersonalDetailSelectAddressView, PersonalDetailManualAddressView, PersonalDetailSummaryAddressView, \
    PersonalDetailLivedAbroadView, PersonalDetailCertificateView, PersonalDetailsPostCertificateView, \
    PersonalDetailsYourChildrenView, Summary

urlpatterns = [
    url(r'^personal-details/your-name/', PersonalDetailNameView.as_view(), name='Personal-Details-Name'),
    url(r'^personal-details/your-date-of-birth/', PersonalDetailDOBView.as_view(), name='Personal-Details-Date-Of-Birth'),
    url(r'^personal-details/your-home-address/', PersonalDetailHomeAddressView.as_view(), name='Personal-Details-Home-Address'),
    url(r'^personal-details/select-home-address/', PersonalDetailSelectAddressView.as_view(), name='Personal-Details-Select-Address'),
    url(r'^personal-details/enter-home-address/', PersonalDetailManualAddressView.as_view(), name='Personal-Details-Manual-Address'),
    url(r'^personal-details/home-address-details/', PersonalDetailSummaryAddressView.as_view(), name='Personal-Details-Address-Summary'),
    url(r'^personal-details/lived-abroad/', PersonalDetailLivedAbroadView.as_view(), name='Personal-Details-Lived-Abroad'),
    url(r'^personal-details/good-conduct-certificates/', PersonalDetailCertificateView.as_view(),
        name='Personal-Details-Certificates-Of-Good-Conduct'),
    url(r'^personal-details/post-certificates/', PersonalDetailsPostCertificateView.as_view(), name='Personal-Details-Post-Certificates'),
    url(r'^personal-details/your-children/', PersonalDetailsYourChildrenView.as_view(), name='Personal-Details-Your-Children'),
    url(r'^personal-details/check-answers/', Summary.as_view(), name='Personal-Details-Summary')
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
