from login_app.views import render_form
from login_app.forms.forms import RevealingForm


def revealing_form(request):
    form = RevealingForm()
    return render_form(request, form)