from django.conf import settings
from django.conf.urls import url, include

from declaration_payment_app.views import declaration_guidance, final_declaration, master_summary, payment_details

urlpatterns = [
    url(r'^check-answers/', master_summary.MasterSummary.as_view(), name='Master-Summary'),
    url(r'^declaration/', declaration_guidance.DeclarationGuidance.as_view(), name='Declaration-Guidance'),
    url(r'^your-declaration', final_declaration.FinalDeclaration.as_view(), name='Declaration-Summary'),
    url(r'^payment/details', payment_details.PaymentDetails.as_view(), name='payment-details'),
]