import datetime

from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.detail import (
    BaseDetailView, SingleObjectMixin, SingleObjectTemplateResponseMixin,
)

from nanny import NannyGatewayActions, reverse
from nanny.table_util import Table, Row


class FormMixin(ContextMixin):
    """
    A mixin that provides a way to show and handle a form in a request.
    """

    initial = {}
    form_class = None
    success_url = None
    prefix = None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_prefix(self):
        """
        Returns the prefix to use for forms on this view
        """
        return self.prefix

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(FormMixin, self).get_context_data(**kwargs)


class ModelFormMixin(FormMixin, SingleObjectMixin):
    """
    A mixin that provides a way to show and handle a modelform in a request.
    """
    fields = None

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model

            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )

            return model_forms.modelform_factory(model, fields=self.fields)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)


class ProcessFormView(View):
    """
    A mixin that renders a form on GET and processes it on POST.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormView(FormMixin, ProcessFormView):
    """
    A base view for displaying a form.
    """


class FormView(TemplateResponseMixin, BaseFormView):
    """
    A view for displaying a form, and rendering a template response.
    """


class BaseCreateView(ModelFormMixin, ProcessFormView):
    """
    Base view for creating an new object instance.

    Using this base class requires subclassing to provide a response mixin.
    """

    def get(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateView, self).post(request, *args, **kwargs)


class CreateView(SingleObjectTemplateResponseMixin, BaseCreateView):
    """
    View for creating a new object instance,
    with a response rendered by template.
    """
    template_name_suffix = '_form'


class BaseUpdateView(ModelFormMixin, ProcessFormView):
    """
    Base view for updating an existing object.

    Using this base class requires subclassing to provide a response mixin.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateView, self).post(request, *args, **kwargs)


class UpdateView(SingleObjectTemplateResponseMixin, BaseUpdateView):
    """
    View for updating an object,
    with a response rendered by template.
    """
    template_name_suffix = '_form'


class DeletionMixin(object):
    """
    A mixin providing the ability to delete objects
    """
    success_url = None

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseDeleteView(DeletionMixin, BaseDetailView):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """


class DeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    """
    View for deleting an object retrieved with `self.get_object()`,
    with a response rendered by template.
    """
    template_name_suffix = '_confirm_delete'


def create_child_table(child):
    """
    Helper method to create a child table for the 'Your children' summary page
    :param child: the child for which a summary table is to be produced
    :return: table object that can be consumed by the generic summary page template
    """

    dob = datetime.date(child['birth_year'], child['birth_month'], child['birth_day']).strftime('%d %b %Y')
    child_name = str(child['first_name']) + " " + str(child['last_name'])
    child_id = child['child_id']

    if not child['lives_with_applicant']:
        child_address = str(child['street_line1']) + ', ' + str(child['street_line2']) + ', ' \
                        + str(child['town']) + ', ' + str(child['postcode'])

        child_fields = [
            ('full_name', child_name),
            ('date_of_birth', dob),
            ('address', child_address)
        ]

    else:
        child_fields = [
            ('full_name', child_name),
            ('date_of_birth', dob),
            ('address', 'Same as your own')
        ]

    table = Table(child_id)
    table.other_people_numbers = '&child=' + str(child['child'])

    child_table = ({
        'table_object': table,
        'fields': child_fields,
        'title': child_name,
        'error_summary_title': "There was a problem with {0}'s details".format(child_name)
    })

    return child_table


def create_children_living_with_applicant_table(application_id):
    """
    Helper function to create a table of children that live with the applicant for the 'Your children' task
    :return: Table of children that live with the applicant
    """
    children_living_with_applicant_temp_store = []

    api_response = NannyGatewayActions().list(
        'your-children', params={'application_id': application_id, 'ordering': 'date_created'}
    )

    # Define a list of children from the API response, ordered by the date they were created by the applicant
    children = api_response.record
    children_living_with_applicant = [child for child in children if child['lives_with_applicant']]

    # Create a list of names of children that live with the applicant
    for child in children_living_with_applicant:
        child_name = str(child['first_name']) + " " + str(child['last_name'])
        children_living_with_applicant_temp_store.append(child_name)

    # Create list of names for the table row
    if len(children_living_with_applicant_temp_store) == 0:
        children_living_with_you_response_string = 'None'
    else:
        children_living_with_you_response_string = ", ".join(children_living_with_applicant_temp_store)

    table = Table(application_id)

    table.error_summary_title = "There was a problem with the children living with you"

    table.title = "Children living with you"
    change_link_description = 'which of your children live with you'
    back_link = 'your-children:Your-Children-addresses'

    row = Row('children_living_with_you', 'Which of your children live with you?',
              children_living_with_you_response_string, back_link, change_link_description)
    table.add_row(row)

    return table


def create_tables(child_table_list):
    """
    Helper function to create a list of childrens tables for use within the 'Your Children' summary page
    :param child_table_list: List of tabkes if the children generated in the get request of the summary page
    :return: Table output list - populated list of tables to be presented on the summary page
    """

    your_children_dict = {'full_name': 'Name',
                          'date_of_birth': 'Date of birth',
                          'address': 'Address'}

    your_children_link_dict = {'full_name': 'your-children:Your-Children-Details',
                               'date_of_birth': 'your-children:Your-Children-Details',
                               'address': 'your-children:Your-Children-Manual-address'}

    table_output_list = []

    for table in child_table_list:

        # Each iteration of a table will be a dictionary
        for key, value in table['fields']:
            # Create a row object using the data name as the key
            temp_row = Row(key, your_children_dict[key], value, your_children_link_dict[key], '')

            # Table object has rows added
            table['table_object'].add_row(temp_row)

        # Once all rows are added, get any errors for the rows
        # table['table_object'].get_errors()
        table['table_object'].title = table['title']
        table['table_object'].error_summary_title = table['error_summary_title']

        table_output_list.append(table['table_object'])

    return table_output_list


def remove_child(remove_person, application_id):
    """
    Helper method to remove children from the 'Your Children details' subtask
    :param remove_person: child_id to be removed
    :param application_id: ID of the applicant
    :return:
    """
    if remove_person != 0:
        api_response = NannyGatewayActions().list('your-children', params={'application_id': application_id,
                                                                       'ordering': 'date_created'})

        if api_response.status_code == "200":
            child_record = api_response.record

            if int(remove_person) <= len(child_record):
                child_id = child_record[int(remove_person) - 1]['child_id']

                NannyGatewayActions().delete('your-children', params={
                                             'application_id': application_id,
                                             'child_id': child_id,
                                         })

    else:
        pass


def assign_child_numbers(api_response):
    """
    Helper method to assign numbers to children in the 'your chidren' task
    :param api_response: Response when calling .list on the your-children endpoint
    :return: Patches the API with the updated 'child' number
    """
    if api_response.status_code == "200":
        for child in api_response.record:
            child['child'] = api_response.record.index(child) + 1
            NannyGatewayActions().patch('your-children', params=child)

    else:
        pass



def date_formatter(day, month, year):
    """
    helper function to format the date
    """

    output_day = str(day).zfill(2)
    output_month = str(month).zfill(2)
    output_year = str(year)

    return output_day, output_month, output_year


def get_child_number_for_address_loop(application_id, child_list, current_child):
    """
    Helper function to allow for the 'child' number to be returned following address entry
    """

    if len(child_list.record) > int(current_child):
        next_child = int(current_child) + 1
        next_child_record = child_list.record[next_child - 1]
        if not next_child_record['lives_with_applicant']:
            return next_child
        else:
            return get_child_number_for_address_loop(application_id, child_list, next_child)
    else:
        return None

