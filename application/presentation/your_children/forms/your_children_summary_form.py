from application.presentation.utilities import NannyForm


class YourChildrenSummaryForm(NannyForm):
    """
    GOV.UK form for the 'your children' task summary
    """
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
