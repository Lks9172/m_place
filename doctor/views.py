from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
from datetime import time, date
from doctor.models import Doctor
from treatment.date_utils import get_weekday_by_str

# Create your views here.
def cal_intersection(a, b, i):
    raw_set = set()
    for idx in b:
        raw_set.add(idx[0])

    if i == 0:
        return raw_set
    return a&raw_set

def check_working_time(doctor, weekday, target_time):
    if not doctor[f'{weekday}_treatment_start'] and doctor[f'{weekday}_treatment_start']:
        return False
    elif weekday == 'weekday':
        if doctor[f'{weekday}_treatment_start'] < target_time\
            and target_time < doctor['lunch_start'] or\
            doctor['lunch_end'] < target_time and target_time < doctor[f'{weekday}_treatment_end']:
            return True
        else:
            return False
    else:
        if doctor[f'{weekday}_treatment_start']  < target_time and target_time < doctor[f'{weekday}_treatment_end']:
            return True
        else:
            return False

@api_view(['GET'])
def search_doctor(request):
    params = request.query_params
    flag =   params.get('flag') if params.get('flag') else None
    if flag == 'string' and params.get('string'):
        keyword =  params.get('string').split(' ') if params.get('string') else None
        doctor = set()

        if keyword:
            for (idx, word) in enumerate(keyword):
                raw = Doctor.search_keyword(word)
                doctor = cal_intersection(doctor, raw, idx)

            doctors = Doctor.get_doctor(list(doctor))
            return Response(doctors)
        else:
            Response('invalid value error', status=400)
    elif flag == 'date' and params.get('date'):
        date_info = re.sub(r'[^0-9 오전후]', '', params.get('date') if params.get('date') else None)
        date_info = {
            'year': int(date_info.split(' ')[0]),
            'month': int(date_info.split(' ')[1]),
            'day': int(date_info.split(' ')[2]),
            'hour': int(re.sub(r'[^0-9]', '', date_info.split(' ')[3])) if '오전' in date_info.split(' ')[3] else int(re.sub(r'[^0-9]', '', date_info.split(' ')[3]))+12,
        }
        day = date(date_info.get('year'), date_info.get('month'), date_info.get('day')).weekday()
        target_time = time(date_info.get('hour'), 0, 0)
        weekday = get_weekday_by_str(day)

        doctors = Doctor.get_doctor_working_time(weekday)
        doctors = list(filter(lambda x: check_working_time(x, weekday, target_time), doctors))
        doctors = Doctor.get_doctor_info(list(map(lambda x: x['id'], doctors)))
        return Response(doctors)
    return Response('invalid value error', status=400)
