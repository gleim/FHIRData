import warnings
warnings.filterwarnings("ignore")
import os

import numpy as np
import pandas as pd
import json
import pprint

from dateutil import parser
from dateutil import relativedelta
import dateutil
import datetime

DATA_PATH = os.path.join('.', 'Winford225_West559_563bb39d-e88a-471c-9fc7-10b0135e42ce.json')
#
with open(DATA_PATH) as f:
    json_data = json.load(f)

error_num = 0

now = datetime.datetime.utcnow()
now = now.date()

try:
    data_black = 0
    data_years = 0
    data_gender = 0
    data_l_wall = 0
    data_l_wall_thickness = 0
    data_edema = 0

    for z in json_data['entry']:

        ### Patient
        if z['resource']['resourceType'] == 'Patient':
            ### RACE
            if z['resource']['extension'][0]['valueCodeableConcept']['coding'][0]['display'] == 'Black or African American':
                data_black = 1

            ### Age
            birth_day_datetime_obj = parser.parse(z['resource']['birthDate'])
            age = dateutil.relativedelta.relativedelta(now,birth_day_datetime_obj)

            data_years = age.years
            # print(age.years + " years old")
            # patient_age_in_days = age.years*365 + age.months*31 + age.days
            # print(patient_age_in_days)

            ### Gender
            if z['resource']['gender'] == 'female':
                data_gender = 1
                # print('female')
            else:
                data_gender = 0
                # print ('male')

        elif z['resource']['resourceType'] == 'Observation':
            ### Wall thickness
            if z['resource']['code']['coding'][0]['code'] == '125270':
                data_l_wall = 1
                data_l_wall_thickness = z['resource']['valueQuantity']['value']

        ### CLaims
        elif z['resource']['resourceType'] == 'Claim':
            ### Edema
            try:
                if z['resource']['diagnosis'][1]['diagnosis']['display'] == 'peripheral edema':
                    data_edema = 1
            except:
                # data_edema = 0
                error_num = error_num + 1

    # print(risk_score)
    data = [[data_black, data_years, data_gender, data_l_wall, data_l_wall_thickness, data_edema]]
    df = pd.DataFrame(data ,columns = ['Black', 'Age', 'Female', 'L_wall', 'L_wall_thickness', 'Edema'])
    # new_row = {'Black':data_black, 'Age':data_years, 'Female':data_gender, 'L_wall':data_l_wall, 'L_wall_thickness':data_l_wall_thickness, 'Edema':data_edema}
    # df = df.append(new_row, ignore_index = True)
    # print(df)
except:
    error_num = error_num + 1

# df = df.drop([0])
print(df)
