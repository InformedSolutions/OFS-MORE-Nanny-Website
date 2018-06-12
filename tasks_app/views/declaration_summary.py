from django.shortcuts import render
from django.views import View


class DeclarationSummaryView(View):
    def get(self, request):
        return render(request, template_name='declaration-summary.html')
