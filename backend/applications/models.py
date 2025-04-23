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

