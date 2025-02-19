"""Let's build 3 function to calculate TRIMP, TRIMP_LT and HRRS. HRRS = TRIMP/TRIMP_LT.
TRIMP = =(((AVG_HR-REST_HR)/(MAX_HR-REST_HR))*0,64*EXP(((AVG_HR-REST_HR)/(MAX_HR-REST_HR))*1,92)*workout_duration)
TRIMP_LT = =(((LT_HR-REST_HR)/(MAX_HR-REST_HR))*0,64*EXP(((LT_HR-REST_HR)/(MAX_HR-REST_HR))*1,92)*LT_duration) con LT_duration = workout_duration*0,5 = 60
HRRS = TRIMP/TRIMP_LT*100"""

import math

def validate_input(value):
    if value < 0:
        raise ValueError("Input values must be non-negative")
    return value

# Function trimp
def trimp(avg_hr, max_hr, rest_hr, workout_duration):
    avg_hr = validate_input(avg_hr)
    max_hr = validate_input(max_hr)
    rest_hr = validate_input(rest_hr)
    workout_duration = validate_input(workout_duration)
    trimp_value = (
        ((avg_hr - rest_hr) / (max_hr - rest_hr))
        * 0.64
        * math.exp(((avg_hr - rest_hr) / (max_hr - rest_hr)) * 1.92)
        * workout_duration
    )
    return trimp_value


# Function trimp_lt, workout_duration = 60
def trimp_lt(lt_hr, max_hr, rest_hr, lt_duration=60):
    lt_hr = validate_input(lt_hr)
    max_hr = validate_input(max_hr)
    rest_hr = validate_input(rest_hr)
    lt_duration = validate_input(lt_duration)
    trimp_lt_value = (
        ((lt_hr - rest_hr) / (max_hr - rest_hr))
        * 0.64
        * math.exp(((lt_hr - rest_hr) / (max_hr - rest_hr)) * 1.92)
        * lt_duration
    )
    return trimp_lt_value


# Function hrrs
def hrrs(avg_hr, max_hr, rest_hr, workout_duration, lt_hr):
    avg_hr = validate_input(avg_hr)
    max_hr = validate_input(max_hr)
    rest_hr = validate_input(rest_hr)
    workout_duration = validate_input(workout_duration)
    lt_hr = validate_input(lt_hr)
    hrrs_value = (
        trimp(avg_hr, max_hr, rest_hr, workout_duration)
        / trimp_lt(lt_hr, max_hr, rest_hr)
        * 100
    )
    return hrrs_value
