from django.conf import settings
from django.conf.urls import url, include

from login_app import views


urlpatterns = [
    url(r'^service-unavailable/', views.ServiceUnavailableView.as_view(), name='Service-Unavailable'),
    url(r'^sign-in/new-application/', views.AccountSelectionFormView.as_view(), name='Account-Selection'),
    url(r'^new-application/$', views.NewUserSignInFormView.as_view(), name='New-User-Sign-In'),
    url(r'^new-application/check-email/', views.CheckEmailView.as_view(), name='Check-New-Email'),
    url(r'^sign-in/check-email/', views.CheckEmailView.as_view(), name='Check-Existing-Email'),
    url(r'^email-resent/', views.ResendEmail.as_view(), name='Resend-Email'),
    url(r'^sign-in/', views.ExistingUserSignIn.as_view(), name='Existing-User-Sign-In')
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
