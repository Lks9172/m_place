from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Doctor, Patient, Treatment
from .date_utils import get_treatement_date, get_expiration_date, get_date_info


# Create your views here.
@api_view(['GET', 'POST', 'PUT'])
def generate_trearment(request):
    if request.method == 'GET':
        doctor_id = request.data.get('doctor_id')
        treatment = Treatment.objects.filter(doctor_id = doctor_id, success_flag = False)
        res = list(map(lambda x: x.get_dict(), treatment))

        return Response(res)

    elif request.method == 'PUT':
        treatment_id = request.data.get('treatment_id')
        try:
            treatment = Treatment.objects.get(treatment_id = treatment_id, success_flag = False)
            treatment.success_flag = True
            treatment.save()
        except Treatment.DoesNotExist:
            return Response('Not Found Error', status=404)
        treatment = treatment.get_dict()
        
        return Response({
            'treatment_id': treatment['treatment_id'],
            'patient_name': treatment['patient_name'],
            'treatment_time': treatment['treatment_time'],
            'end_time': treatment['end_time']
        })

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
        if not treatement_datetime:
            return Response('의사의 영업시간이 아님', status=400)
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
