# -*- coding: utf-8 -*-
"""
Created on 20-01-2023

@author: JEck
"""

# Import required packages
import os.path

# Define folder structure and file identifiers
project_path = 'H:/AppleGame/'
subjects = [161]
runs = []
sessions = [1]
task_name = 'task-untitled'

# loop over all subjects, sessions and runs
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    for ses in range(len(sessions)):
        ses_id = 'ses-' + f'{sessions[ses]:02d}'
        raw_bv_path = project_path + 'derivatives/rawdata_bv/' + sub_id + '/' + ses_id
        if not os.path.isdir(raw_bv_path):
            os.makedirs(raw_bv_path + '/func/')
            os.makedirs(raw_bv_path + '/anat/')
        doc_vmr = bv.open(
            project_path + 'rawdata/' + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + '_T1w.nii.gz')
        doc_vmr.close()
        doc_vmr = bv.open(
            project_path + 'rawdata/' + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + '_T2w.nii.gz')
        doc_vmr.close()

        # identify the number of runs in folder
        runs=[]
        for name in os.listdir(project_path + 'rawdata/' + sub_id + '/' + ses_id + '/func/'):
            if name.endswith('_bold.nii.gz'):
                runs.append(int(name[-14:-12]))

        for run in range(len(runs)):
            run_id = 'run-' + f'{runs[run]:02d}'
            doc_fmr = bv.open(
                project_path + 'rawdata/' + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold.nii.gz')
            # doc_fmr.link_protocol('rawdata/' + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id +  '_' + task_name + '_' + run_id + '.prt')
            doc_fmr.save_as(
                raw_bv_path + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold.fmr')
            doc_fmr.close()
