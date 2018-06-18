from django.conf import settings
from django.conf.urls import url, include

from childcare_training_task_app import views


urlpatterns = [
    url(r'^childcare-training/', views.ChildcareTrainingGuidanceView.as_view(), name='Childcare-Training-Guidance'),
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
