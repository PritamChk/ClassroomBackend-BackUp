# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    College,
    Classroom,
    Student,
    AllowedTeacher,
    AllowedStudents,
    Semester,
    Teacher,
)


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "city", "state", "address")
    search_fields = ("name", "address", "city", "state")
    list_filter = ["city", "state"]
    readonly_fields = ["slug"]

    # @admin.display() #FIXME: Show no of classrooms per college
    # def no_of_classes(self, obj: College):
    #     return (
    #         College.objects.prefetch_related("classrooms")
    #         .filter(id=obj.id)
    #         .annotate(count=Count("classrooms"))
    #         .get("count")
    #     )


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "level",
        "stream",
        "start_year",
        "end_year",
        "section",
        "no_of_semesters",
        "current_sem",
        "created_at",
        "college",
    )
    readonly_fields = ["slug"]
    list_filter = (
        "created_at",
        "college",
        "level",
        "stream",
        "start_year",
        "end_year",
        "section",
        "no_of_semesters",
        "current_sem",
    )
    search_fields = [
        "title__icontains",
        "title__istartswith",
        "level__icontains",
        "level__iexact",
        "stream__icontains",
        "stream__istartswith",
        "section__iexact",
    ]
    list_select_related = ["college"]
    autocomplete_fields = ["college"]
    date_hierarchy = "created_at"


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "classroom", "sem_no", "is_current_sem")
    list_filter = ("classroom", "is_current_sem", "classroom__college")
    list_editable = ["is_current_sem"]
    autocomplete_fields = ["classroom"]
    list_select_related = ["classroom", "classroom__college"]
    search_fields = [
        "classroom__title__icontains",
        "classroom__level__icontains",
        "classroom__stream__icontains",
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "id",
        "first_name",
        "last_name",
        "college_name",
        # "level",
        # "stream",
        # "start_year",
        # "end_year",
        # "university_roll",
        "classroom",
    )
    search_fields = [
        # "user__first_name__istartswith",
        # "user__last_name__istartswith",
        # "user__email__contains",
        # "stream__icontains",
        # "university_roll",
        # "level__iexact",
        # "start_year",
        # "end_year",
    ]
    list_filter = (
        "classroom",
        # "college",
        # "level",
        # "stream",
        # "university_roll",
        # "start_year",
        # "end_year",
    )
    autocomplete_fields = ["classroom", "user"]
    list_select_related = ["user", "classroom", "classroom__college"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_filter = ("user", "classroom")
    list_prefetch_related = ["classroom"]
    list_select_related = ["user"]
    autocomplete_fields = ["user", "classroom"]
    raw_id_fields = ("classroom",)


@admin.register(AllowedTeacher)
class AllowedTeacherAdmin(admin.ModelAdmin):
    list_display = ("email", "id")
    raw_id_fields = ("classrooms",)
    list_prefetch_related = ["classrooms"]
    autocomplete_fields = ["classrooms"]
    list_filter = ["classrooms"]
    search_fields = [
        "email",
        "classrooms__title__icontains",
        "classrooms__stream__icontains",
        "classrooms__level__icontains",
        # "classrooms__college__name__istartswith", #FIXME:search in allowed teacher
    ]


@admin.register(AllowedStudents)
class AllowedStudentsAdmin(admin.ModelAdmin):
    list_display = ("email", "id", "university_roll", "classroom")
    # list_editable = ["classroom"] #TODO: Open Later if needed
    list_filter = ["classroom"]
    raw_id_fields = ("classroom",)
    list_select_related = ["classroom"]
    autocomplete_fields = ["classroom"]
    search_fields = ["university_roll", "email"]
