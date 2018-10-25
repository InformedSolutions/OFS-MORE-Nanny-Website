from django.conf import settings
from django.conf.urls import url, include

from your_children_app.views import YourChildrenGuidanceView
from your_children_app.views.your_children_address import *
from your_children_app.views.your_children_addresses import YourChildrenAddressesView
from your_children_app.views.your_children_details import YourChildrenDetailsView
from your_children_app.views.your_children_summary import YourChildrenSummaryView

urlpatterns = [
    url(r'^your-children/your-children/', YourChildrenGuidanceView.as_view(), name='Your-Children-Guidance'),
    url(r'^your-children-details/', YourChildrenDetailsView.as_view(), name='Your-Children-Details'),
    url(r'^your-children/addresses/', YourChildrenAddressesView.as_view(), name='Your-Children-addresses'),
    url(r'^your-children/address/', YourChildrenAddressView.as_view(), name='Your-Children-address'),
    url(r'^your-children/address-selection/', YourChildrenAddressLookupView.as_view(), name='Your-Children-address-lookup'),
    url(r'^your-children/enter-address/', YourChildrenManualAddressView.as_view(), name='Your-Children-Manual-address'),
    url(r'^your-children/check-answers/', YourChildrenSummaryView.as_view(), name='Your-Children-Summary'),
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
