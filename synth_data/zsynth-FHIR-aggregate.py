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

# DATA_PATH = os.path.join('.', 'Willard975_Brown30_e3a61b11-7beb-42b5-b1dd-e33e84d33183.json')
# #
# with open(DATA_PATH) as f:
#     json_data = json.load(f)

error_num = 0

now = datetime.datetime.utcnow()
now = now.date()

df = pd.DataFrame(data = [[0,0,0,0,0,0]],columns = ['Black', 'Age', 'Female', 'L_wall', 'L_wall_thickness', 'Edema'])

for file in os.listdir(r'C:\Users\bertc\Documents\GitHub\ETHWaterloo-AI\synth_data'):
    try:
        data_black = 0
        data_years = 0
        data_gender = 0
        data_l_wall = 0
        data_l_wall_thickness = 0
        data_edema = 0

        print(file)
        risk_score = 0
        DATA_PATH = os.path.join('.', file)
        with open(DATA_PATH) as f:
            json_data = json.load(f)

        for z in json_data['entry']:

            ### Patient
            if z['resource']['resourceType'] == 'Patient':
                ### RACE
                if z['resource']['extension'][0]['valueCodeableConcept']['coding'][0]['display'] == 'Black or African American':
                    data_black = 1
                    risk_score = risk_score + 2

                # pprint.pprint(z['resource']['extension'][0]['valueCodeableConcept']['coding'][0]['display'])

                ### Age
                birth_day_datetime_obj = parser.parse(z['resource']['birthDate'])
                age = dateutil.relativedelta.relativedelta(now,birth_day_datetime_obj)

                if age.years >= 85:
                    risk_score = risk_score + 4
                elif 50 <= age.years < 85:
                    risk_score = risk_score + 2
                elif 35 <= age.years < 50:
                    risk_score = risk_score + 1

                data_years = age.years
                # print(age.years + " years old")
                # patient_age_in_days = age.years*365 + age.months*31 + age.days
                # print(patient_age_in_days)

                ### Gender
                if z['resource']['gender'] == 'female':
                    risk_score = risk_score + 1
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
                    if data_l_wall_thickness >= 15:
                        risk_score = risk_score + 5
                        # print('thicccc wall')
                    elif 14.5 <= data_l_wall_thickness < 15:
                        risk_score = risk_score + 3
                        # print("thicc wall")
                    elif 14 <= data_l_wall_thickness < 14.5:
                        risk_score = risk_score + 2

            ### CLaims
            elif z['resource']['resourceType'] == 'Claim':
                ### Edema
                try:
                    if z['resource']['diagnosis'][1]['diagnosis']['display'] == 'peripheral edema':
                        risk_score = risk_score + 4
                        data_edema = 1
                except:
                    # data_edema = 0
                    error_num = error_num + 1

        # print(risk_score)
        # data = [[data_black, data_years, data_gender, data_l_wall, data_l_wall_thickness, data_edema]]
        new_row = {'Black':data_black, 'Age':data_years, 'Female':data_gender, 'L_wall':data_l_wall, 'L_wall_thickness':data_l_wall_thickness, 'Edema':data_edema}
        df = df.append(new_row, ignore_index = True)
        # print(df)
    except:
        error_num = error_num + 1

df = df.drop([0])
print(df)

df.to_csv('ATTR_dataset.csv')
