# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcademicActivitie(models.Model):
    application = models.ForeignKey('Applications', on_delete=models.CASCADE, blank=True, null=True)
    activity_type = models.CharField(max_length=50, blank=True, null=True)
    activity_name = models.CharField(max_length=255, blank=True, null=True)
    activity_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    activity_metadata = models.JSONField(blank=True, null=True)
    activity_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'academic_activities'


class AcademicAnnouncement(models.Model):
    title = models.CharField(max_length=255)
    position_type = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'academic_announcements'


class ApplicationCriteria(models.Model):
    announcement = models.ForeignKey(AcademicAnnouncements, on_delete=models.CASCADE, blank=True, null=True)
    criteria = models.JSONField()
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application_criteria'


class ApplicationDocument(models.Model):
    application = models.ForeignKey('Applications', on_delete=models.CASCADE, blank=True, null=True)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    file_url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application_documents'


class Application(models.Model):
    announcement = models.ForeignKey(AcademicAnnouncements, on_delete=models.CASCADE, blank=True, null=True)
    candidate = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    jury_evaluation_completed = models.BooleanField(blank=True, null=True)
    final_decision = models.CharField(max_length=20, blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    finalized_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applications'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUserUserPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Jury(models.Model):
    announcement = models.ForeignKey(AcademicAnnouncements, on_delete=models.CASCADE, blank=True, null=True)
    jury_member = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    assigned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juries'
        unique_together = (('announcement', 'jury_member'),)


class JuryReport(models.Model):
    application = models.ForeignKey(Applications, on_delete=models.CASCADE, blank=True, null=True)
    jury_member = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    evaluation_result = models.CharField(max_length=10, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    report_file_path = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jury_reports'


class Notification(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class User(models.Model):
    tc_kimlik_no = models.CharField(unique=True, max_length=11)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10)
    is_active = models.BooleanField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
