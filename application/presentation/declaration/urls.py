from django.conf import settings
from django.conf.urls import url, include

from declaration_app.views import declaration_guidance, final_declaration, master_summary, confirmation, accepted_confirmation, registration_rules

urlpatterns = [
    url(r'^check-answers/', master_summary.MasterSummary.as_view(), name='Master-Summary'),
    url(r'^declaration/', declaration_guidance.DeclarationGuidance.as_view(), name='Declaration-Guidance'),
    url(r'^your-declaration', final_declaration.FinalDeclaration.as_view(), name='Declaration-Summary'),
    url(r'^accepted-confirmation/', accepted_confirmation.AcceptedConfirmation.as_view(), name='accepted-confirmation'),
    url(r'^confirmation/', confirmation.Confirmation.as_view(), name='confirmation'),
    url(r'^registration-rules/', registration_rules.RegistrationRules.as_view(), name='Registration-Rules')
]