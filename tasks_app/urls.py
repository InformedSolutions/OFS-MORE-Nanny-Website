from django.conf import settings
from django.conf.urls import url, include

from tasks_app import views


urlpatterns = [
    url(r'^task-list/', views.TaskListView.as_view(), name='Task-List'),
    url(r'^insurance-cover/', views.InsuranceCoverGuidanceView.as_view(), name='Insurance-Cover-Guidance'),
    url(r'^declaration-summary/', views.DeclarationSummaryView.as_view(), name='Declaration-Summary'),
    url(r'^first-aid-training/', views.FirstAidGuidanceView.as_view(), name='First-Aid-Guidance'),

]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
