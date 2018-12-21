from django.conf.urls import url

from application.presentation.childcare_address import views


urlpatterns = [
    url(r'^service-unavailable/', views.ServiceUnavailableView.as_view(), name='Service-Unavailable'),
    url(r'^childcare-address/where-you-work/', views.WhereYouWorkView.as_view(), name='Childcare-Address-Where-You-Work'),
    url(r'^childcare-address/details-later/', views.AddressDetailsLaterView.as_view(), name='Childcare-Address-Details-Later'),
    url(r'^childcare-address/childcare-location/', views.ChildcareLocationView.as_view(), name='Childcare-Address-Location'),
    url(r'^childcare-address-postcode/', views.ChildcareAddressPostcodeView.as_view(), name='Childcare-Address-Postcode-Entry'),
    url(r'^select-childcare-address/', views.ChildcareAddressLookupView.as_view(), name='Childcare-Address-Lookup'),
    url(r'^enter-childcare-address/', views.ChildcareAddressManualView.as_view(), name='Childcare-Address-Manual-Entry'),
    url(r'^childcare-address/details/', views.ChildcareAddressDetailsView.as_view(), name='Childcare-Address-Details'),
    url(r'^childcare-address/check-answers/', views.ChildcareAddressSummaryView.as_view(), name='Childcare-Address-Summary'),
    url(r'^childcare-address/', views.GuidanceView.as_view(), name='Childcare-Address-Guidance')
]
