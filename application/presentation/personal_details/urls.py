from django.conf.urls import url

from .views import PersonalDetailNameView, PersonalDetailDOBView, PersonalDetailHomeAddressView, \
    PersonalDetailSelectAddressView, PersonalDetailManualAddressView, PersonalDetailSummaryAddressView, \
    PersonalDetailsYourChildrenView, Summary

urlpatterns = [
    url(r'^personal-details/your-name/', PersonalDetailNameView.as_view(), name='Personal-Details-Name'),
    url(r'^personal-details/your-date-of-birth/', PersonalDetailDOBView.as_view(), name='Personal-Details-Date-Of-Birth'),
    url(r'^personal-details/your-home-address/', PersonalDetailHomeAddressView.as_view(), name='Personal-Details-Home-Address'),
    url(r'^personal-details/select-home-address/', PersonalDetailSelectAddressView.as_view(), name='Personal-Details-Select-Address'),
    url(r'^personal-details/enter-home-address/', PersonalDetailManualAddressView.as_view(), name='Personal-Details-Manual-Address'),
    url(r'^personal-details/home-address-details/', PersonalDetailSummaryAddressView.as_view(), name='Personal-Details-Address-Summary'),
    url(r'^personal-details/your-children/', PersonalDetailsYourChildrenView.as_view(), name='Personal-Details-Your-Children'),
    url(r'^personal-details/check-answers/', Summary.as_view(), name='Personal-Details-Summary')
]
