from datetime import datetime, timedelta, date, time

def get_weekday_by_str(day):
    if day == 5:
        return 'saturday'
    elif day == 6:
        return 'sunday'
    elif 0 <= day and day < 5:
        return 'weekday'
    return False

def get_treatement_date(doctor, date_info, day, treatement_time):
    if day == 5:
        if not doctor.saturday_treatment_start or not doctor.saturday_treatment_end:
            return False
        if doctor.saturday_treatment_start >  treatement_time or treatement_time > doctor.saturday_treatment_end:
            return False
    elif day == 6:
        if not doctor.sunday_treatment_start or not doctor.sunday_treatment_end:
            return False
        if doctor.sunday_treatment_start >  treatement_time or treatement_time > doctor.sunday_treatment_end:
            return False
    elif 0 <= day and day < 5:
        if not doctor.weekday_treatment_start or not doctor.weekday_treatment_end:
            return False
        if doctor.weekday_treatment_start >  treatement_time or treatement_time > doctor.weekday_treatment_end:
            return False
    return datetime(date_info['year'], date_info['month'], date_info['day'], treatement_time.hour, treatement_time.minute)

def add_datetime_time(d_time, time, minutes):
    res = datetime(d_time.year, d_time.month, d_time.day, time.hour, time.minute)
    return res+timedelta(minutes=minutes)

def get_expiration_date(now_time, doctor, now, day):
    day_info = [
        [[doctor.weekday_treatment_start, doctor.lunch_start],
        [doctor.lunch_end, doctor.weekday_treatment_end]],
        [[doctor.weekday_treatment_start, doctor.lunch_start],
        [doctor.lunch_end, doctor.weekday_treatment_end]],
        [[doctor.weekday_treatment_start, doctor.lunch_start],
        [doctor.lunch_end, doctor.weekday_treatment_end]],
        [[doctor.weekday_treatment_start, doctor.lunch_start],
        [doctor.lunch_end, doctor.weekday_treatment_end]],
        [[doctor.weekday_treatment_start, doctor.lunch_start],
        [doctor.lunch_end, doctor.weekday_treatment_end]],
        [[doctor.saturday_treatment_start, doctor.saturday_treatment_end]
            if doctor.saturday_treatment_start else []],
        [[doctor.sunday_treatment_start, doctor.sunday_treatment_end] 
            if doctor.sunday_treatment_start else []],
    ]
    k_time = 0
    if not day_info[day][0]:
        pass
    elif now_time < day_info[day][0][0]:
        k_time = add_datetime_time(now, day_info[day][0][0], 15)
    elif len(day_info[day]) > 1 and day_info[day][0][1] < now_time and now_time < day_info[day][1][0]:
        k_time = add_datetime_time(now, day_info[day][1][0], 15)
    elif len(day_info[day]) > 1 and day_info[day][1][1] < now_time:
        pass
    else:
        k_time = add_datetime_time(now, now_time, 20)

    if k_time == 0:
        for d in range(day+1, 14):
            d_idx = d%7
            if day_info[d_idx]:
                k_time = add_datetime_time(now, day_info[d_idx][0][0], 15)
                break
    return k_time

def get_date_info(datetime_info):
    day = date(datetime_info.get('year'), datetime_info.get('month'), datetime_info.get('day')).weekday()
    treatement_time = time(datetime_info.get('hour'), datetime_info.get('minutes'), 0)
    now_date = datetime.now()
    now_time = time(now_date.hour, now_date.minute, now_date.second)

    return day, treatement_time, now_date, now_time
