# Generated by Django 4.0.4 on 2022-05-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='classroom',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='classroom.classroom'),
        ),
    ]
