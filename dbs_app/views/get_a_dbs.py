from nanny.base_views import NannyTemplateView


class GetDBSView(NannyTemplateView):
    """
    Template view to render the Get A DBS page.
    """
    template_name = 'get-a-dbs.html'
    success_url_name = 'Task-List'
