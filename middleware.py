from re import compile

from django.conf import settings  # import the settings file
from django.http import HttpResponseRedirect

from identity_models.user_details import UserDetails

COOKIE_IDENTIFIER = '_ofs'


class CustomAuthenticationHandler(object):
    """
    Custom authentication handler to globally protect site with the exception of paths
    tested against regex patterns defined in settings.py
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default the login url as being authentication exempt
        authentication_exempt_urls = [compile(settings.LOGIN_URL.lstrip('/'))]

        # If further login exempt URLs have been defined in the settings.py file, append these to
        # the collection
        if hasattr(settings, 'AUTHENTICATION_EXEMPT_URLS'):
            authentication_exempt_urls += [compile(expr) for expr in settings.AUTHENTICATION_EXEMPT_URLS]

        # Allow authentication exempt paths straight through middleware function
        if request.path_info == settings.AUTHENTICATION_URL or any(
                m.match(request.path_info) for m in authentication_exempt_urls):
            return self.get_response(request)

        # If path is not exempt, and user cookie does not exist (e.g. a bypass is being attempted) return
        # user to login page
        if self.get_session_user(request) is None:
            return HttpResponseRedirect(settings.AUTHENTICATION_URL)

        # If an application id has been supplied in the query string or post request
        application_id = None

        if request.method == 'GET' and 'id' in request.GET:
            application_id = request.GET.get('id')

        if request.method == 'POST' and 'id' in request.POST:
            application_id = request.POST.get('id')

        # If an application id is present fetch application from store
        if application_id is not None and application_id != '':
            record = UserDetails.api.get_record(application_id=application_id).record
            # Check the email address stored in the session matches that found on the application
            # and if not raise generic exception
            if record['email'] != self.get_session_user(request):
                raise Exception

        # If request has not been blocked at this point in the execution flow, allow
        # request to continue processing as normal
        response = self.get_response(request)

        session_user = self.get_session_user(request)
        if session_user is not None:
            CustomAuthenticationHandler.create_session(response, session_user)

        return response

    @staticmethod
    def get_cookie_identifier():
        global COOKIE_IDENTIFIER
        return COOKIE_IDENTIFIER

    @staticmethod
    def get_session_user(request):
        if COOKIE_IDENTIFIER not in request.COOKIES:
            return None
        else:
            return request.COOKIES.get(COOKIE_IDENTIFIER)

    @staticmethod
    def create_session(response, email):
        response.set_cookie(COOKIE_IDENTIFIER, email, max_age=1800)

    @staticmethod
    def destroy_session(response):
        response.delete_cookie(COOKIE_IDENTIFIER)
