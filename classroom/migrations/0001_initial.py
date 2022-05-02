# Generated by Django 4.0.4 on 2022-05-01 16:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name', 'state', 'city'])),
                ('name', models.CharField(max_length=255, verbose_name='College Name')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
                ('state', models.CharField(max_length=255, verbose_name='State')),
                ('address', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name', 'city', 'state'],
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['title', 'level', 'stream', 'section', 'start_year', 'end_year', 'college'])),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Classroom Name')),
                ('level', models.CharField(help_text='e.g - UG/PG/MASTERS', max_length=40, verbose_name='Level')),
                ('stream', models.CharField(max_length=255, verbose_name='Your Stream')),
                ('start_year', models.PositiveSmallIntegerField(db_index=True, default=2020, help_text='Write your session starting year (e.g. - 2020)', validators=[django.core.validators.MinValueValidator(2000, "You can't select year less than 2000"), django.core.validators.MaxValueValidator(2023, 'Max Year Can be selected only 1 year ahead of current year')], verbose_name='Starting Year')),
                ('end_year', models.PositiveSmallIntegerField(db_index=True, default=2022, help_text='Write your session ending year (e.g. - 2020)', validators=[django.core.validators.MinValueValidator(2000, "You can't select year less than 2000"), django.core.validators.MaxValueValidator(2200, 'Max Year Can be selected only 1 year ahead of current year')], verbose_name='Ending Year')),
                ('section', models.CharField(blank=True, default='A', max_length=10, null=True, verbose_name='Section(optional)')),
                ('no_of_semesters', models.PositiveSmallIntegerField(default=4, validators=[django.core.validators.MinValueValidator(4, 'Min Course Duration is of 2 Years(4 semesters)'), django.core.validators.MaxValueValidator(14)], verbose_name='Number of Sem')),
                ('current_sem', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(14)], verbose_name='On Going Sem')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('allowed_student_list', models.FileField(default='', upload_to='classroom/students/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xlsx'], message='Please Upload CSV/XLSX file only')], verbose_name='Upload student List File(.csv)')),
                ('allowed_teacher_list', models.FileField(default='', upload_to='classroom/teachers/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xlsx'], message='Please Upload CSV/XLSX file only')], verbose_name='Upload teacher List File(.csv)')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='classroom.college')),
            ],
            options={
                'unique_together': {('level', 'stream', 'start_year', 'end_year', 'section', 'college')},
            },
        ),
        migrations.CreateModel(
            name='AllowedTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='Email Id')),
                ('classrooms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_teachers', to='classroom.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem_no', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'sem value > 0'), django.core.validators.MaxValueValidator(14, 'sem value < 15')], verbose_name='Semester No')),
                ('is_current_sem', models.BooleanField(default=False, verbose_name='is this sem going on? ')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='classroom.classroom')),
            ],
            options={
                'unique_together': {('classroom', 'sem_no')},
            },
        ),
        migrations.CreateModel(
            name='AllowedStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='Email Id')),
                ('university_roll', models.PositiveBigIntegerField(help_text='Your University Roll No - (e.g. - 13071020030)', verbose_name='University Roll')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_students', to='classroom.classroom')),
            ],
            options={
                'verbose_name_plural': 'Allowed Students',
                'unique_together': {('university_roll', 'email'), ('classroom', 'email'), ('university_roll', 'classroom')},
            },
        ),
    ]
