# -*- coding: utf-8 -*-
"""
Save PRT as TSV file
Assuming the data has been saved according to the BIDS definition and that
the PRTs shall be saved in the rawdata/func folder of each participant and session
"""

__author__ = "Judith Eck"
__version__ = "0.1.0"
__date__ = "16-01-2023"
__name__ = "ConvertPRTsInCurrentFoldertoTSV_CopyToFunc.py"

# =============================================================================
# Import required packages
# =============================================================================

import numpy as np
import bvbabel
import os.path
import shutil

# Define folder structure and file identifiers
project_path = 'H:/AppleGame/rawdata/'
# I am assuming that the PRTs are saved in a subdirectory where the original DCM data has been saved, e.g. C:\Users\JEck\Downloads\RomainPetit\UCL2_146\prts
PRT_path = 'H:/AppleGame/PRTfiles/'
PRT_folder_name = '/prts'
sub_folder_name = 'UCL2_'  # I am assuming here the following subject naming folder convention that you have provided as example: UCL2_146
subjects = [146]
ses_id = 'ses-01'

# specify the repetion time
TR = 1.7  # specified in seconds

# loop over all subjects, sessions and runs
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    print(sub_id)
    prts = []
    prt_path_sub = PRT_path + sub_folder_name + str(subjects[sub]) + PRT_folder_name

    # get all PRTfiles in the directory 'prts' in the subjects folder UCL2_146
    for name in os.listdir(prt_path_sub):
        if (os.path.isfile(os.path.join(prt_path_sub, name))) and name.endswith('.prt'):
            prts.append(prt_path_sub + '/' + name)

    for prtfile in prts:
        # Read the PRT file, convert it to _events.tsv and save in the func folder in rawdata
        # prtfile = project_path + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id +  '_' + task_name + '_' + run_id + '.prt'
        prt_header, prt_data = bvbabel.prt.read_prt(prtfile)
        temp = np.empty(shape=(0, 3), dtype=str)

        for cond in range(len(prt_data)):
            if prt_header['ResolutionOfTime'] == 'msec':
                prt_data[cond]['Time start'] = np.int_(prt_data[cond]['Time start']) / 1000
                prt_data[cond]['Time stop'] = np.int_(prt_data[cond]['Time stop']) / 1000
            else:
                prt_data[cond]['Time start'] = ((prt_data[cond]['Time start']) - 1) * TR
                prt_data[cond]['Time stop'] = prt_data[cond]['Time stop'] * TR
            duration = np.round(np.subtract(prt_data[cond]['Time stop'], prt_data[cond]['Time start']), decimals=4)
            onset = prt_data[cond]['Time start']
            event_name = np.repeat(prt_data[cond]['NameOfCondition'], len(prt_data[cond]['Time start']))
            temp = np.append(temp, np.array([onset.astype(str), duration.astype(str), event_name.astype(str)]).T,
                             axis=0)
            del (duration, onset, event_name)
        np.savetxt((prtfile.split('.')[0] + '_events.tsv'), temp, fmt='%s', delimiter='\t',
                   header='onset\tduration\ttrial_type', comments='')
        del (prt_header, prt_data, temp)

    # copy all PRT and TSV files to the func folder in the raw directory
    sourcepath = prt_path_sub + '/'
    destpath = project_path + sub_id + '/' + ses_id + '/func/'
    for name in os.listdir(prt_path_sub):
        if (os.path.isfile(os.path.join(prt_path_sub, name))) and name.endswith('.tsv'): #original: and (name.endswith('.prt') or name.endswith('.tsv')):
            shutil.copy(sourcepath + name, destpath + name)




