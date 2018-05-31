from .base import render_form
from template.forms.forms import SimpleForm, LongForm, FieldsetForm


def simple_form(request):
    form = SimpleForm()
    return render_form(request, form)


def long_form(request):
    form = LongForm()
    return render_form(request, form)


def fieldset_form(request):
    form = FieldsetForm()
    return render_form(request, form)