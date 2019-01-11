from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView, TemplateView
from .utilities import app_id_finder, build_url



class NannyFormView(FormView):
    """
    This is the base interface from which the rest of the Nanny forms inherit from
    It contains a set of base methods to aid in page design/workflow, see the django documentation on GCBVs for details
    """

    # Used in the generation of the url for a successful form submission's destination
    success_url = None
    success_parameters = {}

    def get_context_data(self, **kwargs):
        """
        Get context data passes arguments into the template context for the view
        :param kwargs:
        :return: a dictionary containing all the data to be rendered
        """

        context = super(NannyFormView, self).get_context_data()
        context['id'] = app_id_finder(self.request)

        return context

    def get_success_url(self):
        """
        Get success url is called whenever a successful form submission occurs, it generates a url based off of
        success_url and success_parameters as defined in the class definition
        :return: a full url for the next page
        """

        if self.success_url:
            # If not none, run the build url util function
            url = build_url(self.success_url, get=self.get_success_parameters())
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return url

    def get_success_parameters(self):
        """
        Custom method to generate the list of get parameters for the success_url
        :return: a dictionary containing each of the pieces of data to be sent
        """
        params = dict()
        params['id'] = app_id_finder(self.request)

        return params

    def get_form(self, form_class=None):
        """
        Method to instantiate the form for rendering in the view.
        If it is a GET request, perform check for ARC comments.
        If it is a POST, remove any existing ARC comments.
        """
        form = super(NannyFormView, self).get_form(form_class)
        id = app_id_finder(self.request)
        if self.request.method == 'GET':
            if getattr(form, 'check_flags', None):
                form.check_flags(id)
        elif self.request.method == 'POST':
            if getattr(form, 'remove_flags', None):
                form.remove_flags(id)
        return form



class NannyTemplateView(TemplateView):
    """
    Base Template view is used for any pages that do not require a form, but still require some context data
    """
    success_url_name = None

    def get_context_data(self, **kwargs):
        """
        Get context data passes arguments into the template context for the view, in this case, the link to be followed
        :param kwargs:
        :return:
        """
        context = super(NannyTemplateView, self).get_context_data(**kwargs)
        application_id = app_id_finder(self.request)
        context['link_url'] = build_url(self.success_url_name, get={'id': application_id})
        context['id'] = app_id_finder(self.request)
        return context
