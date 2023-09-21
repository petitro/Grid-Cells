# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:41:57 2022

@author: JEck
"""

# Import required packages
import os.path

# Define folder structure, file identifiers and properties
project_path = 'H:/AppleGame/derivatives/'
anat_prep = 'workflow_id-1_type-2_name-anat-preprocessing/'
anat_norm = 'workflow_id-2_type-3_name-anat-normalization/'
func_prep = 'workflow_id-3_type-1_name-func-preprocessing/'
coreg = 'workflow_id-4_type-4_name-func-to-anat-coreg/'

mni=True
vtc_folder = 'workflow_id-5_type-5_name-func-normalization/'
vtc_native= 'workflow_id-5_type-5_name-func-native/'

res = 2
interpol = 2
if interpol == 0:
    interp = 'nearest'
elif interpol == 1:
    interp = 'trilin'
elif interpol == 2:
    interp = 'sinc'

coreg_BBR = False
use_intrasesscoreg = False

fmr_suffix = '_bold_3DMCTS_SCCTBL.fmr'
anat_suffix = '_T1w_IIHC.vmr'

if coreg_BBR:
    fa_suffix = '_BBR_FA.trf'
else:
    fa_suffix = '_FA.trf'
ia_suffix = '_IA.trf'

intensity_thresh = 100

if use_intrasesscoreg:
    coreg_run = 1
    coreg_task_name = 'task-untitled'

subjects = [10]
runs = []
sessions = [1]
task_name = 'task-untitled'

# loop over all subjects, sessions and runs and perform coregistration
for sub in range(len(subjects)):
    sub_id = 'sub-' + f'{subjects[sub]:02d}'
    for ses in range(len(sessions)):
        ses_id = 'ses-' + f'{sessions[ses]:02d}'
        doc_vmr = brainvoyager.open(
            project_path + anat_prep + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + anat_suffix)
        vtc_out = project_path + vtc_folder + sub_id + '/' + ses_id + '/func/'
        if not os.path.isdir(vtc_out):
            os.makedirs(vtc_out)

        # identify the number of runs in folder
        runs = []
        for name in os.listdir(project_path + 'rawdata_bv/' + sub_id + '/' + ses_id + '/func/'):
            if name.endswith('_bold.fmr'):
                runs.append(int(name[-11:-9]))
        for run in range(len(runs)):
            run_id = 'run-' + f'{runs[run]:02d}'
            if use_intrasesscoreg:
                coreg_id = 'run-' + f'{coreg_run:02d}'
                coreg_task = coreg_task_name
            else:
                coreg_id = run_id
                coreg_task = task_name
            fmr_path = project_path + func_prep + sub_id + '/' + ses_id + '/func/'
            fmr_file = sub_id + '_' + ses_id + '_' + task_name + '_' + run_id + fmr_suffix
            coreg_file = sub_id + '_' + ses_id + '_' + coreg_task + '_' + coreg_id + fmr_suffix
            fmr = fmr_path + fmr_file
            ia_trf = project_path + coreg + sub_id + '/' + ses_id + '/func/' + coreg_file[
                                                                               0:-4] + "-TO-" + doc_vmr.file_name[
                                                                                                0:-4] + ia_suffix
            fa_trf = project_path + coreg + sub_id + '/' + ses_id + '/func/' + coreg_file[
                                                                               0:-4] + "-TO-" + doc_vmr.file_name[
                                                                                                0:-4] + fa_suffix
            if mni==True:
                mni_trf = project_path + anat_norm + sub_id + '/' + ses_id + '/anat/' + sub_id + '_' + ses_id + anat_suffix[
                                                                                                            0:-4] + '_TO_MNI_a12_adjBBX.trf'
                vtc = vtc_out + fmr_file[0:-4] + '_256_' + interp + '_' + str(res) + 'x1.0_MNI.vtc'
                doc_vmr.create_vtc_in_mni_space(fmr, ia_trf, fa_trf, mni_trf, vtc, res, interpol, intensity_thresh)
            else:
                vtc_out = project_path + vtc_native + sub_id + '/' + ses_id + '/func/'
                if not os.path.isdir(vtc_out):
                    os.makedirs(vtc_out)
                vtc=vtc_out + fmr_file[0:-4] + '_256_' + interp + '_' + str(res) + 'Native.vtc'
                success = doc_vmr.create_vtc_in_native_space(fmr, ia_trf, fa_trf, vtc,res, interpol, intensity_thresh)
                if success:
                    print("Created VTC file: sub" + sub_id+" "+run_id)
        doc_vmr.close()