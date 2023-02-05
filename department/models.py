from django.db import models

# Create your models here.
class Department(models.Model):
    department_id = models.AutoField(verbose_name='d_id', primary_key=True)
    name = models.CharField(verbose_name='이름', max_length=20, null=False)
    alias = models.CharField(verbose_name='별칭', max_length=20, null=True)
    health_insurance = models.BooleanField(verbose_name='건강보험 적용여부', null=False)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name