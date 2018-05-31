from ..views import render_form
from template.forms.forms import RevealingForm


def revealing_form(request):
    form = RevealingForm()
    return render_form(request, form)