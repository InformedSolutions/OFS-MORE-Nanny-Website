# A generic form-rendering function that renders the correct form based on the request method
from django.shortcuts import render


def render_form(request, form):
    if request.method == 'GET':
        # Get the blank form
        return render(request, 'form.html', {'form': form})
    else:
        # For now, render a generic success page
        return render(request, 'success.html')