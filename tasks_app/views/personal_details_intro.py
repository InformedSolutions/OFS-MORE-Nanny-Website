from django.shortcuts import render
from django.views import View


class PersonalDetailsIntroView(View):
    def get(self, request):
        return render(request, template_name='personal-details-intro.html')
