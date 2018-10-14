import SimpleITK as sitk
from pathlib import Path
import os

def generate_ktrans_folder():
    path_to_nifti = Path('./nifti')
    patient_folders = [x for x in path_to_nifti.iterdir() if x.is_dir()]
    for patient in patient_folders:
        patient.joinpath('ktrans').mkdir()

def convert_mhd2nifti():
    print('Generating nifti files from mhd...')

    path_to_ktrans_data = Path('./ktrans_data')
    path_to_nifti_folder = Path('./nifti')

    patient_folders = [x for x in path_to_ktrans_data.iterdir() if x.is_dir()]
    
    patients_length = len(patient_folders)

    for patient in patient_folders:
        current_patient_id = next(os.walk(patient))[0].replace('ktrans_data/', '')
        print('current_patient_id: ', current_patient_id)

        mhd_files = []
        
        for item in patient.rglob('*.mhd'):
            mhd_files.append(item.name)

        full_path_to_mhdfile = path_to_ktrans_data / current_patient_id / mhd_files[0]
        full_path_to_ktrans_folder = path_to_nifti_folder / current_patient_id / 'ktrans'
        filename = current_patient_id + '-ktrans.nii.gz' 
        new_file_path = full_path_to_ktrans_folder / filename
        
        reader = sitk.ImageFileReader()
        reader.SetFileName(str(full_path_to_mhdfile))
        image = reader.Execute()

        writer = sitk.ImageFileWriter()
        writer.SetFileName(str(new_file_path))
        writer.Execute(image)    

        patients_length = patients_length - 1
        print(patients_length, ' conversions remaining.')

def main():
    generate_ktrans_folder()
    convert_mhd2nifti()

main()

