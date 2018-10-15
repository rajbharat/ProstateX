import SimpleITK as sitk
import matplotlib.pyplot as plt
from pathlib import Path

def get_information_for_image(image_path):
    
    """This function accepts a path object and returns a tuple containing voxel spacing (tuple) and 
    image size (tuple) for the nifti file at the given path"""
   
    sitk_image = sitk.ReadImage(str(image_path))
    voxel_spacing = sitk_image.GetSpacing()
    image_size = sitk_image.GetSize()
    return (voxel_spacing, image_size)
    
def process_modality(modality):
    
    """This function accepts a modality (str) and returns a dict containing voxel spacings (lst of tuples) 
    and image sizes (lst of tuples) for the desired modality"""
    
    voxel_spacings = []
    image_sizes = []
    paths_to_nifti = Path('./nifti')
    patient_folders = [x for x in paths_to_nifti.iterdir() if x.is_dir()]
    for patient_folder in patient_folders:
        subdirectories = [x for x in patient_folder.iterdir() if x.is_dir()]
        for subdirectory in subdirectories:
            if modality in str(subdirectory):
                modality_file = [x for x in subdirectory.iterdir()]
                if len(modality_file) != 0:
                    information = get_information_for_image(modality_file[0])
                    voxel_spacings.append(information[0])
                    image_sizes.append(information[1])
    return {'voxel_spacings':voxel_spacings, 'image_sizes':image_sizes}

def generate_charts(modality):
    
    """This function accepts a modality (str) and returns a bar chart of voxel spacing and image sizes for
    all patients in the dataset. Plots for each modality are saved as PDF to a plots folder."""
    
    processed_modality = process_modality(modality)
    voxel_spacings = processed_modality['voxel_spacings']
    image_sizes = processed_modality['image_sizes']
    
    def count_elements(sequence):
        tally = {}
        for element in sequence:
            tally[str(element)] = tally.get(str(element), 0) + 1
        return tally
    
    voxel_count = count_elements(voxel_spacings)
    size_count = count_elements(image_sizes)
    
    v_keys = list(voxel_count.keys())
    v_values = list(voxel_count.values())
    s_keys = list(size_count.keys())
    s_values = list(size_count.values())
    
    plt.figure(figsize=(20,11))
    plt.subplot(1,2,1)
    plt.title(modality + ' voxel spacings')
    plt.xlabel('pixel spacing (x,y,z) in mm')
    plt.ylabel('patient count')
    plt.xticks(rotation=90)
    plt.bar(v_keys, v_values)
    
    plt.subplot(1,2,2)
    plt.title(modality + ' image sizes')
    plt.xlabel('(w,h,d)')
    plt.ylabel('patient count')
    plt.xticks(rotation=90)
    plt.bar(s_keys, s_values)
    
    plt.tight_layout()
    
    plots_path = Path('./plots')
    save_path = plots_path.joinpath(modality + '.pdf')
    plt.savefig(str(save_path))
    
    plt.cla()
    plt.clf()

def main():
    generate_charts('adc')
    generate_charts('bval')
    generate_charts('ktrans')
    generate_charts('t2')

main()