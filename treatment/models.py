from django.db import models

from doctor.models import Doctor
from patient.models import Patient

# Create your models here.
class Treatment(models.Model):
    treatment_id = models.AutoField(verbose_name='treatment_id', primary_key=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    success_flag = models.BooleanField(verbose_name='성공flag', null=False, default=False)
    treatment_time = models.DateTimeField(verbose_name='진료희망시간', null=True)
    end_time = models.DateTimeField(verbose_name='예약요청만료시간', null=True)
    

    class Meta:
        db_table = 'treatment'

    def get_dict(self):
        return {
            'treatment_id': self.treatment_id,
            'doctor_name': self.doctor_id.name,
            'success_flag': self.success_flag,
            'patient_name': self.patient_id.name,
            'treatment_time': self.treatment_time,
            'end_time': self.end_time
        }

    def __str__(self):
        return f'{self.treatment_id}'