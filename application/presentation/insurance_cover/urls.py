from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^public-liability', PublicLiabilityView.as_view(), name='Public-Liability'),
    url(r'^get-insurance', InsuranceCoverView.as_view(), name='Insurance-Cover'),
    url(r'^check-answers', SummaryView.as_view(), name='Summary'),
    url(r'^', GuidanceView.as_view(), name='Guidance'),
]
