from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^task-list/', TaskListView.as_view(), name='Task-List'),
    url(r'cancel-application/', CancelApplicationTemplateView.as_view(), name='Cancel-Application'),
    url(r'application-cancelled/', ApplicationCancelledTemplateView.as_view(), name='Application-Cancelled'),
    url(r'^insurance-cover/', InsuranceCoverGuidanceView.as_view(), name='Insurance-Cover-Guidance'),
    # url(r'^first-aid-training/', FirstAidGuidanceView.as_view(), name='First-Aid-Guidance'),
    url(r'^costs/', CostsView.as_view(), name='Costs'),
    url(r'^help-contacts/', HelpAndContactView.as_view(), name='Help-And-Contact'),

]
