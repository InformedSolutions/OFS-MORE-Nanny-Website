from django.conf.urls import url

from .views import feedback

urlpatterns = [
    url(r'^feedback/', feedback.feedback, name='Feedback'),
    url(r'^feedback-submitted/', feedback.feedback_confirmation, name='Feedback-Confirmation')
]