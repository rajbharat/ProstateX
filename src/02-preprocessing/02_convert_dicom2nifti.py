"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-11-14
Description: A script to convert raw data (DICOM images) in ProstateX challenge to nifti format
"""

import pandas as pd
import dicom2nifti
import os
from pathlib import Path

def generate_paths_to_dicom(is_training_data):
    """
    This function generates a dictionary containing the patient id as the 
    primary key and assigns a second dictionary containing the paths to the 
    t2, adc, and bval dicom folders for conversion to nifti later

    Directory structure for raw data:
    ProstateX/raw/train/dicom_train_204
    ProstateX/raw/test/dicom_train_140
    """
    
    path_to_data = Path()
    paths_to_dicom = {}
    
    if is_training_data:
        path_to_data = Path('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/raw/train/dicom_train_204')
    else:
        path_to_data = Path('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/raw/test/dicom_test_140') 
    
    patient_folders = [x for x in path_to_data.iterdir() if x.is_dir()]
    for patient_folder in patient_folders:
        patient_path = patient_folder.stem
        subdirectories = [x for x in patient_folder.iterdir() if x.is_dir()]
        for subdirectory in subdirectories:
            t2_path = Path()
            adc_path = Path()
            bval_path = Path()

            scan_folders_paths = [x for x in subdirectory.iterdir() if x.is_dir()]
            
            for folder in scan_folders_paths: 
                if 't2tsetra' in str(folder):
                    t2_path = folder
                if 'ADC' in str(folder):
                    adc_path = folder
                if 'BVAL' in str(folder):
                    bval_path = folder
            
            paths_to_dicom[patient_path] = {'t2':t2_path, 'adc': adc_path, 'bval':bval_path} 
    
    #TODO: write a dataframe containing the patient id | t2_path | adc_path | bval_path
    #dataframe = pd.DataFrame(paths_to_dicom)
    print('Done generating paths to dicom files for conversion...')
    return paths_to_dicom

def convert_dicom2nifti(paths_to_dicom, is_training_data):
    """
    This function does the actual conversion of dicom files to nifti by 
    supplying the dicom2nifti convert_directory method with a path to the 
    original dicom files and to a new directory.

    * Note: this failed on approximately 40 patients in the previous dataset. 
    I am going to try a try:except pattern to continue on in the loop. There
    is a command line tool to remedy this problem - but it is challenging to
    install and configure.
    """
    
    path_to_nifti = Path()

    if is_training_data:
        path_to_nifti = Path('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/nifti/')
    else:
        path_to_nifti = Path('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/nifti/')

    counter = 1

    for patient_id, file_structure in paths_to_dicom.items():
        
        # DICOM Paths
        dicom_t2_path = file_structure['t2']
        dicom_adc_path = file_structure['adc']
        dicom_bval_path = file_structure['bval']

        # NIFTI Paths
        nifti_t2_path = path_to_nifti.joinpath(str(patient_id) + '/t2')
        nifti_adc_path = path_to_nifti.joinpath(str(patient_id) + '/adc')
        nifti_bval_path = path_to_nifti.joinpath(str(patient_id) + '/bval')

        try:
            dicom2nifti.convert_directory(str(dicom_t2_path), str(nifti_t2_path))
            dicom2nifti.convert_directory(str(dicom_adc_path), str(nifti_adc_path))
            dicom2nifti.convert_directory(str(dicom_bval_path), str(nifti_bval_path))
            print('Successful conversion of: ' + patient_id, counter)
            counter = counter + 1

        except:
            if is_training_data:
                f = open('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/dicom2nifti_train_problem_cases.txt', 'a+')
                f.write(patient_id +"\n")
                f.close()
                print('Problem with:', patient_id)
            else:
                f = open('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/dicom2nifti_train_problem_cases.txt', 'a+')
                f.write(patient_id +"\n")
                f.close()
                print('Problem with:', patient_id)
            continue

def main():
    is_training_data = False
    
    dataset_type = input('What type of data to convert? (1-Train; 2-Test):')
    if dataset_type == str(1):
        is_training_data = True
    
    paths_to_dicom = generate_paths_to_dicom(is_training_data)
    convert_dicom2nifti(paths_to_dicom, is_training_data)
    
main()