# Generated by Django 4.0.4 on 2022-05-22 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0042_alter_assignment_due_date_alter_assignment_due_time"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SubmittedAssignment",
            new_name="AssignmentSubmission",
        ),
    ]