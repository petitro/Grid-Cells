# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 11:10:57 2022

@author: JEck
"""

# NOTE: PLEASE RUN THE SCRIPT WITH THE PYTHON CONSOLE IN BRAINVOYAGER OPEN (Python -> Python Console...) This
#       WILL HELP TO IDENTIFY ANY TYPOS IN THE FOLDER/FILE NAMES

# Import required packages
import os.path



# Define folder structure and file identifiers
#project_path = 'C:/Users/colmantl/Documents/fMRI/' # this is the folder contraining the data of all participants
project_path = 'H:/derivatives/'
#project_path = 'Ce PC/Documents/fMRI/'
folder_str = 'sub_' # this is the first part of the participant folders (I need to define this as the partcipant-ID differs from the folder-ID, e.g. UCL081 vs. UCL2_81)
sub_str = 'sub' # this is the first part of participant ID
#anat_str = 'T1' # this is the identifier of the VMR
subjects = [34] # this is the ID of the participant, e.g. 4, 81, 161
runs = [1,2,3,4,5] # please specify only the run numbers
preprocess_str = '_bold_3DMCTS_SCCTBL'
mni_opt = '_TO_MNI_a12_adjBBX.trf' # specifies the name of the MNI transformation file
prt_folder = 'GLM_PPI_LPI' # specifies the name of the PRT folder (has to be a sub-directory of the participant folder)
prt_name = 'Protocole_GLM_' # specifies the first part of the PRT file

# Perform Coregistration (yes (1) or no (0))
coreg = 1 # 0 or 1, set to 0 to skip coregistration, set to 1 to perform coregistration

# Perform VTC Creation (yes (1) or no (0))
vtccreate = 1 # 0 or 1, set to 0 to skip VTC creation, set to 1 to perform VTC creation
res      = 2
interpol = 2 
if interpol == 0:
    interp = 'nearest'
elif interpol == 1:
    interp = 'trilin'
elif interpol == 2:
    interp = 'sinc'
intensity_thresh = 100

# Perform Linking of PRTs (yes (1) or no (0))
prtlink = 0 # 0 or 1, set to 1 to link PRT to VTC
# use the parameters above, in the "Perform VTC Creation" section, to define the VTC name

# Perform spatial smoothing on VTC
vtcsmooth = 1 # 0 or 1, set to 0 to skip VTC smoothing, set to 1 to perform spatial smoothing
gauss_fwhm = 4 # smoothing kernel
fwhm_unit = 'mm' # "mm" or "vx"



# loop over all subjects and runs and perform coregistration
for sub in range(len(subjects)):
    sub_id = sub_str + f'{subjects[sub]:03d}'
    sub_folder = folder_str + str(subjects[sub])
    print('subjects folder: '+ sub_folder)
    print('subjects file ID: '+ sub_id)
    for run in range(len(runs)):
        run_id = 'run' + f'{runs[run]:01d}'
        vmr = project_path +'rawdata_bv/'+ sub_folder + '/ses-01/anat/' +sub_id + '_ses-01_T1w.vmr'
        print( '\n \n' + 'vmr file: ' + vmr)
        print('run folder and file ID: '+ run_id + '\n')
        
        # Perform Coregistration
        if coreg == 1:
            doc_vmr = brainvoyager.open(vmr)
            fmr_file = project_path + sub_folder + '/' + run_id + '/' + sub_id + '_' + run_id + '_' + preprocess_str + '.fmr'
            print('coregistration: ')
            print('fmr file: ' + fmr_file + '\n')
            doc_vmr.coregister_fmr_to_vmr(fmr_file, True)
            doc_vmr.close()
            
        # Perform VTC creation   
        if vtccreate == 1:
            doc_vmr = brainvoyager.open(vmr)
            fmr_file = project_path + sub_folder + '/' + run_id + '/' + sub_id + '_' + run_id + '_' + preprocess_str + '.fmr'
            ia_trf   = fmr_file[0:-4] + "-TO-" + sub_id + '_' + anat_str + '_IIHC' + "_IA.trf"
            fa_trf   = fmr_file[0:-4] + "-TO-" + sub_id + '_' + anat_str + '_IIHC' + "_FA.trf"
            mni_trf  = project_path + sub_folder + '/' + anat_str + '/' + sub_id + '_' + anat_str + '_IIHC'  + mni_opt
            vtc  =  project_path + sub_folder + '/' + run_id + '/' + sub_id + '_' + run_id + '_' + preprocess_str + '_256_' + interp + '_' + str(res) + 'x1.0_MNI.vtc'
            print('VTC creation: ')
            print('fmr file: ' + fmr_file)
            print('IA file: ' + ia_trf)
            print('FA file: ' + fa_trf)
            print('MNI TRF file: ' + mni_trf)
            print('Resulting VTC file: ' + vtc + '\n')
            doc_vmr.create_vtc_in_mni_space(fmr_file, ia_trf, fa_trf, mni_trf, vtc, res, interpol, intensity_thresh)
            doc_vmr.close()
        
        # Link PRTs to VTCs and save VTCs    
        if prtlink == 1:
            doc_vmr = brainvoyager.open(vmr[0:-4] + '_MNI.vmr')
            prt = project_path + sub_folder + '/' +prt_folder +'/' + prt_name +  sub_folder + '_' + str(runs[run]) + '.prt'
            vtc  =  project_path + sub_folder + '/' + run_id + '/' + sub_id + '_' + run_id + '_' + preprocess_str + '_256_' + interp + '_' + str(res) + 'x1.0_MNI.vtc'
            print('Link PRT and save VTC: ')
            #print('vtc file: ' + vtc)
            #print('prt file: ' + prt + '\n')
            doc_vmr.link_vtc(vtc)
            doc_vmr.link_protocol(prt)
            doc_vmr.save_vtc(vtc)
            doc_vmr.close()
            
        # perform VTC preprocessing    
        if vtcsmooth == 1:
            doc_vmr = brainvoyager.open(vmr[0:-4] + '_MNI.vmr')
            vtc  =  project_path + sub_folder + '/' + run_id + '/' + sub_id + '_' + run_id + '_' + preprocess_str + '_256_' + interp + '_' + str(res) + 'x1.0_MNI.vtc'
            print('Perform spatial smoothing: ')
            print('vtc file: ' + vtc)
            print('smotthing kernel: ' + str(gauss_fwhm) + fwhm_unit + '\n')
            doc_vmr.link_vtc(vtc)
            doc_vmr.smooth_spatial(gauss_fwhm, fwhm_unit)
            doc_vmr.close()
            
