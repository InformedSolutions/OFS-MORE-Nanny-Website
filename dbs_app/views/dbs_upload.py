from nanny.base_views import NannyTemplateView


class DBSUpload(NannyTemplateView):
    """
    Template view to  render the post dbs page from the dbs task
    """
    template_name = "dbs-upload.html"
    success_url_name = 'dbs:Summary'
