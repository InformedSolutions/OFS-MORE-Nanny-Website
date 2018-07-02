from django.conf import settings
from django.conf.urls import url, include

from dbs_app.views import DBSDetailsView, DBSUpload, DBSGuidance, DBSSummary

urlpatterns = [
    url(r'^your-details/', DBSDetailsView.as_view(), name='Details'),
    url(r'^post-certificate/', DBSUpload.as_view(), name='DBS-Upload'),
    url(r'^check-answers/', DBSSummary.as_view(), name='Summary'),
    url(r'^', DBSGuidance.as_view(), name='Guidance')
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
