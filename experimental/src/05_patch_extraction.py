"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-10-31 3:36 PM
Description: This script does patch extraction from the resampled nifti files. 
It generates a dataframe for each of the sequences (t2, bval etc.) with columns
containing an array for the patch, an equalized patch, equalized patch at 90 degress,
equalized patch at 180 degrees, and an equalized patch at 270 degress. The dataframes
also contain information about the biopsy location - whether it was significant or not.
"""
#%% DEPENDENCIES
import pandas as pd
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
import pickle

from pathlib import Path
from scipy import ndimage
from skimage import exposure

problem_cases = []

#%% PATCH EXTRACTION
def generate_patches(row, patch_size):
    """
    This function generates the patches from the resampled nifti files. 
    It returns a Pandas Series object containing the patch in several forms
    (histogram equalized and rotated 90, 180, and 270 degrees).
    """
    
    path_to_resampled_file = row.path_to_resampled_file
    reported_pos = row.pos

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
            
        return extracted_patch

    def rotate_patches(image_array):
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
    eq_90 = rotate_patches(eq_patch)[0]
    eq_180 = rotate_patches(eq_patch)[1]
    eq_270 = rotate_patches(eq_patch)[2]
    
    patch_values = pd.Series({'patch':patch, 'eq_patch':eq_patch, 'eq_90':eq_90, 'eq_180':eq_180, 'eq_270':eq_270})
    return patch_values

def add_patch_columns_to_df(dataframe, patch_size):
    new_data = dataframe.apply(generate_patches, patch_size = patch_size, axis = 1)
    merged_frame = pd.concat([dataframe, new_data], axis=1)
    return merged_frame

def remove_problem_cases(dataframe, problem_cases):
    problem_cases = set(problem_cases)
    to_delete = []
    for id, row in dataframe.iterrows():
        # MAY WANT TO CONSIDER REMOVING PATIENTS (PROXID) FROM ALL TABLES TO BALANCE TRAINING DATA?
        if (row.ProxID and row.DCMSerDescr) in problem_cases:
            to_delete.append(id)
    clean_dataframe = dataframe.drop(to_delete)
    return clean_dataframe

def main():

    # Set patch sizes
    t2_patch_size = 32
    adc_patch_size = 8
    bval_patch_size = 8
    ktrans_patch_size = 8

    # Load training_tables 
    t2_train_table = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/t2_train.pkl')
    adc_train_table = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/adc_train.pkl')
    bval_train_table = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/bval_train.pkl')
    ktrans_train_table = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/ktrans_train.pkl')

    # Generate new training data tables
    new_t2_table = add_patch_columns_to_df(t2_train_table, t2_patch_size)
    new_adc_table = add_patch_columns_to_df(adc_train_table, adc_patch_size)
    new_bval_table = add_patch_columns_to_df(bval_train_table, bval_patch_size)
    new_ktrans_table = add_patch_columns_to_df(ktrans_train_table, ktrans_patch_size)
    
    # Drop duplicate rows
    compare_columns = ['ProxID', 'DCMSerDescr', 'path_to_resampled_file', 'fid', 'pos', 'ijk', 'zone', 'ClinSig']

    t2_unique = new_t2_table.drop_duplicates(subset = compare_columns)
    adc_unique = new_adc_table.drop_duplicates(subset = compare_columns)
    bval_unique = new_bval_table.drop_duplicates(subset = compare_columns)
    ktrans_unique = new_ktrans_table.drop_duplicates(subset = compare_columns)

    t2_clean = remove_problem_cases(t2_unique, problem_cases)
    adc_clean = remove_problem_cases(adc_unique, problem_cases)
    bval_clean = remove_problem_cases(bval_unique, problem_cases)
    ktrans_clean = remove_problem_cases(ktrans_unique, problem_cases)

    # Persist new training data tables to disk
    tables_path = Path('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/')
    tables_path.mkdir(exist_ok = True)

    t2_clean.to_csv(str(tables_path) + '/t2_training_data.csv')
    t2_clean.to_pickle(str(tables_path) + '/t2_training_data.pkl')

    adc_clean.to_csv(str(tables_path) + '/adc_training_data.csv')
    adc_clean.to_pickle(str(tables_path) + '/adc_training_data.pkl')

    bval_clean.to_csv(str(tables_path) + '/bval_training_data.csv')
    bval_clean.to_pickle(str(tables_path) + '/bval_training_data.pkl')

    ktrans_clean.to_csv(str(tables_path) + '/ktrans_training_data.csv')
    ktrans_clean.to_pickle(str(tables_path) + '/ktrans_training_data.pkl')

main()