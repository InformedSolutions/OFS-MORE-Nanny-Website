from django.views import View
from django.shortcuts import render


class LinkUsedView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Link-Used' page.
    """
    def get(self, request):
        return render(request, 'link-used.html')
