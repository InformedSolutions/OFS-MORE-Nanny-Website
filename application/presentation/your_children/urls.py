from django.conf.urls import url

from .views import YourChildrenGuidanceView
from .views.your_children_address import *
from .views.your_children_addresses import YourChildrenAddressesView
from .views.your_children_details import YourChildrenDetailsView
from .views.your_children_summary import YourChildrenSummaryView

urlpatterns = [
    url(r'^your-children/$', YourChildrenGuidanceView.as_view(), name='Your-Children-Guidance'),
    url(r'^your-children-details/', YourChildrenDetailsView.as_view(), name='Your-Children-Details'),
    url(r'^your-children/addresses/', YourChildrenAddressesView.as_view(), name='Your-Children-addresses'),
    url(r'^your-children/address/', YourChildrenPostcodeView.as_view(), name='Your-Children-Postcode'),
    url(r'^your-children/address-selection/', YourChildrenAddressSelectionView.as_view(), name='Your-Children-Address-Selection'),
    url(r'^your-children/enter-address/', YourChildrenManualAddressView.as_view(), name='Your-Children-Manual-address'),
    url(r'^your-children/check-answers/', YourChildrenSummaryView.as_view(), name='Your-Children-Summary'),
]
