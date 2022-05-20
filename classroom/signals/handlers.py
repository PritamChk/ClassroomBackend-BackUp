from .classroom_handlers import (
    create_allowed_students,
    create_allowed_teacher_for_classroom_level,
    create_allowed_teacher_for_classroom_level_with_check,
    create_sems_for_new_classroom,
)
from .college_handlers import (
    create_allowed_teacher,
    remove_teacher_profile_after_allowed_teacher_deletion,
    send_mail_after_create_allowed_teacher,
)
from .dba_handlers import create_allowed_dba
from .profile_handlers import create_profile
from .teacher_classroom_handlers import (
    assign_classroom_to_existing_teacher,
    auto_join_teacher_to_classes,
    remove_class_after_removal_of_assigned_teacher,
)
from .user_handlers import (
    delete_user_on_dba_delete,
    delete_user_on_student_delete,
    delete_user_on_teacher_delete, #FIXME: not working
)

# @shared_task
# @receiver(post_save, sender=Classroom)
# def create_sems_for_new_classroom(sender, instance: Classroom, **kwargs):
#     if kwargs.get("created"):
#         sems = [
#             Semester(
#                 classroom=instance,
#                 sem_no=i + 1,
#                 is_current_sem=instance.current_sem == i + 1,
#             )
#             for i in range(instance.no_of_semesters)
#         ]
#         Semester.objects.bulk_create(sems)


# @shared_task
# @receiver(post_save, sender=Classroom)
# def create_allowed_students(sender, instance: Classroom, created, **kwargs):
#     if created:
#         if instance.allowed_student_list == None:
#             send_mail(
#                 "Allowed Student List Does Not Exists",
#                 "You Have To Create Allowed Students Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         file_abs_path = None
#         student_file_path = os.path.join(
#             settings.BASE_DIR,
#             settings.MEDIA_ROOT,
#             instance.allowed_student_list.name,
#         )
#         if os.path.exists(student_file_path):
#             file_abs_path = os.path.abspath(student_file_path)
#         else:
#             send_mail(
#                 "Allowed Student List Does Not Exists",
#                 "You Have To Create Allowed Students Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None

#         df = None
#         if str(file_abs_path).split(".")[-1] == "csv":
#             df = pd.read_csv(file_abs_path)
#         elif str(file_abs_path).split(".")[-1] == "xlsx":
#             df = pd.read_excel(file_abs_path)

#         if not (
#             "university_roll" in df.columns and "email" in df.columns
#         ):  # TODO:check col name case insensitive
#             send_mail(
#                 "Wrong File Structure",
#                 "column name should be => 'university_roll' | 'email' ",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         list_of_students = [
#             AllowedStudents(classroom=instance, **args)
#             for args in df.to_dict("records")
#         ]
#         AllowedStudents.objects.bulk_create(list_of_students)
#         email_list = df["email"].to_list()
#         subject = "Create Your Student Account"
#         prompt = "please use your following mail id to sign up in the Classroom[LMS]"
#         try:
#             send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
#         except BadHeaderError:
#             print("Could not able to sen emails to students")
#         os.remove(file_abs_path)
#         Classroom.objects.update(allowed_student_list="")


# @shared_task
# @receiver(post_save, sender=College)
# def create_allowed_teacher(sender, instance: College, created, **kwargs):
#     if created:
#         if instance.allowed_teacher_list == None:
#             send_mail(
#                 "Allowed Teacher List Does Not Exists",
#                 "You Have To Create Allowed Teachers Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         file_abs_path = None
#         dba_file_path = os.path.join(
#             settings.BASE_DIR,
#             settings.MEDIA_ROOT,
#             instance.allowed_teacher_list.name,
#         )
#         if os.path.exists(dba_file_path):
#             file_abs_path = os.path.abspath(dba_file_path)
#         else:
#             send_mail(
#                 "Allowed Teacher List Does Not Exists",
#                 "You Have To Create Allowed Teachers Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None

#         df = None
#         if str(file_abs_path).split(".")[-1] == "csv":
#             df: pd.DataFrame = pd.read_csv(file_abs_path)
#         elif str(file_abs_path).split(".")[-1] == "xlsx":
#             df = pd.read_excel(file_abs_path)

#         if not "email" in df.columns:
#             send_mail(
#                 "Wrong File Structure",
#                 "column name should be => 'email' ",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         df_dict = df.to_dict("records")
#         # print(df_dict)
#         list_of_teachers = [
#             AllowedTeacher(college=instance, **args) for args in df.to_dict("records")
#         ]
#         AllowedTeacher.objects.bulk_create(list_of_teachers)
#         # create_bulk_allowed_teacher.delay(df_dict, instance)
#         email_list = df["email"].to_list()
#         subject = "Create Your Teacher Account"
#         prompt = "please use your following mail id to sign up in the Classroom[LMS]"
#         try:
#             send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
#         except BadHeaderError:
#             print("Could not able to sen emails to students")
#         os.remove(file_abs_path)
#         College.objects.update(allowed_teacher_list="")


# @receiver(post_save, sender=AllowedTeacher)
# def send_mail_after_create_allowed_teacher(
#     sender, instance: AllowedTeacher, created, **kwargs
# ):
#     if created:
#         college: College = College.objects.get(pk=instance.college)
#         # email_list = df["email"].to_list()
#         subject = "Create Your Teacher Account"
#         prompt = f"please use your following mail id - {instance.email} \n to sign up in the Classroom[LMS]"
#         try:
#             send_mail(subject, prompt, college.owner_email_id, [instance.email])
#         except BadHeaderError:
#             cprint("Could not able to sen emails to students", "red")


# @receiver(post_delete, sender=AllowedTeacher)
# def remove_teacher_profile_after_allowed_teacher_deletion(
#     sender, instance: AllowedTeacher, **kwargs
# ):
#     try:
#         teacher_profile: Teacher = Teacher.objects.select_related("user").get(
#             user__email=instance.email
#         )
#         teacher_profile.delete()
#         return Response(
#             data={"massage": f"{instance.email} has been successfully removed."},
#             status=status.HTTP_202_ACCEPTED,
#         )
#     except:
#         raise ValidationError(
#             "Either teacher profile does not exists or couldn't able to delete that",
#             code=status.HTTP_302_FOUND,
#         )


# @shared_task
# @receiver(post_save, sender=Classroom)
# def create_allowed_teacher_for_classroom_level(
#     sender, instance: Classroom, created, **kwargs
# ):
#     if created:
#         if instance.allowed_teacher_list == None:
#             send_mail(
#                 "Allowed Teacher List Does Not Exists",
#                 "You Have To Create Allowed Teachers Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         file_abs_path = None
#         dba_file_path = os.path.join(
#             settings.BASE_DIR,
#             settings.MEDIA_ROOT,
#             instance.allowed_teacher_list.name,
#         )
#         if os.path.exists(dba_file_path):
#             file_abs_path = os.path.abspath(dba_file_path)
#         else:
#             send_mail(
#                 "Allowed Teacher List Does Not Exists",
#                 "You Have To Create Allowed Teachers Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None

#         df = None
#         if str(file_abs_path).split(".")[-1] == "csv":
#             df: pd.DataFrame = pd.read_csv(file_abs_path)
#         elif str(file_abs_path).split(".")[-1] == "xlsx":
#             df = pd.read_excel(file_abs_path)

#         if not "email" in df.columns:
#             send_mail(
#                 "Wrong File Structure",
#                 "column name should be => 'email' ",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         df_dict: list[dict] = df.to_dict("records")
#         # print(df_dict)
#         college_allowed_teacher_list = list(
#             AllowedTeacher.objects.select_related("college")
#             .filter(college=instance.college)
#             .values_list("email", flat=True)
#         )

#         list_of_teachers = []
#         rejected_teacher_mails = []
#         from termcolor import cprint

#         for allowed_teacher in df_dict:
#             if allowed_teacher["email"] in college_allowed_teacher_list:
#                 list_of_teachers.append(
#                     AllowedTeacherClassroomLevel(classroom=instance, **allowed_teacher)
#                 )
#                 cprint("OUTSIDE OF IF", "yellow")
#                 if (
#                     Teacher.objects.select_related("user")
#                     .filter(user__email=allowed_teacher["email"])
#                     .exists()
#                 ):
#                     cprint("INSIDE OF IF", "yellow")
#                     teacher = Teacher.objects.select_related("user").get(
#                         user__email=allowed_teacher["email"]
#                     )
#                     instance.teachers.add(teacher)
#                     instance.save(force_update=True)
#                     for tchr in instance.teachers.all():
#                         cprint("Classrooms of teachers -> ", "cyan")
#                         cprint(tchr, "cyan")
#                 # AllowedTeacherClassroomLevel.objects.create(
#                 #     classroom=instance, **allowed_teacher
#                 # )
#             else:
#                 rejected_teacher_mails.append(allowed_teacher["email"])
#         if len(rejected_teacher_mails) > 0:
#             send_mail(
#                 "Some Teacher's don't belong to the college",
#                 f"""
#                 Please add this teachers to college first and
#                 then add to CLASSROOM.
#                 Rejected teacher list : {rejected_teacher_mails}
#                 """,
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],
#                 "",
#             )
#         AllowedTeacherClassroomLevel.objects.bulk_create(list_of_teachers)
#         email_list = df["email"].to_list()
#         subject = "Teacher Account Associated With Classroom"
#         prompt = (
#             "please use your following mail id to sign up/log in in the Classroom[LMS]"
#         )
#         try:
#             send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
#         except BadHeaderError:
#             print("Could not able to sen emails to students")
#         os.remove(file_abs_path)
#         Classroom.objects.update(allowed_teacher_list="")


# @receiver(post_save, sender=AllowedTeacherClassroomLevel)
# def create_allowed_teacher_for_classroom_level_with_check(
#     sender, instance: AllowedTeacherClassroomLevel, created, **kwargs
# ):
#     if created:
#         is_email_in_allowed_teacher_list = AllowedTeacher.objects.filter(
#             email=instance.email
#         )
#         if not is_email_in_allowed_teacher_list.exists():
#             AllowedTeacherClassroomLevel.objects.filter(email=instance.email).delete()
#             cprint("this teacher email does not associated with any college", "red")
#             raise ValidationError(
#                 "this teacher email does not associated with any college", code=400
#             )


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile(sender, instance: settings.AUTH_USER_MODEL, created, **kwargs):
#     if created:
#         if (
#             AllowedStudents.objects.filter(email=instance.email).exists()
#             and not Student.objects.select_related("user")
#             .filter(user=instance)
#             .exists()
#         ):
#             classroom: Classroom = AllowedStudents.objects.get(
#                 email=instance.email
#             ).classroom
#             university_roll = AllowedStudents.objects.get(
#                 email=instance.email
#             ).university_roll
#             s = Student.objects.create(
#                 university_roll=university_roll, user=instance, classroom=classroom
#             )
#             # TODO: Add some other info also in the mail
#             subject = "Your Student Profile Has Been Created Successfully"
#             msg = f"""
#                 Student ID :{s.id}
#                 mail : {instance.email}
#                 classroom : {classroom.title}

#                 You Can Login After Activation Of your account
#             """
#             send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
#         elif (
#             AllowedTeacher.objects.filter(email=instance.email).exists()
#             and not Teacher.objects.select_related("user")
#             .filter(user=instance)
#             .exists()
#         ):
#             college_detail = College.objects.get(
#                 pk=(
#                     AllowedTeacher.objects.filter(email=instance.email)
#                     .select_related("college")
#                     .values_list("college", flat=True)
#                 )[0]
#             )
#             from termcolor import cprint

#             cprint(college_detail, "red")
#             t = Teacher.objects.create(user=instance, college=college_detail)
#             subject = "Your Teacher Profile Has Been Created Successfully"
#             msg = f"""
#                 Teacher ID :{t.id}
#                 mail : {instance.email}

#                 You Can Login After Activation Of your account
#             """
#             send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
#         elif (
#             AllowedCollegeDBA.objects.filter(email=instance.email).exists()
#             and not CollegeDBA.objects.select_related("user")
#             .filter(user=instance)
#             .exists()
#         ):
#             from termcolor import cprint

#             # cprint("In DBA Creation", "red")
#             college_detail: College = College.objects.get(
#                 pk=(
#                     AllowedCollegeDBA.objects.filter(email=instance.email)
#                     .select_related("college")
#                     .values_list("college", flat=True)
#                 )[0]
#             )

#             # cprint(college_detail, "red")
#             is_owner = False
#             if instance.email == college_detail.owner_email_id:
#                 is_owner = True
#             # cprint(f"is owner --> [ {is_owner} ]", "red")
#             t: CollegeDBA = CollegeDBA.objects.create(
#                 user=instance, college=college_detail, is_owner=is_owner
#             )
#             subject = "Your DBA Profile Has Been Created Successfully"
#             msg = f"""
#                 COLLEGE DBA ID :{t.id}
#                 mail : {instance.email}

#                 You Can Login After Activation Of your account
#             """
#             send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
#         elif instance.is_superuser or instance.is_staff:  # ADMIN
#             print("Admin")
#         else:
#             subject = "Profile Creation Failed"
#             msg = f"""
#                 You have not been assigned any class, but your account has been created.
#                 So to create a profile contact ADMIN

#                 contact mail id: {settings.EMAIL_HOST_USER}
#             """
#             # FIXME: Delete below line of code if gives error
#             User.objects.filter(pk=instance.id).delete()
#             send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])


# @shared_task
# @receiver(post_delete, sender=Student)
# def delete_user_on_student_delete(sender, instance: Student, **kwargs):
#     user = User.objects.filter(pk=instance.user.id)
#     if user.exists():
#         user.delete()


# @shared_task
# @receiver(post_delete, sender=CollegeDBA)
# def delete_user_on_dba_delete(sender, instance: CollegeDBA, **kwargs):
#     user = User.objects.filter(pk=instance.user.id)
#     if user.exists():
#         user.delete()


# @shared_task
# @receiver(
#     post_delete, sender=Teacher
# )  # FIXME: Off this code if teacher removal from class deletes user
# def delete_user_on_teacher_delete(sender, instance: Teacher, **kwargs):
#     user = User.objects.filter(pk=instance.user.id)
#     if user.exists():
#         user.delete()


# @shared_task
# @receiver(post_save, sender=Teacher)
# def auto_join_teacher_to_classes(sender, instance: Teacher, created, **kwargs):
#     # from termcolor import cprint

#     if created:
#         qset = Classroom.objects.prefetch_related("allowed_teachers").filter(
#             allowed_teachers__email=instance.user.email
#         )
#         # cprint(list(qset), "blue")
#         try:
#             instance.classrooms.add(*qset)
#         except:
#             pass
#             # cprint("already assigned classrooms to teacher ", "yellow")


# @receiver(
#     post_save, sender=AllowedTeacherClassroomLevel
# )  # FIXME: classroom pre signed up teachers are not saving
# def assign_classroom_to_existing_teacher(
#     sender, instance: AllowedTeacherClassroomLevel, created, **kwargs
# ):
#     from termcolor import cprint

#     t = (
#         "assign_classroom_to_existing_teacher "
#         + instance.email
#         + "\n---> "
#         + str(created)
#     )
#     cprint(t, "red")
#     if created:
#         classroom: Classroom = Classroom.objects.select_related("college").get(
#             pk=instance.classroom.id
#         )
#         cprint(classroom, "red")
#         teacher_query = Teacher.objects.select_related("user").filter(
#             user__email=instance.email
#         )
#         cprint(str(teacher_query.exists()) + " -> " + instance.email, "blue")
#         if teacher_query.exists():
#             teacher = teacher_query.first()
#             from django.db import transaction

#             with transaction.atomic():
#                 classroom.teachers.add(teacher)
#                 classroom.save(force_update=True)
#             for tchr in classroom.teachers.all():
#                 cprint("Classrooms of teacher -> ", "cyan")
#                 cprint(tchr, "cyan")
#             owner_mail_id = classroom.college.owner_email_id
#             cprint(f"owner mail id --> {owner_mail_id}", "red")
#             subject = "Sir You have been Assigned A new Class"
#             msg = f"Classroom - {classroom.title}"
#             send_mail(subject, msg, owner_mail_id, [instance.email])


# @shared_task
# @receiver(post_delete, sender=AllowedTeacherClassroomLevel)
# def remove_class_after_removal_of_assigned_teacher(
#     sender, instance: AllowedTeacherClassroomLevel, **kwargs
# ):
#     """
#     this removes the classroom from the teacher if teacher
#     has been removed from allowed class room level
#     """
#     classroom: Classroom = Classroom.objects.select_related("college").get(
#         pk=instance.classroom.id
#     )
#     teacher_query = Teacher.objects.select_related("user").filter(
#         user__email=instance.email
#     )
#     if teacher_query.exists():
#         teacher_query.first().classrooms.remove(classroom)
#         subject = "Sir You have been Removed From A Class"
#         msg = f"Classroom - {classroom.title}"
#         owner_mail_id = classroom.college.owner_email_id
#         cprint(f"owner mail id --> {owner_mail_id}", "red")
#         send_mail(subject, msg, owner_mail_id, [instance.email])


# @shared_task
# @receiver(post_save, sender=College)
# def create_allowed_dba(sender, instance: College, created, **kwargs):
#     if created:
#         is_owner_of_college_exists = AllowedCollegeDBA.objects.filter(
#             email=instance.owner_email_id
#         ).exists()
#         if is_owner_of_college_exists:
#             from rest_framework import status

#             raise ValidationError(
#                 detail=f"""
#                 college owner {instance.owner_email_id} already associated with
#                 college - {instance.name}""",
#                 code=status.HTTP_400_BAD_REQUEST,
#             )
#         else:
#             AllowedCollegeDBA.objects.create(
#                 college=instance, email=instance.owner_email_id
#             )
#             subject = f"Welcome to {instance.name}"
#             body = f"""
#                 You are the owner admin of college {instance.name}
#                 Now you can sign up with mail id - {instance.owner_email_id}
#                 ----------------
#                 NB: Only you will be able to add other DBAs or remove them
#             """
#             send_mail(
#                 subject, body, settings.EMAIL_HOST_USER, [instance.owner_email_id]
#             )
#         if instance.allowed_dba_list == None:
#             College.objects.filter(
#                 pk=instance.id
#             ).delete()  # FIXME: Delete this line if not works
#             send_mail(
#                 "Allowed DBA List Does Not Exists",
#                 "You Have To Create Allowed DBAs Manually",
#                 settings.EMAIL_HOST_USER,
#                 ["dba@admin.com"],  # FIXME: Send mail to session dba
#             )
#             return None
#         file_abs_path = None
#         dba_file_path = os.path.join(
#             settings.BASE_DIR,
#             settings.MEDIA_ROOT,
#             instance.allowed_dba_list.name,
#         )
#         if os.path.exists(dba_file_path):
#             file_abs_path = os.path.abspath(dba_file_path)
#         else:
#             send_mail(
#                 "Allowed Teacher List Does Not Exists",
#                 "You Have To Create Allowed Teachers Manually",
#                 settings.EMAIL_HOST_USER,
#                 [instance.owner_email_id],
#             )
#             return None

#         df = None
#         if str(file_abs_path).split(".")[-1] == "csv":
#             df: pd.DataFrame = pd.read_csv(file_abs_path)
#         elif str(file_abs_path).split(".")[-1] == "xlsx":
#             df = pd.read_excel(file_abs_path)

#         if not "email" in df.columns:
#             send_mail(
#                 "Wrong File Structure",
#                 "column name should be => 'email' ",
#                 settings.EMAIL_HOST_USER,
#                 [instance.owner_email_id],  # FIXME: Send mail to session dba
#             )
#             return None
#         df_dict = df.to_dict("records")
#         if len(df_dict) < 1:

#             raise ValidationError(
#                 detail="Please give at least one mail-id in the fail "
#             )

#         # print(df_dict)
#         list_of_teachers = [
#             AllowedCollegeDBA(college=instance, **args)
#             for args in df.to_dict("records")
#         ]
#         AllowedCollegeDBA.objects.bulk_create(list_of_teachers)
#         email_list = df["email"].to_list()
#         subject = "Open Your DBA Account"
#         prompt = "please use your following mail id to sign up in the Classroom[LMS]"
#         try:
#             send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
#         except BadHeaderError:
#             print("Could not able to send emails to DBAs")
#         os.remove(file_abs_path)
#         instance.allowed_teacher_list = ""
#         instance.allowed_dba_list = ""
