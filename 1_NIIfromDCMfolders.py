# -*- coding: utf-8 -*-
"""
CREATE NIfTI Files from DICOM folders running dcm2nixx
This script can also be used to create BIDS compatible NIfTI files and the corresponding folder structure

"""

__author__ = "Judith Eck"
__version__ = "0.1.0"
__date__ = "16-01-2023"
__name__ = "CreateNIIfromDCMfolders_Version2_GetRunFolders.py"

# =============================================================================
# Import required packages
# =============================================================================
import os.path

# Define folder structure and file identifiers
dcm2niix_path = 'C:/MRIcroGL/Resources/dcm2niix.exe' #Path to converter do not change!!!
dcm_path = 'H:/AppleGame/fMRI/'
sub_folder_name = 'UCL2_'  # I am assuming here the following subject naming folder convention that you have provided as example: UCL2_146
subjects = [146]


output_path = 'H:/AppleGame/rawdata/'
task = 'task-untitled'

for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    print(sub_id)
    dcm_path_sub = dcm_path + sub_folder_name + str(subjects[sub])
    runs = []

    if not os.path.isdir(output_path + sub_id + '/ses-01/' + 'anat'):
        os.makedirs(output_path + sub_id + '/ses-01/' + 'anat')
        os.system(
            dcm2niix_path + ' -f' + ' "' + sub_id + '_ses-01_T1w' + '" ' + '-z y -o ' + output_path + sub_id + '/ses-01/' + 'anat/' + ' ' + dcm_path_sub + '/T1')
        os.system(
            dcm2niix_path + ' -f' + ' "' + sub_id + '_ses-01_T2w' + '" ' + '-z y -o ' + output_path + sub_id + '/ses-01/' + 'anat/' + ' ' + dcm_path_sub + '/T2')

    # check whether there are any subdirectories starting with 'run' in the subjects folder and if so add them to the runs array
    # assuming the following folder naming convention run1 - run9
    for name in os.listdir(dcm_path_sub):
        if (os.path.isdir(dcm_path_sub + '/' + name)) and name.startswith('run'):
            runs.append(int(name[-1]))

    if not os.path.isdir(output_path + sub_id + '/ses-01/' + 'func'):
        os.makedirs(output_path + sub_id + '/ses-01/' + 'func')
    for run in range(len(runs)):
        run_id = 'run-' + f'{runs[run]:02d}'
        print(run_id)
        run_folder = 'run' + f'{runs[run]:01d}'
        os.system(
            dcm2niix_path + ' -f' + ' "' + sub_id + '_ses-01_' + task + '_' + run_id + '_bold" ' + '-z y -o ' + output_path + sub_id + '/ses-01/' + 'func/' + ' ' + dcm_path_sub + '/' + run_folder)
