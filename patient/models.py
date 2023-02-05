from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(verbose_name='p_id', primary_key=True)
    name = models.CharField(verbose_name='이름', max_length=8, null=False)

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return self.name