from first_aid_app.views.base import BaseTemplateView


class PaymentDetails(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "payment-details.html"
    success_url_name = 'declaration-payment:confirmation'
