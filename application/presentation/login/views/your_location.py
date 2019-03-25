from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms.your_location import YourLocationForm


def your_location(request):
    """
    Function to handle GET and POST request to the new public beta splitting page
    This view is copied directly from the Childminder implementation.
    """

    if request.method == 'GET':
        form = YourLocationForm()
        variables = {
            'form': form
        }
        return render(request, 'your-location.html', variables)

    if request.method == 'POST':
        form = YourLocationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['your_location'] == 'True':
                return HttpResponseRedirect(reverse('Account-Selection'))
            else:
                return redirect("https://online.ofsted.gov.uk/onlineofsted/Ofsted_Online.ofml")
        else:
            variables = {
                'form': form,
            }
            return render(request, 'your-location.html', variables)
