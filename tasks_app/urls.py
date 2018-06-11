from django.conf import settings
from django.conf.urls import url, include

from tasks_app import views


urlpatterns = [
    url(r'task-list/', views.TaskListView.as_view(), name='Task-List'),
    url(r'personal-details/', views.PersonalDetailsIntroView.as_view(), name='Personal-Details-Intro')
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
