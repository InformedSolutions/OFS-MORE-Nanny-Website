from django.conf import settings
from django.conf.urls import url, include

from login_app import views


urlpatterns = [
    url(r'^register-as-nanny/', views.StartPageView.as_view(), name='Start-Page'),
    url(r'^service-unavailable/', views.ServiceUnavailableView.as_view(), name='Service-Unavailable'),
    url(r'^sign-in/new-application/', views.AccountSelectionFormView.as_view(), name='Account-Selection'),
    url(r'^new-application/$', views.NewUserSignInFormView.as_view(), name='New-User-Sign-In'),
    url(r'^new-application/check-email/', views.CheckEmailView.as_view(), name='Check-New-Email'),
    url(r'^sign-in/check-email/', views.CheckEmailView.as_view(), name='Check-Existing-Email'),
    url(r'^email-resent/', views.ResendEmail.as_view(), name='Resend-Email'),
    url(r'^sign-in/$', views.ExistingUserSignInFormView.as_view(), name='Existing-User-Sign-In'),
    url(r'^security-code/', views.SecurityCodeFormView.as_view(), name='Security-Code'),
    url(r'^link-used/', views.LinkUsedView.as_view(), name='Link-Used'),
    url(r'^application-saved/', views.ApplicationSavedView.as_view(), name='Application-Saved'),
    url(r'^phone-number/', views.PhoneNumbersFormView.as_view(), name='Phone-Number'),
    url(r'^resend-code/', views.ResendSecurityCodeView.as_view(), name='Resend-Security-Code'),
    url(r'^sign-in/question/', views.SecurityQuestionFormView.as_view(), name='Security-Question'),
    url(r'^sign-in/check-answers/', views.ContactDetailsSummaryView.as_view(), name='Contact-Details-Summary'),
    url(r'^validate/(?P<id>[\w-]+)/$', views.ValidateMagicLinkView.as_view(), name='Validate-Magic-Link'),
    url(r'^help-contact/$', views.HelpAndContactsView.as_view(), name='Help-And-Contacts'),
    url(r'^sign-in/change-email/$', views.ChangeEmailTemplateView.as_view(), name='Change-Email'),
    url(r'^sign-in/check-email-change/$', views.CheckEmailView.as_view(), name='Check-Change-Email'),
    url(r'^sign-in/change-email-resent/', views.ResendChangeEmail.as_view(), name='Resend-Change-Email'),
]

# Django toolbar settings for development environments
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
