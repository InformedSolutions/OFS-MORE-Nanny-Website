from django.conf.urls import include, url


urlpatterns = [
    url('', include('login_app.urls')),
]
