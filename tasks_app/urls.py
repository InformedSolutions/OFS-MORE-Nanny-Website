from django.conf import settings
from django.conf.urls import url, include

from tasks_app import views


urlpatterns = [
    url(r'^task-list/', views.TaskListView.as_view(), name='Task-List'),
<<<<<<< HEAD
    url(r'^childcare-address/', views.ChildcareAddressGuidanceView.as_view(), name='Childcare-Address-Guidance'),
    url(r'^first-aid/', views.FirstAidGuidanceView.as_view(), name='First-Aid-Guidance'),
    url(r'^childcare-training/', views.ChildcareTrainingGuidanceView.as_view(), name='Childcare-Training-Guidance'),
=======
    url(r'^personal-details/', views.PersonalDetailsGuidanceView.as_view(), name='Personal-Details-Guidance'),
>>>>>>> develop
    url(r'^criminal-record/', views.CriminalRecordGuidanceView.as_view(), name='Criminal-Record-Guidance'),
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
