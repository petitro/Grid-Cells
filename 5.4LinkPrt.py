# -*- coding: utf-8 -*-
"""
Created 2023-05-03

@author: JEck
"""

# Import required packages
import os.path

# Define folder structure and file identifiers
project_path = 'C:/Users/Jeck/Documents/BrainVoyager/Projects/RomainPetit/derivatives/'
file_ending = '_bold_3DMCTS_SCCTBL_256_sinc_2x1.0_MNI.vtc'
anat_folder = 'workflow_id-2_type-3_name-anat-normalization/'
anat_ending = '_T1w_IIHC_MNI.vmr'
vtc_folder = 'workflow_id-5_type-5_name-func-normalization/'
prt_folder = 'rawdata_bv/'

subjects = [1]
runs = []
sessions = [1]
task_name = 'task-untitled'

# loop over all subjects, sessions and runs
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    for ses in range(len(sessions)):
        ses_id = 'ses-' + f'{sessions[ses]:02d}'

        # identify the number of runs in folder
        for name in os.listdir(project_path + vtc_folder + sub_id + '/' + ses_id + '/func/'):
            if name.endswith(file_ending):
                runs.append(int(name.split('run-')[1][:2]))

        for run in range(len(runs)):
            run_id = 'run-' + f'{runs[run]:02d}'
            file_folder = vtc_folder
            doc = brainvoyager.open(
                project_path + anat_folder + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + anat_ending)
            doc.link_vtc(
                project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + file_ending)
            doc.link_protocol(
                project_path + prt_folder + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '.prt')
            doc.save_vtc(
                project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + file_ending)
            doc.close()

        runs = []