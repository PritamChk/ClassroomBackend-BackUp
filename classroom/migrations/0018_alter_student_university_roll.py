# Generated by Django 4.0.4 on 2022-05-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0017_alter_notesattachmentfile_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='university_roll',
            field=models.PositiveBigIntegerField(default=5637255, help_text='Your University Roll No - (e.g. - 13071020030)', null=True, verbose_name='University Roll'),
        ),
    ]
