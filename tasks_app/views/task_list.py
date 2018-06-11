from django.shortcuts import render
from django.views import View


class TaskListView(View):
    def get(self, request):

        from django.conf import settings

        s = settings

        tasks = [
            'Your sign in details',
            'Your personal details',
            'Childcare address',
            'First aid training',
            'Childcare training',
            'Criminal record (DBS) check',
            'Insurance cover',
            'Declaration and payment'
        ]
        context = {'tasks': tasks}
        return render(request, template_name='task-list.html', context=context)
