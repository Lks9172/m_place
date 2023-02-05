from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Doctor


# Create your views here.
def cal_intersection(a, b, i):
    raw_set = set()
    for idx in b:
        raw_set.add(idx[0])

    if i == 0:
        return raw_set
    return a&raw_set

@api_view(['GET'])
def search_doctor(request):
    params = request.query_params
    keyword = params.get('string').split(' ')

    doctor = set()
    for (idx, word) in enumerate(keyword):
        raw = Doctor.search_keyword(word)
        doctor = cal_intersection(doctor, raw, idx)

    doctors = Doctor.get_doctor(list(doctor))

    return Response(doctors)
