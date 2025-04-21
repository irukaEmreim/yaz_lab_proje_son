from django.db import models

class Jury(models.Model):
    id = models.AutoField(primary_key=True)
    announcement_id = models.IntegerField()
    jury_member_id = models.IntegerField()
    assigned_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'juries'