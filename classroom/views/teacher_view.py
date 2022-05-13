from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from classroom.models import Announcement, Classroom, Semester, Subject, Teacher
from classroom.serializers.classroom import (
    AnnouncementsPostOrUpdateSerializer,
    AnnouncementsReadSerializer,
    ClassroomReadForStudentSerializer,
    ClassroomReadForTeacherSerializer,
    SemesterReadSerializer,
    SubjectCreateByTeacherSerializer,
    SubjectRetriveForTeacherSerializer,
)

from classroom.serializers.teacher import TeacherProfileSerializer


class TeacherProfileViewSet(RetrieveModelMixin, GenericViewSet):
    my_tags = ["[teacher] 1. profile"]
    serializer_class = TeacherProfileSerializer

    def get_queryset(self):
        return (
            Teacher.objects.select_related("user").prefetch_related("classrooms")
            # .filter(user__id=self.request.user.id) #TODO:This will work after permission applied
            .filter(id=self.kwargs["pk"])
        )


class ClassroomsForTeacherViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["[teacher] 2. classrooms"]
    serializer_class = ClassroomReadForTeacherSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Classroom.objects.prefetch_related("teachers", "semesters").filter(
            teachers__id=self.kwargs["teacher_pk"]
        )


class SemesterForTeacherViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["[teacher] 3. semester"]
    serializer_class = SemesterReadSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        sem = Semester.objects.select_related("classroom").filter(
            classroom__slug=self.kwargs["teacher_classrooms_slug"]
        )
        return sem


class SubjectForTeacherViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]
    my_tags = ["[teacher] 4. subjects/classroom"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SubjectRetriveForTeacherSerializer
        elif self.request.method == "POST":
            return SubjectCreateByTeacherSerializer
        return SubjectRetriveForTeacherSerializer

    def get_queryset(self):
        return (
            Subject.objects.select_related("created_by", "semester")
            .filter(
                semester=self.kwargs["sem_pk"], created_by=self.kwargs["teacher_pk"]
            )
            .all()
        )

    def get_serializer_context(self):
        return {
            "created_by": self.kwargs.get("teacher_pk"),
            "sem_pk": self.kwargs.get("sem_pk"),
        }


class AnnouncementPostByTeacherViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]
    my_tags = ["[teacher] 5. announcement/subject"]
    # lookup_field='slug'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AnnouncementsReadSerializer
        return AnnouncementsPostOrUpdateSerializer

    def get_queryset(self):
        return Announcement.objects.select_related("posted_by", "subject").filter(
            posted_by=self.kwargs["teacher_pk"], subject__slug=self.kwargs["subject_slug"]
        )

    def get_serializer_context(self):
        return {
            "teacher_pk": self.kwargs.get("teacher_pk"),
            "subject_slug": self.kwargs.get("subject_slug"),
        }
