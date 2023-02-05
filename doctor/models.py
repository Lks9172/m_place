from django.db import models

# Create your models here.
class Doctor(models.Model):
    doctor_id = models.AutoField(verbose_name='doctor_id', primary_key=True)
    name = models.CharField(verbose_name='이름', max_length=8, null=False)
    hospital_name = models.BooleanField(verbose_name='병원이름', null=False)
    weekday_treatment_start = models.DateTimeField(verbose_name='평일진료시작시간', null=True)
    weekday_treatment_end = models.DateTimeField(verbose_name='평일진료종료시간', null=True)
    saturday_treatment_start = models.DateTimeField(verbose_name='토요일진료시작시간', null=True)
    saturday_treatment_end = models.DateTimeField(verbose_name='토요일진료시작시간', null=True)
    sunday_treatment_start = models.DateTimeField(verbose_name='일요일진료시작시간', null=True)
    sunday_treatment_end = models.DateTimeField(verbose_name='일요일진료시작시간', null=True)


    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.name