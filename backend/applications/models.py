from django.db import models

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    announcement_id = models.IntegerField()
    candidate_id = models.IntegerField()
    assigned_to = models.IntegerField(null=True)
    status = models.CharField(max_length=15)
    submitted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'applications'


class ApplicationActivity(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey('Application', db_column='application_id', on_delete=models.CASCADE)
    faaliyet_kodu = models.CharField(max_length=10)   # ✅ bunu ekle
    adet = models.IntegerField()                      # ✅ bunu da ekle
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'application_activities'




class ApplicationDocument(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey('Application', db_column='application_id', on_delete=models.CASCADE)
    file_path = models.TextField()
    description = models.TextField()
    uploaded_at = models.DateTimeField()
    faaliyet_kodu = models.CharField(max_length=10, null=True, blank=True)  # 🔥 yeni eklenen alan

    class Meta:
        managed = False
        db_table = 'application_documents'


from announcements.models import AcademicAnnouncement
from users.models import User

class Jury(models.Model):
    id = models.AutoField(primary_key=True)
    announcement = models.ForeignKey(AcademicAnnouncement, on_delete=models.CASCADE)
    jury_member = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'juries'

class JuryReport(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id')
    jury_member = models.ForeignKey(User, on_delete=models.CASCADE, db_column='jury_member_id')
    evaluation_result = models.CharField(max_length=10)  # 'olumlu' veya 'olumsuz'
    report_file_path = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)  # Jüri üyesinin eklemek istediği açıklama
    class Meta:
        managed = False  # Çünkü biz kendi SQL ile tablo oluşturduk
        db_table = 'jury_reports'