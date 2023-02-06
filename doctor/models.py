from django.db import models
from django.db import connection

# Create your models here.
class Doctor(models.Model):
    doctor_id = models.AutoField(verbose_name='doctor_id', primary_key=True)
    name = models.CharField(verbose_name='이름', max_length=8, null=False)
    hospital_name = models.CharField(verbose_name='병원이름', max_length=20, null=False)
    weekday_treatment_start = models.TimeField(verbose_name='평일진료시작시간', null=True)
    weekday_treatment_end = models.TimeField(verbose_name='평일진료종료시간', null=True)
    saturday_treatment_start = models.TimeField(verbose_name='토요일진료시작시간', null=True)
    saturday_treatment_end = models.TimeField(verbose_name='토요일진료시작시간', null=True)
    sunday_treatment_start = models.TimeField(verbose_name='일요일진료시작시간', null=True)
    sunday_treatment_end = models.TimeField(verbose_name='일요일진료시작시간', null=True)
    lunch_start = models.TimeField(verbose_name='점심시간시작시간', null=True)
    lunch_end = models.TimeField(verbose_name='점심시간시작시간', null=True)


    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.name
    
    def search_keyword(keyword):
        with connection.cursor() as cursor:
            cursor.execute(f'''	SELECT 
                doctor_id
            FROM m_place.doctor as doctor
            left join m_place.department_doctor_map as ddm
            on doctor.doctor_id = ddm.doctor_id_id
            left join m_place.department as depart
            on ddm.department_id_id = depart.department_id
            where concat(doctor.name, doctor.hospital_name, depart.name) regexp '{keyword}' 
            or depart.alias like '{keyword}'
            group by doctor_id
            ''')
            row = cursor.fetchall()
        return row

    def get_doctor(ids):
        rows = []
        with connection.cursor() as cursor:
            for id in ids:
                cursor.execute(f'''	SELECT 
                    doctor_id, 
                    doctor.name as doctor_name,
                    doctor.hospital_name,
                    doctor.weekday_treatment_start,
                    doctor.weekday_treatment_end,
                    doctor.saturday_treatment_start,
                    doctor.saturday_treatment_end,
                    doctor.sunday_treatment_start,
                    doctor.sunday_treatment_end,
                    doctor.lunch_start,
                    doctor.lunch_end,
                    depart.name,
                    depart.alias,
                    depart.health_insurance
                    FROM m_place.doctor as doctor
                inner join m_place.department_doctor_map as ddm
                on doctor.doctor_id = ddm.doctor_id_id
                inner join m_place.department as depart
                on ddm.department_id_id = depart.department_id
                where doctor_id = '{id}'
                ''')
                rows.append(cursor.fetchall())
        
        doctors = []
        for (idx, id) in enumerate(ids):
            doctors.append(list(filter(lambda x:x[0] == id, rows[idx])))
            doctors[idx] = {
                'id': doctors[idx][0][0],
                'name': doctors[idx][0][1],
                'hospital_name': doctors[idx][0][2],
                'weekday_treatment_start': doctors[idx][0][3],
                'weekday_treatment_end': doctors[idx][0][4],
                'saturday_treatment_start': doctors[idx][0][5],
                'saturday_treatment_end': doctors[idx][0][6],
                'sunday_treatment_start': doctors[idx][0][7],
                'sunday_treatment_end': doctors[idx][0][8],
                'lunch_start': doctors[idx][0][9],
                'lunch_end': doctors[idx][0][10],
                'depart': (doctors[idx][0][12] if doctors[idx][0][12] else doctors[idx][0][11]),
                'health_insurance': doctors[idx][0][13],
            }
        
        return doctors
    
    def get_doctor_working_time(weekday):
        with connection.cursor() as cursor:
            cursor.execute(f'''	SELECT 
                doctor_id, 
                doctor.name as doctor_name,
                doctor.hospital_name,
                doctor.{weekday}_treatment_start,
                doctor.{weekday}_treatment_end,
                doctor.lunch_start,
                doctor.lunch_end
                FROM m_place.doctor as doctor
                where doctor.{weekday}_treatment_start is not null and 
                doctor.{weekday}_treatment_end is not null
            ''')
            rows = list(cursor.fetchall())
        
            for (idx, row) in enumerate(rows):
                rows[idx] = {
                    'id': row[0],
                    'name': row[1],
                    'hospital_name': row[2],
                    'weekday_treatment_start': row[3],
                    'weekday_treatment_end': row[4],
                    'lunch_start': row[5],
                    'lunch_end': row[6],
                }
        
            return rows
    
    def get_doctor_info(ids):
        rows = []
        with connection.cursor() as cursor:
            for id in ids:
                print(id)
                cursor.execute(f'''	SELECT 
                    doctor_id, 
                    doctor.name as doctor_name,
                    doctor.hospital_name,
                    doctor.weekday_treatment_start,
                    doctor.weekday_treatment_end,
                    doctor.saturday_treatment_start,
                    doctor.saturday_treatment_end,
                    doctor.sunday_treatment_start,
                    doctor.sunday_treatment_end,
                    doctor.lunch_start,
                    doctor.lunch_end
                    FROM m_place.doctor as doctor
                where doctor_id = '{id}'
                ''')
                rows.append(cursor.fetchone())
        
            for (idx, row) in enumerate(rows):
                rows[idx] = {
                    'id': row[0],
                    'name': row[1],
                    'hospital_name': row[2],
                    'weekday_treatment_start': row[3],
                    'weekday_treatment_end': row[4],
                    'saturday_treatment_start': row[5],
                    'saturday_treatment_end': row[6],
                    'sunday_treatment_start': row[7],
                    'sunday_treatment_end': row[8],
                    'lunch_start': row[9],
                    'lunch_end': row[10],
                }
        
            return rows