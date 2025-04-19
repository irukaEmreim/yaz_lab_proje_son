from django.db import models

class AcademicAnnouncement(models.Model):
    POSITION_CHOICES = [
        ('Dr. Öğr. Üyesi', 'Dr. Öğr. Üyesi'),
        ('Doçent', 'Doçent'),
        ('Profesör', 'Profesör'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    position_type = models.CharField(max_length=30, choices=POSITION_CHOICES)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.IntegerField()  # User ID
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'academic_announcements'

    def __str__(self):
        return f"{self.title} - {self.position_type}"
