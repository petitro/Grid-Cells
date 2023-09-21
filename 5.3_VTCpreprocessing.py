# -*- coding: utf-8 -*-
"""
Created 2023-02-28

@author: JEck
"""

# Import required packages
import os.path

# Define folder structure and file identifiers
project_path = 'H:/AppleGame/derivatives/'
file_ending = '_bold_3DMCTS_SCCTBL_256_sinc_2x1.0_MNI.vtc'
anat_folder = 'workflow_id-2_type-3_name-anat-normalization/'
anat_ending = '_T1w_IIHC_MNI.vmr'
vtc_folder = 'workflow_id-5_type-5_name-func-normalization/'
vtc_prep_folder = 'workflow_id-6_type-9_name-vtc-preprocessing/'

subjects = [146]
runs = []
sessions = [1]
task_name = 'task-untitled'

# Perform temporal highpassfiltering on VTC
vtc_filter = True
n_cycles = 3

# Perform temporal smoothing on VTC
vtc_tempsmooth = False
temp_gauss_fwhm = 3  # smoothing kernel
temp_fwhm_unit = 'dps'  # d or dps (data points) or s or secs (seconds)

# Perform spatial smoothing on VTC
vtc_smooth = True
gauss_fwhm = 4  # smoothing kernel
fwhm_unit = 'mm'  # "mm" or "vx"

# loop over all subjects, sessions and runs
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    for ses in range(len(sessions)):
        ses_id = 'ses-' + f'{sessions[ses]:02d}'

        vtc_out = project_path + vtc_prep_folder + sub_id + '/' + ses_id + '/func/'
        if not os.path.isdir(vtc_out):
            os.makedirs(vtc_out)

        # identify the number of runs in folder
        runs = []
        for name in os.listdir(project_path + 'rawdata_bv/' + sub_id + '/' + ses_id + '/func/'):
            if name.endswith('_bold.fmr'):
                runs.append(int(name[-11:-9]))

        for run in range(len(runs)):
            run_id = 'run-' + f'{runs[run]:02d}'
            file_folder = vtc_folder
            doc = brainvoyager.open(
                project_path + anat_folder + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + anat_ending)
            doc.link_vtc(
                project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + file_ending)
            doc.save_vtc(
                project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + file_ending)
            if vtc_filter:
                # temporal high-pass filter
                doc.filter_temporal_highpass_glm_fourier(n_cycles)
                resulting_file = doc.vtc_file.split('/')[-1]
                os.replace(project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + resulting_file,
                           project_path + vtc_prep_folder + sub_id + '/' + ses_id + '/func/' + resulting_file)
            if vtc_tempsmooth:
                # temporal smoothing
                doc.smooth_temporal(temp_gauss_fwhm, temp_fwhm_unit)
                resulting_file = doc.vtc_file.split('/')[-1]
                os.replace(project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + resulting_file,
                           project_path + vtc_prep_folder + sub_id + '/' + ses_id + '/func/' + resulting_file)
            if vtc_smooth:
                # spatial smoothing
                doc.smooth_spatial(gauss_fwhm, fwhm_unit)
                resulting_file = doc.vtc_file.split('/')[-1]
                os.replace(project_path + vtc_folder + sub_id + '/' + ses_id + '/func/' + resulting_file,
                           project_path + vtc_prep_folder + sub_id + '/' + ses_id + '/func/' + resulting_file)
            doc.close()