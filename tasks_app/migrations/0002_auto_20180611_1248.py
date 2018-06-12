# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-11 11:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0001_application_reference_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantPersonalDetails',
            fields=[
                ('personal_detail_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('birth_day', models.IntegerField(blank=True, null=True)),
                ('birth_month', models.IntegerField(blank=True, null=True)),
                ('birth_year', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'APPLICANT_PERSONAL_DETAILS',
            },
        ),
        migrations.AddField(
            model_name='application',
            name='childcare_address_arc_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='application',
            name='childcare_address_status',
            field=models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('FLAGGED', 'FLAGGED')], default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicantpersonaldetails',
            name='application_id',
            field=models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='tasks_app.Application'),
        ),
    ]
