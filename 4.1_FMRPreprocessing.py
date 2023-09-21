# -*- coding: utf-8 -*-
"""
Created on 2023-01-20

@author: JEck
"""

# Import required packages
import os.path

# Define folder structure and file identifiers
project_path = 'H:/AppleGame/derivatives/'
subjects = [262]
runs = []
sessions = [1]
task_name = 'task-untitled'
func_prep = 'workflow_id-3_type-1_name-func-preprocessing/'

## Motion correction
perform_moco = True
perform_intrasession = False
input_moco = ''
# Define references for preprocessing
moco_ref_volume = 'first'  # 'first' or 'last'
moco_ref_run = 'run-01'
moco_ref_task = 'task-untitled'

## Slice Scan Time Correction
perform_ssc = True
input_ssc = '_3DMCTS'

## High-Pass-Filtering
perform_hpf = True
input_hpf = '_3DMCTS_SCCTBL'
n_cycles = 3

## Spatial Smoothing
perform_smoothing = False
input_smooth = '_3DMCTS_SCCTBL_THPGLMF3c'
gauss_fwhm = 4
fwhm_unit = 'mm'

# loop over all subjects, sessions and runs
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    for ses in range(len(sessions)):
        ses_id = 'ses-' + f'{sessions[ses]:02d}'

        # identify the number of runs in folder
        runs=[]
        for name in os.listdir(project_path + 'rawdata_bv/' + sub_id + '/' + ses_id + '/func/'):
            if name.endswith('_bold.fmr'):
                runs.append(int(name[-11:-9]))
        print(runs)
        runs=[4]
        # if intra-session motion correction shall be applied, define all parameters for the moco reference run
        if perform_moco:
            if perform_intrasession:
                ref_run = project_path + 'rawdata_bv/' + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + moco_ref_task + '_' + moco_ref_run + '_bold.fmr'
                if moco_ref_volume == 'last':
                    doc_ref_run = brainvoyager.open(ref_run)
                    moco_ref_vol = doc_ref_run.n_volumes - 1
                    doc_ref_run.close()

        for run in range(len(runs)):
            run_id = 'run-' + f'{runs[run]:02d}'
            # open all files in the rawdata_bv directory and copy them to the new preprocessing directory
            doc_fmr = brainvoyager.open(
                project_path + 'rawdata_bv/' + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold.fmr')

            # define new preprocessing directory and if it does not exist yet, create it
            func_prep_path = project_path + func_prep + sub_id + '/' + ses_id + '/func/'
            if not os.path.isdir(func_prep_path):
                os.makedirs(func_prep_path)
            # copy file to new preprocessing folder
            doc_fmr.save_as(func_prep_path + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold.fmr')
            doc_fmr.close()

            ## If perform_moco = True, perform motion correction
            if perform_moco:
                doc_fmr = brainvoyager.open(
                    func_prep_path + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold' + input_moco + '.fmr')
                if moco_ref_volume == 'first':
                    moco_ref_vol = 0
                ## If perform_intrasession = True, perform intra-session motion correction
                if perform_intrasession:
                    doc_fmr.correct_motion_to_run_ext(ref_run, moco_ref_vol, 2, 1, 100, 1, 1)
                ## If perform_intrasession = False, perform motion correction within same run
                else:
                    if moco_ref_volume == 'last':
                        moco_ref_vol = doc_fmr.n_volumes - 1
                    doc_fmr.correct_motion_ext(moco_ref_vol, 2, 1, 100, 1, 1)
                doc_fmr.close()

            ## If perform_ssc = True, perform slice scan time correction
            if perform_ssc:
                doc_fmr = brainvoyager.open(
                    func_prep_path + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold' + input_ssc + '.fmr')
                doc_fmr.correct_slicetiming_using_timingtable(1)
                doc_fmr.close()

            ## If perform_hpf = True, perform highpass filtering
            if perform_hpf:
                doc_fmr = brainvoyager.open(
                    func_prep_path + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold' + input_hpf + '.fmr')
                doc_fmr.filter_temporal_highpass_glm_fourier(n_cycles)
                doc_fmr.close()

            ## If perform_smoothing = True, perform spatial smoothing
            if perform_smoothing:
                doc_fmr = brainvoyager.open(
                    func_prep_path + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + '_bold' + input_smooth + '.fmr')
                doc_fmr.smooth_spatial(gauss_fwhm, fwhm_unit)
                doc_fmr.close()




