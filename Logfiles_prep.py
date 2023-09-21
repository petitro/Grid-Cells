# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 11:56:55 2023

@author: Romain PETIT
"""
import csv
import re
import numpy as np
import pandas as pd


def round_to_5(number):
    return round(number / 5) * 5


def prep_log(input_file):
    # Define a regular expression pattern to match the expected format
    pattern = r'^-?\d{1,3},\d{3}\.\d{3}$'

    # Set the name of the input file
    output_file = input_file + '.txt'
    output_xls = input_file + '.xlsx'

    # Read the data from the input file into a dictionary
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        data = {}
        t0 = 0
        for row in reader:
            for column, value in row.items():
                data.setdefault(column, [])
                if (column == 'time'):
                    if (re.match(pattern, value) != None):
                        value = value.replace(",", "")
                    if (t0 == 0):
                        t0 = float(value)
                    value = float(value) - t0
                    data[column].append(value)
                elif column in ['feedback', 'phasetype', 'subtask']:
                    data[column].append(int(value))
                elif re.match(pattern, value) != None and column != 'time':
                    s = value.replace(",", "")
                    data[column].append(float(s))
                elif (column == 'yaw'):
                    angle = float(value)+180
                    angle = round_to_5(angle)
                    data[column].append(angle)
                else:
                    data[column].append(float(value))

    # Calculate the velocities
    dt = np.diff(data['time'])
    dx = np.diff(data['x'])
    dy = np.diff(data['y'])
    vx = np.concatenate(([0], dx / dt))
    vy = np.concatenate(([0], dy / dt))
    v = np.sqrt(vx ** 2 + vy ** 2)

    # Add velocities to the dictionary
    data['vx'] = vx
    data['vy'] = vy
    data['v'] = v

    # Calculate the delta angle
    dyaw = np.diff(data['yaw'])
    dyaw = np.concatenate(([0], dyaw))
    data['dyaw'] = dyaw
    dt = np.concatenate((dt, [0]))
    data['dt'] = dt

    # Select only the desired columns
    cols_selected = ['time', 'dt', 'v', 'dyaw', 'yaw', 'phasetype', 'feedback', 'x', 'vx', 'y', 'vy', 'z', 'subtask','triggercount']
    dico = {col: data[col] for col in cols_selected}

    # Create a pandas dataframe from the dictionary
    df = pd.DataFrame.from_dict(dico)

    # Write the dataframe to an Excel file
    with pd.ExcelWriter(output_xls, engine='openpyxl') as writer:
        df.to_excel(writer,index=False)
    #df.to_excel(output_xls, index=False)

    return df


################################################################################################################
"""
# Write the filtered data to a new text file
with open(output_file, 'w') as file:
    for i in range(len(data['phasetype'])):
        if data['phasetype'][i] == 0 and data['feedback'][i] == -1:
            file.write(f'Croix&Etoiles;{data["time"][i]};{data["feedback"][i]}\n')
            # Use double quotes inside the f-string to avoid syntax errors caused by using single quotes inside the single-quoted string.
            # Use string '0' and '-1' instead of integer 0 and -1 as they seem to be strings in the data.
"""