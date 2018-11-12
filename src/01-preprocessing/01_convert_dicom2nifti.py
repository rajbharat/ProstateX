"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-09-26
Description: A script to convert raw data (DICOM images) in ProstateX challenge to nifti format
"""

from pathlib import Path
import dicom2nifti
import os
import json

def generate_paths_to_dicom():
    
    """
    This function generates a dictionary containing the patient id as the
    primary key and assigns a second dictionary containing the paths to the t2,
    adc, and bval dicom folders for conversion to nifti later
    """
    
    print('Generating paths to dicom files for conversion...')
    paths_to_dicom = {}
    path_to_data = Path('./data')

    #generate list containing paths to each patient folder
    patient_folders = [x for x in path_to_data.iterdir() if x.is_dir()]

    # iterate over list of paths to each patient folder
    for patient_folder in patient_folders:
        #os.walk index 0 = roots, 1 = dirs, 2 = files
        patient_path = next(os.walk(patient_folder))[0].replace('data/', '')

        # for each patient folder generate list containing paths to top level subfolder(s) contained within
        subdirectories = [x for x in patient_folder.iterdir() if x.is_dir()]
    
        # iterate over list of paths to subfolders in patient folder
        for subdirectory in subdirectories:
            t2_path = Path()
            adc_path = Path()
            bval_path = Path()
        
            scan_folders_paths = [x for x in subdirectory.iterdir() if x.is_dir()]            

            #//TOFIX: Need to handle situations where patient may have multiple series for a particular modality
            for folder in scan_folders_paths: 
                if 't2tsetra' in str(folder):
                    t2_path = folder
                if 'ADC' in str(folder):
                    adc_path = folder
                if 'BVAL' in str(folder):
                    bval_path = folder

            paths_to_dicom[patient_path] = {'t2':t2_path, 'adc': adc_path, 'bval':bval_path}
    return paths_to_dicom

def convert_dicom2nifti(paths_to_dicom_files):
    
    """
    This function does the actual conversion of dicom files to nifti by
    supplying the dicom2nifti convert_directory method with the path to the
    original dicom files and to a new directory. A nifti subdirectory in the
    main project folder is created.

    * Note: dicom2nifti fails on approximately 40 patients in the data folder
      due to unsupported file types. A command line tool to remedy this problem
      was challenging to install and configure. This is considered a TOFIX for
      future work on this project. 
    """
    
    print('Generating new file structure and nifti files...')
    Path('nifti').mkdir()

    # create ./nifti/patient_folders...
    for patient_id, file_structure in paths_to_dicom_files.items():
        Path('nifti').joinpath(patient_id).mkdir()
        
    nifti = Path('./nifti')
    new_patient_folders = [x for x in nifti.iterdir() if x.is_dir()]
    
    # create ./nifti/patient_folders/subfolders...
    for patient in new_patient_folders:
        patient.joinpath('t2').mkdir()
        patient.joinpath('adc').mkdir()
        patient.joinpath('bval').mkdir()

    # convert files
    patients_length = len(paths_to_dicom_files)
    
    unsuccessful_t2_conversions = []
    unsuccessful_ADC_conversions = []
    unsuccessful_BVAL_conversions = []

    for patient_id, file_structure in paths_to_dicom_files.items():
        # dicom paths
        dicom_t2_path = file_structure['t2']
        dicom_adc_path = file_structure['adc']
        dicom_bval_path = file_structure['bval']

        # new paths
        new_patient_id_path = Path('./nifti').joinpath(patient_id)
        new_t2_path = new_patient_id_path.joinpath('t2')
        new_adc_path = new_patient_id_path.joinpath('adc')
        new_bval_path = new_patient_id_path.joinpath('bval')
 
        #//TOFIX: not catching exception for failed conversions
        try:
            dicom2nifti.convert_directory(str(dicom_t2_path), str(new_t2_path))
        except:
            unsuccessful_t2_conversions.append(dicom_t2_path.parts[1])
        
        try: 
            dicom2nifti.convert_directory(str(dicom_adc_path), str(new_adc_path))
        except:
            unsuccessful_ADC_conversions.append(dicom_adc_path.parts[1])

        try:
            dicom2nifti.convert_directory(str(dicom_bval_path), str(new_bval_path))
        except:
            unsuccessful_BVAL_conversions.append(dicom_bval_path.parts[1])
        
        #log patient id to file
        f = open('dicom2nifti_successful.txt', 'a+')
        f.write(patient_id +"\n")
        f.close()

        patients_length = patients_length - 1
        print(patients_length, ' conversions remaining.')

    with open('t2errors.json', 'w') as filehandle:
        json.dump(unsuccessful_t2_conversions, filehandle)

    with open('adcerrors.json', 'w') as filehandle:
        json.dump(unsuccessful_ADC_conversions, filehandle)
    
    with open('bvalerrors.json', 'w') as filehandle:
        json.dump(unsuccessful_BVAL_conversions, filehandle)
    
def main():
    paths_to_dicom = generate_paths_to_dicom()
    convert_dicom2nifti(paths_to_dicom)

main()

# SCRIPT GENERATES AN ERROR:
# GDCMCONV_NOT_FOUND
# Potential solution here: https://github.com/icometrix/dicom2nifti/issues/11

