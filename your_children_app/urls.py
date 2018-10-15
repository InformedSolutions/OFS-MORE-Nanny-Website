from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import YourChildrenGuidance

urlpatterns = [
    url(r'^your_children/your_children/', YourChildrenGuidance.as_view(), name='Your-Children-Guidance'),

]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
