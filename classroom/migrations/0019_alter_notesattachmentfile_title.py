# Generated by Django 4.0.4 on 2022-05-11 18:54

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0018_alter_classroom_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notesattachmentfile',
            name='title',
            field=django_extensions.db.fields.AutoSlugField(blank=True, default='a-1', editable=False, populate_from=['notes__title', 'notes__subject__title', 'created_at']),
            preserve_default=False,
        ),
    ]
