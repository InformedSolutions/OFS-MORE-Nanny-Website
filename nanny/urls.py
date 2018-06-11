from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('login_app.urls')),
    url(r'^', include('tasks_app.urls')),
]
