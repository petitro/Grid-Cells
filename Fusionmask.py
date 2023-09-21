import nibabel as nib
import numpy as np

# Charger les fichiers NIfTI
mask1_path = 'H:/GridcatTest/Jeunes/Sub146/Mask/alEC_merged.nii'
mask2_path = 'H:/GridcatTest/Jeunes/Sub146/Mask/pmEC_merged.nii'

mask1_img = nib.load(mask1_path)
mask2_img = nib.load(mask2_path)

# Assurez-vous que les dimensions des deux masques sont identiques
if mask1_img.shape != mask2_img.shape:
    raise ValueError("Les dimensions des masques ne correspondent pas.")

# Charger les données des masques
mask1_data = mask1_img.get_fdata().astype(np.uint8)
mask2_data = mask2_img.get_fdata().astype(np.uint8)

# Fusionner les masques (par exemple, en utilisant une opération OR logique)
merged_mask_data = np.logical_or(mask1_data, mask2_data).astype(np.uint8)

# Créer une nouvelle image NIfTI pour le masque fusionné
merged_mask_img = nib.Nifti1Image(merged_mask_data, mask1_img.affine)

# Enregistrer le masque fusionné en tant que fichier NIfTI
merged_mask_save_path = 'H:/GridcatTest/Jeunes/Sub146/Mask/EC_merged.nii'
nib.save(merged_mask_img, merged_mask_save_path)

print("Le masque fusionné a été enregistré avec succès.")
