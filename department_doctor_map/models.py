from django.db import models

# Create your models here.
from django.db import models

from doctor.models import Doctor
from department.models import Department

# Create your models here.
class DepartmentDoctorMap(models.Model):
    department_doctor_id = models.AutoField(verbose_name='department_doctor_id', primary_key=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'department_doctor_map'

    def __str__(self):
        return self.name