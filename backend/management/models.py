from django.db import models


class Jury(models.Model):
    id = models.AutoField(primary_key=True)
    announcement_id = models.IntegerField()
    jury_member_id = models.IntegerField()
    assigned_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'juries'


class KadroKriterleri(models.Model):
    bolum = models.ForeignKey('Bolum', on_delete=models.CASCADE)
    unvan = models.CharField(max_length=20)
    faaliyet_kodu = models.CharField(max_length=20)
    asgari_adet = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'kadro_kriterleri'

class PuanKriterleri(models.Model):
    bolum = models.ForeignKey('Bolum', on_delete=models.CASCADE)
    unvan = models.CharField(max_length=30)
    faaliyet_kodu = models.CharField(max_length=20)
    asgari_puan = models.IntegerField(null=True, blank=True)
    azami_puan = models.IntegerField(null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'puan_kriterleri'

class Bolum(models.Model):
    ad = models.CharField(max_length=100, unique=True)
    
    class Meta:
        managed = False
        db_table = 'bolumler'

class FaaliyetPuanlari(models.Model):
    id = models.AutoField(primary_key=True)
    faaliyet_kodu = models.CharField(max_length=10)
    faaliyet_adi = models.TextField()
    aciklama = models.TextField()
    puan = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'faaliyet_puanlari'

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

