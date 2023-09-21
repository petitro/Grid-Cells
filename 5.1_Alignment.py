# -*- coding: utf-8 -*-
"""
Created on Tue 2023-01-24

@author: JEck
"""

# Import required packages
import os.path

# Define folder structure and file identifiers
project_path = 'H:/AppleGame/derivatives/'
anat_prep = 'workflow_id-1_type-2_name-anat-preprocessing/'
func_prep = 'workflow_id-3_type-1_name-func-preprocessing/'
coreg_out = 'workflow_id-4_type-4_name-func-to-anat-coreg/'
anat_suffix = '_T1w_IIHC.vmr'
func_suffix = '_bold_3DMCTS_SCCTBL.fmr'
subjects = [10]
sessions = [1]
task_name = 'task-untitled'
runs = []

use_BBR = False  # set to True when you want to use BBR for coregistration

# loop over all subjects, sessions and runs and perform coregistration
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    for ses in range(len(sessions)):
        ses_id = 'ses-' + f'{sessions[ses]:02d}'
        doc_vmr = brainvoyager.open(
            project_path + anat_prep + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + anat_suffix) #UPDATE
        anat_path = doc_vmr.path
        coreg_out_dir = project_path + coreg_out + sub_id + '/' + ses_id + '/func/'
        if not os.path.isdir(coreg_out_dir):
            os.makedirs(coreg_out_dir)

        # identify the number of runs in folder
        runs=[]
        for name in os.listdir(project_path + 'rawdata_bv/' + sub_id + '/' + ses_id + '/func/'):
            if name.endswith('_bold.fmr'):
                runs.append(int(name[-11:-9]))

        for run in range(len(runs)):
            run_id = 'run-' + f'{runs[run]:02d}'
            fmr_path = project_path + func_prep + sub_id + '/' + ses_id + '/func/'
            fmr_file = sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + func_suffix
            if use_BBR:
                doc_vmr.coregister_fmr_to_vmr_using_bbr(fmr_path + fmr_file)
                IA = fmr_file[0:-4] + "-TO-" + doc_vmr.file_name[0:-4] + "_IA.trf"
                FA = fmr_file[0:-4] + "-TO-" + doc_vmr.file_name[0:-4] + "_BBR_FA.trf"

                os.replace(fmr_path + IA, coreg_out_dir + IA)
                allfiles = os.listdir(fmr_path)
                for f in allfiles:
                    if 'bbr' in f.lower():
                        os.replace(fmr_path + f, coreg_out_dir + f)
            else:
                doc_vmr.coregister_fmr_to_vmr(fmr_path + fmr_file,
                                              True)  # this second parameter enables functional inhomogeneity correction
                IA = fmr_file[0:-4] + "-TO-" + doc_vmr.file_name[0:-4] + "_IA.trf"
                FA = fmr_file[0:-4] + "-TO-" + doc_vmr.file_name[0:-4] + "_FA.trf"
                os.replace(fmr_path + IA, coreg_out_dir + IA)
                os.replace(fmr_path + FA, coreg_out_dir + FA)
                #doc_vmr.close()
            print('Coregistration finished for: ' + fmr_file)
        if use_BBR:
            allfiles = os.listdir(anat_path)
            for f in allfiles:
                if '_ETC-' in f:
                    os.replace(anat_path + f, coreg_out_dir + f)
        doc_vmr.close()


