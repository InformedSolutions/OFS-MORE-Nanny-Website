"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- form_fields.py --
@author: Informed Solutions
"""

import datetime
from collections import OrderedDict

from django import forms
from govuk_forms import fields as govf
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext, gettext_lazy as _

from govuk_forms.widgets import SplitHiddenDateWidget, SplitDateWidget

from application.presentation.widgets import ExpirySplitDateWidget, TimeKnownSplitDateWidget


class YearField(forms.IntegerField):
    """
    In integer field that accepts years between 1900 and now
    Allows 2-digit year entry which is converted depending on the `era_boundary`
    """

    def __init__(self, era_boundary=None, **kwargs):
        """
        When initialised, this field object will create attributes for later validation base of the current time and
        year, error messages and field options are specified here.
        :param era_boundary: If supplied, will limit how far back a user cna enter without raising an error
        :param kwargs: Any other key word arguments passed during the implementation of the class
        """
        self.current_year = now().year
        self.century = 100 * (self.current_year // 100)
        if era_boundary is None:
            # 2-digit dates are a minimum of 10 years ago by default
            era_boundary = self.current_year - self.century - 10
        self.era_boundary = era_boundary
        bounds_error = gettext('Check the expiry date or use a new card')
        options = {
            'min_value': self.current_year,
            'error_messages': {
                'min_value': bounds_error,
                'invalid': gettext('Check the expiry date or use a new card'),
            }
        }
        options.update(kwargs)
        super().__init__(**options)

    def clean(self, value):
        """
        This will clean the two year value entered into the field in order to ensure the value entered is in the write
        century, for example, 68 will be changed to 1968 rather the 2068 as the latter has not occured yet
        :param value:The value object obtained from the form
        :return:This returns the cleaned value object (after cleaning specified above
        """
        value = self.to_python(value)
        if len(str(value)) > 2:
            raise forms.ValidationError('Check the expiry date or use a new card')
        if isinstance(value, int) and value < 100:
                value += self.century

        return super().clean(value)


class ExpirySplitDateField(forms.MultiValueField):
    """
    This class defines the validation for the month field and also the overall ordering and organisation for the two
    fields
    """
    widget = ExpirySplitDateWidget
    hidden_widget = SplitHiddenDateWidget
    default_error_messages = {
        'invalid': _('Check the expiry date or use a new card')
    }

    def __init__(self, *args, **kwargs):
        """
        Standard constructor that defines what the month field should do, and which errors should be raised should
        certain events occur
        :param args: Standard arguments parameter
        :param kwargs: Standard key word arguments parameter
        """
        month_bounds_error = gettext('Check the expiry date or use a new card')

        # Field definition
        self.fields = [
            forms.IntegerField(min_value=1, max_value=12, error_messages={
                'min_value': month_bounds_error,
                'max_value': month_bounds_error,
                'invalid': gettext('Check the expiry date or use a new card')
            }),
            # Uses a clean year field defined above
            YearField(),
        ]

        super().__init__(self.fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Uses compress as there are multiple values (compress is a replacement for clean in these cases
        :param data_list: The object containing each of the values
        :return: Returns the cleaned value object
        """
        if data_list:
            try:
                if any(item in self.empty_values for item in data_list):
                    raise ValueError
                return data_list[1], data_list[0]
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'], code='invalid')
        return None

    def widget_attrs(self, widget):
        """
        Populates the attributes of the widget with the values defined in the original widget creation
        :param widget: The widget to have its parameters populated
        :return: returns the attributes
        """
        attrs = super().widget_attrs(widget)
        if not isinstance(widget, ExpirySplitDateWidget):
            return attrs
        for subfield, subwidget in zip(self.fields, widget.widgets):
            if subfield.min_value is not None:
                subwidget.attrs['min'] = subfield.min_value
            if subfield.max_value is not None:
                subwidget.attrs['max'] = subfield.max_value
        return attrs


class TimeKnownField(forms.MultiValueField):
    """
    Class that defines the field type used for both month and years in the TimeKnownWidget
    """
    widget = TimeKnownSplitDateWidget
    hidden_widget = SplitHiddenDateWidget
    default_error_messages = {
        'invalid': _('Enter a valid date')
    }

    def __init__(self, *args, **kwargs):
        """
        The contructor defines each field for the object, the errors it can raise and the resultant error text should
        an error be returned
        :param args: Standard arguments parameter
        :param kwargs: Standard key word arguments parameter
        """
        month_bounds_error = gettext('Month must be between 1 and 11')
        year_bounds_error = gettext('You must have known the referee for at least 1 year')

        self.fields = [
            forms.IntegerField(min_value=0, error_messages={
                'min_value': year_bounds_error,
                'max_value': year_bounds_error,
                'invalid': gettext('You must have known the referee for at least 1 year')
            }),
            forms.IntegerField(max_value=11, error_messages={
                'min_value': month_bounds_error,
                'max_value': month_bounds_error,
                'invalid': gettext('Month must be between 1 and 11')
            })
        ]

        super().__init__(self.fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Compresses the resultant data list into a single tuple for returning to wherever the result is called
        :param data_list: The list of field inputs
        :return: Atuple containing the amount of months and years known in the correct order
        """
        if data_list:
            try:
                if any(item in self.empty_values for item in data_list):
                    raise ValueError
                return data_list[1], data_list[0]
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'], code='invalid')
        return None

    def widget_attrs(self, widget):
        """
        Populates the attributes of the widget with the values defined in the original widget creation
        :param widget: The widget to have its parameters populated
        :return: returns the attributes
        """
        attrs = super().widget_attrs(widget)
        if not isinstance(widget, ExpirySplitDateWidget):
            return attrs
        for subfield, subwidget in zip(self.fields, widget.widgets):
            if subfield.min_value is not None:
                subwidget.attrs['min'] = subfield.min_value
            if subfield.max_value is not None:
                subwidget.attrs['max'] = subfield.max_value
        return attrs


class CustomSplitDateFieldDOB(forms.MultiValueField):
    widget = SplitDateWidget
    hidden_widget = SplitHiddenDateWidget
    default_error_messages = {
        'invalid': _('Please enter a valid date')
    }


    def __init__(self, *args, **kwargs):
        day_bounds_error = gettext('Day must be between 1 and 31')
        month_bounds_error = gettext('Month must be between 1 and 12')

        self.fields = [
            forms.IntegerField(min_value=1, max_value=31, error_messages={
                'min_value': day_bounds_error,
                'max_value': day_bounds_error,
                'invalid': gettext('Enter day as a number')
            }),
            forms.IntegerField(min_value=1, max_value=12, error_messages={
                'min_value': month_bounds_error,
                'max_value': month_bounds_error,
                'invalid': gettext('Enter month as a number')
            }),
            CustomYearFieldDOB(),
        ]

        super().__init__(self.fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            try:
                if any(item in self.empty_values for item in data_list):
                    raise ValueError
                return datetime.date(data_list[2], data_list[1], data_list[0])
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'], code='invalid')
        return None

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if not isinstance(widget, SplitDateWidget):
            return attrs
        for subfield, subwidget in zip(self.fields, widget.widgets):
            if subfield.min_value is not None:
                subwidget.attrs['min'] = subfield.min_value
            if subfield.max_value is not None:
                subwidget.attrs['max'] = subfield.max_value
        return attrs


class CustomYearFieldDOB(forms.IntegerField):
    """
    In integer field that accepts years between 1900 and now
    Allows 2-digit year entry which is converted depending on the `era_boundary`
    """

    def __init__(self, era_boundary=None, **kwargs):
        self.current_year = now().year
        self.century = 100 * (self.current_year // 100)
        if era_boundary is None:
            # 2-digit dates are a minimum of 10 years ago by default
            era_boundary = self.current_year - self.century - 10
        self.era_boundary = era_boundary
        options = {
            'error_messages': {
                'invalid': gettext('Enter year as a number'),
            }
        }
        options.update(kwargs)
        super().__init__(**options)

    def clean(self, value):
        value = self.to_python(value)
        if len(str(value)) < 4:
            raise forms.ValidationError('Please enter the whole year (4 digits)')
        if value < 1900:
            raise forms.ValidationError('Please check the year')
        if value > now().year:
            raise forms.ValidationError('Please check the year')
        return super().clean(value)


class CustomSplitDateField(forms.MultiValueField):
    widget = SplitDateWidget
    hidden_widget = SplitHiddenDateWidget
    default_error_messages = {
        'invalid': _('Please check the date of the course')
    }

    def __init__(self, bounds_error=None, min_value=2000, *args, **kwargs):
        day_bounds_error = gettext('Day must be between 1 and 31')
        month_bounds_error = gettext('Month must be between 1 and 12')

        self.fields = [
            forms.IntegerField(min_value=1, max_value=31, error_messages={
                'min_value': day_bounds_error,
                'max_value': day_bounds_error,
                'invalid': gettext('Enter day as a number')
            }),
            forms.IntegerField(min_value=1, max_value=12, error_messages={
                'min_value': month_bounds_error,
                'max_value': month_bounds_error,
                'invalid': gettext('Enter month as a number')
            }),
            CustomYearField(bounds_error=bounds_error, min_value=min_value),
        ]

        super().__init__(self.fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            try:
                if any(item in self.empty_values for item in data_list):
                    raise ValueError
                date_compressed = datetime.date(data_list[2], data_list[1], data_list[0])
                if date_compressed > now().date():
                    raise ValueError
                else:
                    return date_compressed
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'], code='invalid')
        return None

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if not isinstance(widget, SplitDateWidget):
            return attrs
        for subfield, subwidget in zip(self.fields, widget.widgets):
            if subfield.min_value is not None:
                subwidget.attrs['min'] = subfield.min_value
            if subfield.max_value is not None:
                subwidget.attrs['max'] = subfield.max_value
        return attrs



class CustomYearField(forms.IntegerField):
    """
    In integer field that accepts years between 1900 and now
    Allows 2-digit year entry which is converted depending on the `era_boundary`
    """

    def __init__(self, era_boundary=None, bounds_error=None, min_value=2000, **kwargs):
        self.current_year = now().year
        self.century = 100 * (self.current_year // 100)
        if era_boundary is None:
            # Interpret two-digit dates as this century if they are before the current year
            # otherwise interpret them as a year from the previous century
            era_boundary = self.current_year - self.century
        self.era_boundary = era_boundary
        if bounds_error is None:
            bounds_error = gettext('Please check the date of the course') % {
                'current_year': self.current_year
            }
        else:
            bounds_error = gettext(bounds_error)
        options = {
            'min_value': min_value,
            'max_value': self.current_year,
            'error_messages': {
                'min_value': bounds_error,
                'max_value': bounds_error,
                'invalid': gettext('Enter year as a number'),
            }
        }
        options.update(kwargs)
        super().__init__(**options)

    def clean(self, value):
        value = self.to_python(value)
        if isinstance(value, int) and value < 100:
            if value > self.era_boundary:
                value += self.century - 100
            else:
                value += self.century
        return super().clean(value)

class CustomSplitDateFieldAddress(govf.SplitDateField):
    """
    Extends govuk_forms.fields.SplitDateField to:
    * allow all child field options and error messages to be customised (prefix with "day_", "month_" or "year_")
    * use different default bounds and error messages
    * introduce finer-grained error messages for date validation
    * allow same error message to be used for multiple validation types without duplicate messages being
      added to error list
    * allow 4-digit years to be required
    """

    # Sentinel which can be passed in for min_value or max_value, triggering a different error message than if a fixed
    # date was passed in
    TODAY = object()

    default_error_messages = {
        'invalid': 'Enter a real date',
        'required': 'Enter the date, including the day, month and year',
        'incomplete': 'Enter the date, including the day, month and year',
        'min_value': 'Date must be after 1 Jan 1900',
        'max_value': "Date must be before today's date",
        'min_today': 'Date must be in the future',
        'max_today': 'Date must be in the past',
        'short_year': 'The year is too short',
    }

    def __init__(self, *args, **kwargs):

        day_args = self._pop_prefixed_kwargs(kwargs, 'day_')
        day_options = {
            'min_value': 1,
            'max_value': 31,
            'error_messages': {
                'min_value': 'Day must be between 1 and 31',
                'max_value': 'Day must be between 1 and 31',
                'invalid': 'Enter day as a number',
            },
        }
        day_options.update(day_args)

        month_args = self._pop_prefixed_kwargs(kwargs, 'month_')
        month_options = {
            'min_value': 1,
            'max_value': 12,
            'error_messages': {
                'min_value': 'Month must be between 1 and 12',
                'max_value': 'Month must be between 1 and 12',
                'invalid': 'Enter month as a number',
            },
        }
        month_options.update(month_args)

        year_args = self._pop_prefixed_kwargs(kwargs, 'year_')
        current_year = datetime.date.today().year
        century = 100 * (current_year // 100)
        era_boundary = current_year - century
        year_options = {
            'min_value': 1900,
            'max_value': current_year,
            'era_boundary': era_boundary,
            'error_messages': {
                'min_value': 'Year must be between 1900 and the current year',
                'max_value': 'Year must be between 1900 and the current year',
                'invalid': 'Enter year as a number',
                'short_year': 'Enter year in long year format.'
            },
        }
        year_options.update(year_args)

        options = {
            'min_value': datetime.date(1900, 1, 1),
            'max_value': self.TODAY,
            'required': False,
            'allow_short_year': True,
        }
        options.update(**kwargs)

        self.min_value = options.pop('min_value')
        self.max_value = options.pop('max_value')
        self.required = options.pop('required')
        self.allow_short_year = options.pop('allow_short_year')

        self.fields = [
            forms.IntegerField(**day_options),
            forms.IntegerField(**month_options)
        ]

        if self.allow_short_year:
            self.fields.append(govf.YearField(**year_options))
        else:
            year_options.pop('era_boundary')
            self.fields.append(NoShortYearField(**year_options))

        super(govf.SplitDateField, self).__init__(self.fields, *args, **options)

    def clean(self, value):
        """
        `clean` is not usually overidden for MultiValueField subclasses, however we're just
        overriding to do a final de-duplication on the error messages before the ValidationError
        is raised
        """
        try:
            return super().clean(value)
        except ValidationError as e:
            # de-duplicate error message list and raise new ValidationError.
            # Using keys of OrderedDict because python has no OrderedSet class
            uniques = OrderedDict((err.message, None) for err in e.error_list)
            raise ValidationError(list(uniques.keys())) from e

    def compress(self, data_list):
        """
        `compress` is used in place of `clean` for subclasses of MultiValueField
        """
        if not data_list:
            return None

        if any(item in self.empty_values for item in data_list):
            if self.required:
                raise forms.ValidationError(self.error_messages['required'], code='required')
            else:
                return None

        try:
            date_compressed = datetime.date(data_list[2], data_list[1], data_list[0])
        except ValueError:
            raise forms.ValidationError(self.error_messages['invalid'], code='invalid')

        if self.min_value is not None:
            if self.min_value is self.TODAY and date_compressed < datetime.date.today():
                raise forms.ValidationError(self.error_messages['min_today'], code='min_today')
            elif self.min_value is not self.TODAY and date_compressed < self.min_value:
                raise forms.ValidationError(self.error_messages['min_value'], code='min_value')

        if self.max_value is not None:
            if self.max_value is self.TODAY and date_compressed > datetime.date.today():
                raise forms.ValidationError(self.error_messages['max_today'], code='max_today')
            elif self.max_value is not self.TODAY and date_compressed < self.max_value:
                raise forms.ValidationError(self.error_messages['max_value'], code='max_value')

        return date_compressed

    def _pop_prefixed_kwargs(self, kwarg_dict, prefix):
        result = {}
        dict_copy = dict(kwarg_dict)
        for k, v in dict_copy.items():
            if k.startswith(prefix):
                result[k[len(prefix):]] = kwarg_dict.pop(k)
        return result

