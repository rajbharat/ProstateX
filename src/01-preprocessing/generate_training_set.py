"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-10-31 3:36 PM
Description:
"""

import pandas as pd
import SimpleITK as sitk
import matplotlib.pyplot as plt
from skimage import exposure
import pickle
from pathlib import Path

def generate_patches(row, patch_size):
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

        extracted_patch = image_array[location_of_finding[2], y_start:y_end, x_start:x_end]
        return extracted_patch

    sitk_image, image_array = load_image(path_to_resampled_file)
    location_of_finding = calculate_location_of_finding(sitk_image, reported_pos)
    raw_image_array = image_array.copy()
    equalized_image_array = equalize_image(image_array)
    patch = extract_patch(raw_image_array, location_of_finding, patch_size)
    hist_equalized_patch = extract_patch(equalized_image_array, location_of_finding, patch_size)
    return (patch, hist_equalized_patch)

def add_patch_columns_to_df(dataframe, patch_size):
    patches_col = dataframe.apply(generate_patches, patch_size = patch_size, axis = 1)
    dataframe = dataframe.assign(patches = patches_col)
    return dataframe

def main():

    # Set patch sizes
    t2_patch_size = 32
    adc_patch_size = 8
    bval_patch_size = 8
    ktrans_patch_size = 8
    
    # Load training_tables 
    t2_train_table = pd.read_pickle('/Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/t2_train.pkl')
    adc_train_table = pd.read_pickle('/Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/adc_train.pkl')
    bval_train_table = pd.read_pickle('/Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/bval_train.pkl')
    ktrans_train_table = pd.read_pickle('/Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/ktrans_train.pkl')

    # Generate new training data tables
    new_t2_table = add_patch_columns_to_df(t2_train_table, t2_patch_size)
    new_adc_table = add_patch_columns_to_df(adc_train_table, adc_patch_size)
    new_bval_table = add_patch_columns_to_df(bval_train_table, bval_patch_size)
    new_ktrans_table = add_patch_columns_to_df(ktrans_train_table, ktrans_patch_size)

    # Drop duplicate rows
    t2_unique = new_t2_table.drop_duplicates()
    adc_unique = new_adc_table.drop_duplicates()
    bval_unique = new_bval_table.drop_duplicates()
    ktrans_unique = new_ktrans_table.drop_duplicates()

    # Persist new training data tables to disk
    tables_path = Path.home().joinpath('Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/')
    tables_path.mkdir(exist_ok = True)

    t2_unique.to_csv(str(tables_path) + '/t2_training_data.csv')
    t2_unique.to_pickle(str(tables_path) + '/t2_training_data.pkl')

    adc_unique.to_csv(str(tables_path) + '/adc_training_data.csv')
    adc_unique.to_pickle(str(tables_path) + '/adc_training_data.pkl')

    bval_unique.to_csv(str(tables_path) + '/bval_training_data.csv')
    bval_unique.to_pickle(str(tables_path) + '/bval_training_data.pkl')

    ktrans_unique.to_csv(str(tables_path) + '/ktrans_training_data.csv')
    ktrans_unique.to_pickle(str(tables_path) + '/ktrans_training_data.pkl')

    # CHECKING PATCHES FOR PROSTATEX-0005
    # 0005_t2 = new_t2_table.iloc[1]
    # plt.imshow(0005_t2['patches'][0], cmap = 'gray', origin='lower')
    # plt.imshow(0005_t2['patches'][1], cmap = 'gray', origin='lower')

    # 0005_adc = new_adc_table.iloc[1]
    # plt.imshow(0005_adc['patches'][0], cmap = 'gray', origin='lower')
    # plt.imshow(0005_adc['patches'][1], cmap = 'gray', origin='lower')

main()