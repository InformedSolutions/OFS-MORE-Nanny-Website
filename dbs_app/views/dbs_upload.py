from first_aid_app.views.base import BaseTemplateView


class DBSUpload(BaseTemplateView):
    """
    Template view to  render the post dbs page from the dbs task
    """
    template_name = "dbs-upload.html"
    success_url_name = 'dbs:Summary'
