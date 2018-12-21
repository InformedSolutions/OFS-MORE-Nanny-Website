from application.presentation.utilities import NannyForm


class YourChildrenSummaryForm(NannyForm):
    """
    GOV.UK form for the 'your children' task summary
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    auto_replace_widgets = True
