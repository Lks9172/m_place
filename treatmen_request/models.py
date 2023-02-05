from django.db import models

from doctor.models import Doctor
from patient.models import Patient

# Create your models here.
class TreatmentRequest(models.Model):
    treatment_id = models.AutoField(verbose_name='treatment_id', primary_key=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    success_flag = models.BooleanField(verbose_name='요청만료', null=False, default=False)
    end_time = models.DateTimeField(verbose_name='예약요청만료시간', null=True)
    

    class Meta:
        db_table = 'treatment_request'

    def __str__(self):
        return self.name