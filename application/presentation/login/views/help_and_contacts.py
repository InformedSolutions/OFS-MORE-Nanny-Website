from django.views import View

from django.shortcuts import render


class HelpAndContactsView(View):
    def get(self, request):
        return render(request, template_name='help-and-contacts.html')
