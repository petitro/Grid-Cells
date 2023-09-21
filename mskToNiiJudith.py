import nibabel as nb
import sys

#sys.path.append('C:/Users/Jeck/miniconda3/envs/env_bv_py38/Lib/site-packages/bvbabel-0.2.0-py3.8.egg/')
import bvbabel

NII ="H:/GridcatTest/Sub95/Judith4Dto3DNII/sub-95_ses-01_task-untitled_run-01_bold_3DMCTS_SCCTBL_THPGLMF3c_SD3DSS4.00mm_256_sinc_2x1.0_MNI.nii.gz"
MSK ="H:/GridcatTest/Sub95/Mask/pmEC_PHCpref_right_MNI.msk"
# Load NII and MSK
msk_header, msk_data = bvbabel.msk.read_msk(MSK)
nii_img = nb.load(NII)

# Export mask as nifti
img = nb.Nifti1Image(msk_data, affine=nii_img.affine, header=nii_img.header)
nb.save(img, MSK[:-4] + '_bvbabel.nii')
