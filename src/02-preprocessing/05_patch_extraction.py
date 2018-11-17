"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-11-16
Description: This script does patch extraction from the resampled NIFTI files. 
"""

import pandas as pd
import numpy as np
import SimpleITK as sitk
import pickle

from pathlib import Path
from scipy import ndimage
from skimage import exposure

problem_cases = []

def generate_patches(row, patch_sizes):
    """
    This function generate patches from the resampled NIFTI files.
    """

    path_to_resampled_file = row.resampled_nifti
    reported_pos = row.pos

    if 't2' in row.DCMSerDescr:
        patch_size = patch_sizes.get('t2')
    elif 'adc' in row.DCMSerDescr:
        patch_size = patch_sizes.get('adc')
    elif 'bval' in row.DCMSerDescr:
        patch_size = patch_sizes.get('bval')
    else:
        patch_size = patch_sizes.get('ktrans')


    def load_image(path_to_resampled_file):
        sitk_image = sitk.ReadImage(str(path_to_resampled_file))
        image_array = sitk.GetArrayViewFromImage(sitk_image)
        return sitk_image, image_array
    
    def calculate_location_of_finding(sitk_image, reported_pos):
        location_of_finding = sitk_image.TransformPhysicalPointToIndex(reported_pos)
        return location_of_finding

    def equalize_image(image_array):
        equalized_image_array = exposure.equalize_hist(image_array)
        return equalized_image_array
    
    def extract_patch(image_array, location_of_finding, patch_size):
        x = location_of_finding[0]
        y = location_of_finding[1]

        x_start = x - (patch_size // 2)
        x_end = x + (patch_size // 2)
        y_start = y - (patch_size // 2)
        y_end = y + (patch_size // 2)

        try:
            extracted_patch = image_array[location_of_finding[2], y_start:y_end, x_start:x_end]
        except IndexError:
            extracted_patch = image_array[-1, y_start:y_end, x_start:x_end]
            problem_cases.append(row.ProxID)
            problem_cases.append(row.DCMSerDescr)
            print('Problem with image:', row.ProxID, path_to_resampled_file)
            pass 

        return extracted_patch
    
    def generate_rotations(image_array):
        patch_90 = ndimage.rotate(image_array, 90, reshape=False)
        patch_180 = ndimage.rotate(image_array, 180, reshape=False)
        patch_270 = ndimage.rotate(image_array, 270, reshape=False)
        return (patch_90, patch_180, patch_270)
    
    sitk_image, image_array = load_image(path_to_resampled_file)
    location_of_finding = calculate_location_of_finding(sitk_image, reported_pos)
    
    raw_image_array = image_array.copy()
    equalized_image_array = equalize_image(image_array)
    
    patch = extract_patch(raw_image_array, location_of_finding, patch_size)
    eq_patch = extract_patch(equalized_image_array, location_of_finding, patch_size)
    eq_90 = generate_rotations(eq_patch)[0]
    eq_180 = generate_rotations(eq_patch)[1]
    eq_270 = generate_rotations(eq_patch)[2]
    
    patch_values = pd.Series({'patch':patch, 'eq_patch':eq_patch, 'eq_90':eq_90, 'eq_180':eq_180, 'eq_270':eq_270})
    return patch_values

def add_patch_columns_to_df(dataframe, patch_sizes):
    new_data = dataframe.apply(generate_patches, patch_sizes = patch_sizes, axis = 1)
    merged_frame = pd.concat([dataframe, new_data], axis=1)
    return merged_frame

def remove_problem_cases(dataframe, problem_cases):
    problem_cases = set(problem_cases)
    to_delete = []
    for id, row in dataframe.iterrows():
        # MAY WANT TO CONSIDER REMOVING PATIENTS (PROXID) FROM ALL TABLES TO BALANCE TRAINING DATA?
        if (row.ProxID in problem_cases) and (row.DCMSerDescr in problem_cases):
            to_delete.append(id)
    clean_dataframe = dataframe.drop(to_delete)
    return clean_dataframe

def persist_data(is_training_data, dataframe):
    if is_training_data:
        dataframe.to_csv('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/dataframes/training.csv')
        dataframe.to_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/dataframes/training.pkl')
    else:
        dataframe.to_csv('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/dataframes/training.csv')
        dataframe.to_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/dataframes/training.pkl')

def main():
    is_training_data = False
    dataset_type = input('Which dataset are you working with? (1-Train; 2-Test):')
    if dataset_type == str(1):
        is_training_data = True

    patch_sizes = {
        't2': 32,
        'adc': 8,
        'bval':8,
        'ktrans':8
    }
    
    if is_training_data:
        dataset = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/dataframes/training_meta_data.pkl')
        complete_dataset = add_patch_columns_to_df(dataset, patch_sizes)
        clean_dataset = remove_problem_cases(complete_dataset, problem_cases)
        persist_data(is_training_data, clean_dataset)
    else:
        dataset = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/dataframes/test_meta_data.pkl')
        complete_dataset = add_patch_columns_to_df(dataset, patch_sizes)
        clean_dataset = remove_problem_cases(complete_dataset, problem_cases)
        persist_data(is_training_data, clean_dataset)

main()

