import os
import nibabel as nib

def split_4d_nifti(nifti_file):
    # Load the 4D NIfTI file
    img = nib.load(nifti_file)

    # Get the data array
    data = img.get_fdata()

    # Get the dimensions of the 4D data
    num_volumes = data.shape[-1]

    # Create a directory to store the output volumes
    output_dir = os.path.splitext(nifti_file)[0]
    os.makedirs(output_dir, exist_ok=True)

    # Save each volume as a separate 3D NIfTI file
    for i in range(num_volumes):
        # Extract the i-th volume
        volume = data[..., i]

        # Create a new NIfTI image from the volume data
        volume_img = nib.Nifti1Image(volume, img.affine, img.header)

        # Generate the output filename
        volume_number = str(i + 1).zfill(3)
        output_file = os.path.join(output_dir, f"volume_{volume_number}.nii")

        # Save the volume as a separate NIfTI file
        nib.save(volume_img, output_file)

        #print(f"Volume {i+1} saved as {output_file}")

    print("Splitting complete.")

# Usage example
sub=261 #number of subject
runs=[1] #number of runs of the subject
Path="H:/GridcatTest/Vieux/" #Path to 4D nifti file.gz (Need to adapt the name of nifti_file below)
for index in runs:
    nifti_file = Path+"Sub"+str(sub)+"/NII/sub-"+str(sub)+"_ses-01_task-untitled_run-0"+str(index)+"_bold_3DMCTS_SCCTBL_256_sinc_2x1.0_MNI.nii.gz"
    split_4d_nifti(nifti_file)
