from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Doctor, Patient, Treatment
from .date_utils import get_treatement_date, get_expiration_date, get_date_info


# Create your views here.
@api_view(['GET', 'POST'])
def generate_trearment(request):
    if request.method == 'GET':
        doctor_id = request.data.get('doctor_id')
        print(doctor_id)
        treatment = Treatment.objects.filter(doctor_id = doctor_id, success_flag = False)
        res = list(map(lambda x: x.get_dict(), treatment))
        return Response(res)
    elif request.method == 'POST':
        doctor = Doctor.objects.get(doctor_id = request.data.get('doctor_id'))
        patient = Patient.objects.get(patient_id = request.data.get('patient_id'))
        datetime_info = {
            'year': request.data.get('year'),
            'month': request.data.get('month'),
            'day': request.data.get('day'),
            'hour': request.data.get('hour'),
            'minutes': request.data.get('minutes'),
        }
        day, treatement_time, now_date, now_time = get_date_info(datetime_info)
        treatement_datetime = get_treatement_date(doctor, datetime_info, day, treatement_time)
        expiration_date = get_expiration_date(now_time, doctor, now_date, day)
        
        treatment = Treatment.objects.create(
                success_flag = False, 
                doctor_id = doctor,
                patient_id = patient,
                treatment_time = treatement_datetime,
                end_time = expiration_date
            )

        res = {
            'treatment_id': treatment.treatment_id,
            'doctor_name': doctor.name,
            'patient_name': patient.name,
            'treatement_day': treatement_datetime,
            'expiration_day': expiration_date,
        }

        return Response(res)
