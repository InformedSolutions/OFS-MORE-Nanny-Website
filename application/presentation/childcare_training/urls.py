from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^childcare-training/$', views.ChildcareTrainingGuidanceView.as_view(), name='Childcare-Training-Guidance'),
    url(r'^childcare-training/type/', views.TypeOfChildcareTrainingFormView.as_view(), name='Type-Of-Childcare-Training'),
    url(r'^childcare-training/check-answers/', views.ChildcareTrainingSummaryView.as_view(), name='Childcare-Training-Summary'),
    url(r'^childcare-training-course/', views.ChildcareTrainingCourseView.as_view(), name='Childcare-Training-Course'),
    url(r'^childcare-training-certificate/', views.ChildcareTrainingCertificateView.as_view(), name='Childcare-Training-Certificate'),
]
