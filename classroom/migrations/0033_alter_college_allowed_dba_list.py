# Generated by Django 4.0.4 on 2022-05-19 11:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0032_alter_collegedba_college"),
    ]

    operations = [
        migrations.AlterField(
            model_name="college",
            name="allowed_dba_list",
            field=models.FileField(
                blank=True,
                max_length=500,
                null=True,
                upload_to="P:\\Codes\\SEM_4_Major_Project\\Code\\ClassroomBackend\\media/college/dbas/%Y/%m/%d",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["csv", "xlsx"],
                        message="Please Upload CSV/XLSX file only",
                    )
                ],
                verbose_name="Upload DBA List File(.csv/.xl)",
            ),
        ),
    ]
