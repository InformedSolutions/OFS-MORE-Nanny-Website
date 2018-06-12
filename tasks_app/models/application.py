from uuid import uuid4

from django.core.validators import RegexValidator
from django.db import models


class NannyApplication(models.Model):
    """
    Model for APPLICATION table
    """
    APP_STATUS = (
        ('ARC_REVIEW', 'ARC_REVIEW'),
        ('CANCELLED', 'CANCELLED'),
        ('CYGNUM_REVIEW', 'CYGNUM_REVIEW'),
        ('DRAFTING', 'DRAFTING'),
        ('FURTHER_INFORMATION', 'FURTHER_INFORMATION'),
        ('NOT_REGISTERED', 'NOT_REGISTERED'),
        ('REGISTERED', 'REGISTERED'),
        ('REJECTED', 'REJECTED'),
        ('SUBMITTED', 'SUBMITTED'),
        ('WITHDRAWN', 'WITHDRAWN')
    )
    APP_TYPE = (
        ('CHILDMINDER', 'CHILDMINDER'),
        ('NANNY', 'NANNY'),
        ('NURSERY', 'NURSERY'),
        ('SOCIAL_CARE', 'SOCIAL_CARE')
    )
    TASK_STATUS = (
        ('NOT_STARTED', 'NOT_STARTED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('FLAGGED', 'FLAGGED')
    )
    application_id = models.UUIDField(primary_key=True, default=uuid4)
    application_type = models.CharField(choices=APP_TYPE, max_length=50, blank=True)
    application_status = models.CharField(choices=APP_STATUS, max_length=50, blank=True)
    cygnum_urn = models.CharField(max_length=50, blank=True)
    login_details_status = models.CharField(choices=TASK_STATUS, max_length=50)
    login_details_arc_flagged = models.BooleanField(default=False)
    personal_details_status = models.CharField(choices=TASK_STATUS, max_length=50)
    personal_details_arc_flagged = models.BooleanField(default=False)
    childcare_address_status = models.CharField(choices=TASK_STATUS, max_length=50)
    childcare_address_arc_flagged = models.BooleanField(default=False)
    first_aid_training_status = models.CharField(choices=TASK_STATUS, max_length=50)
    first_aid_training_arc_flagged = models.BooleanField(default=False)
    childcare_training_status = models.CharField(choices=TASK_STATUS, max_length=50)
    childcare_training_arc_flagged = models.BooleanField(default=False)
    criminal_record_check_status = models.CharField(choices=TASK_STATUS, max_length=50)
    criminal_record_check_arc_flagged = models.BooleanField(default=False)
    insurance_cover_status = models.CharField(choices=TASK_STATUS, max_length=50)
    insurance_cover_arc_flagged = models.BooleanField(default=False)
    declarations_status = models.CharField(choices=TASK_STATUS, max_length=50)
    share_info_declare = models.NullBooleanField(blank=True, null=True, default=None)
    display_contact_details_on_web = models.NullBooleanField(blank=True, null=True, default=None)
    suitable_declare = models.NullBooleanField(blank=True, null=True, default=None)
    information_correct_declare = models.NullBooleanField(blank=True, null=True, default=None)
    change_declare = models.NullBooleanField(blank=True, null=True, default=None)
    date_created = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    date_accepted = models.DateTimeField(blank=True, null=True)
    date_submitted = models.DateTimeField(blank=True, null=True)
    application_reference = models.CharField(blank=True, null=True, max_length=9,
                                             validators=[RegexValidator(r'(\w{2})([0-9]{7})')])
    ofsted_visit_email_sent = models.DateTimeField(blank=True, null=True)

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(pk=app_id)

    class Meta:
        db_table = 'NANNY_APPLICATION'
