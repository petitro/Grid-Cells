# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 16:24:16 2023

@author: romai
runs=[]
        for name in os.listdir(project_path + 'rawdata/' + sub_id + '/' + ses_id + '/func/'):
            if name.endswith('_bold.nii.gz'):
                runs.append(int(name[-14:-12]))
"""
import pandas as pd
from Logfiles_prep import prep_log
import os

Sub=29
Project_path='H:/GridcatTest/Vieux/Sub'+str(Sub)+'/'
os.chdir(Project_path)
runs=[1,2,3,4,5]

for j in runs:
    input_file = 'run' + str(j)
    output_file = 'Eventable/run' + str(j) + 'LPI.txt'
    df = prep_log('Eventable/'+input_file)

    # Ouvrir fichier final pour écriture
    file = open(output_file, 'w')

    # retenir la ligne précédente
    name = ""
    time = 0
    duration = 0
    degree = 0
    first = True
    last = len(df) - 1
    LPI=0
    # Parcourir le dataframe ligne par ligne
    for i, row in df.iterrows():
        if (row['phasetype'] == 0):
            if (first == False):
                file.write(f'{name};{round(time, 3)};{round(duration, 3)};{round(degree, 3)}\n')
                first = True
        else:
            if (row['feedback'] != -1):
                if (first == True):
                    name = "feedback"
                    time = row["time"]
                    duration = row["dt"]
                    degree = row["yaw"]
                    first = False
                else:
                    if (name != "feedback"):
                        file.write(f'{name};{round(time, 3)};{round(duration, 3)};{round(degree, 3)}\n')
                        name = "feedback"
                        time = row["time"]
                        duration = row["dt"]
                        degree = row["yaw"]
                    else:
                        duration = duration + row["dt"]
            elif (row['phasetype'] == 5):
                if (first == True):
                    name = "Nextblock"
                    time = row["time"]
                    duration = row["dt"]
                    degree = row["yaw"]
                    first = False
                else:
                    if (name != "Nextblock"):
                        file.write(f'{name};{round(time, 3)};{round(duration, 3)};{round(degree, 3)}\n')
                        name = "Nextblock"
                        time = row["time"]
                        duration = row["dt"]
                        degree = row["yaw"]
                    else:
                        duration = duration + row["dt"]

            elif (row['v'] == 0):
                if (first == True):
                    name = "vnulle"
                    time = row["time"]
                    duration = row["dt"]
                    degree = row["yaw"]
                    first = False
                else:
                    if (name != "vnulle"):
                        file.write(f'{name};{round(time, 3)};{round(duration, 3)};{round(degree, 3)}\n')
                        name = "vnulle"
                        time = row["time"]
                        duration = row["dt"]
                        degree = row["yaw"]
                    else:
                        duration = duration + row["dt"]
            elif (row['v'] != 0):
                if (first == True):
                    if(row['subtask']==3):
                        name = "translationLPI"
                    else:
                        name = "translationPPI"
                    time = row["time"]
                    duration = row["dt"]
                    degree = row["yaw"]
                    first = False
                else:
                    if ((name != "translationLPI" and name != "translationPPI") or degree != row["yaw"]):
                        file.write(f'{name};{round(time, 3)};{round(duration, 3)};{round(degree, 3)}\n')
                        if (row['subtask'] == 3):
                            name = "translationLPI"
                        else:
                            name = "translationPPI"
                        time = row["time"]
                        duration = row["dt"]
                        degree = row["yaw"]
                    else:
                        duration = duration + row["dt"]
            if (i == last):
                #print(row)
                file.write(f'{name};{round(time, 3)};{round(duration, 3)};{round(degree, 3)}\n')
    print(input_file+'Done')
    file.close()

