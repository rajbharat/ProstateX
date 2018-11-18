"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-11-17
Description: This script generates the numpy arrays that will be used in 
deep learning models.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_image_sequence(is_training_data, data):
    t2_sequence = data[data['sequence_type'] == 't2']
    adc_sequence = data[data['sequence_type'] == 'adc']
    bval_sequence = data[data['sequence_type'] == 'bval']
    ktrans_sequence = data[data['sequence_type'] == 'ktrans']


    def balance_classes(sequence):
        # class balance is approximately 3.2/1 in favour of noncancer - therefore 
        # cancer related cases are oversampled by adding 3 rotations to the dataset

        patch_sequence = []
        significance_sequence = []

        for row_id, row in sequence.iterrows():
            if row.ClinSig == True:
                patch_sequence.append(row.eq_patch)
                significance_sequence.append(1)

                patch_sequence.append(row.eq_90)
                significance_sequence.append(1)

                patch_sequence.append(row.eq_180)
                significance_sequence.append(1)

                patch_sequence.append(row.eq_270)
                significance_sequence.append(1)
            else:
                patch_sequence.append(row.eq_patch)
                significance_sequence.append(0)

        return (np.array(patch_sequence), np.array(significance_sequence))
    
    def zero_mean_unit_variance(image_array):

        # https://stackoverflow.com/questions/41652330/centering-of-array-of-images-in-python
        # https://stackoverflow.com/questions/36394340/centering-a-numpy-array-of-images
       
        image_array_float = np.array(image_array, dtype=np.float, copy = True)
        mean = np.mean(image_array_float, axis=(0))
        std = np.std(image_array_float, axis=(0))
        standardized_images = (image_array_float - mean) / std
        return standardized_images

    t2_images, t2_findings = balance_classes(t2_sequence)
    adc_images, adc_findings = balance_classes(adc_sequence)
    bval_images, bval_findings = balance_classes(bval_sequence)
    ktrans_images, ktrans_findings = balance_classes(ktrans_sequence)
    
    t2_norm = zero_mean_unit_variance(t2_images)
    adc_norm = zero_mean_unit_variance(adc_images)
    bval_norm = zero_mean_unit_variance(bval_images)
    ktrans_norm = zero_mean_unit_variance(ktrans_images)

    return {'t2':(t2_norm, t2_findings), 
            'adc':(adc_norm, adc_findings),
            'bval':(bval_norm, bval_findings),
            'ktrans':(ktrans_norm, ktrans_findings)} 

def persist_numpy_to_disk(is_training_data, data):
    t2_images = data.get('t2')[0]
    t2_labels = data.get('t2')[1]

    adc_images = data.get('adc')[0]
    adc_labels = data.get('adc')[1]

    bval_images = data.get('bval')[0]
    bval_labels = data.get('bval')[1]

    ktrans_images = data.get('ktrans')[0]
    ktrans_labels = data.get('ktrans')[1]

    if is_training_data:
        root_path = '/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy'
        
        np.save(Path(root_path + '/t2/X_train.npy'), t2_images)
        np.save(Path(root_path + '/t2/Y_train.npy'), t2_labels)

        np.save(Path(root_path + '/adc/X_train.npy'), adc_images)
        np.save(Path(root_path + '/adc/Y_train.npy'), adc_labels)

        np.save(Path(root_path + '/bval/X_train.npy'), bval_images)
        np.save(Path(root_path + '/bval/Y_train.npy'), bval_labels)

        np.save(Path(root_path + '/ktrans/X_train.npy'), ktrans_images)
        np.save(Path(root_path + '/ktrans/Y_train.npy'), ktrans_labels)
    else:
        root_path = '/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/numpy'
        
        np.save(Path(root_path + '/t2/X_train.npy'), t2_images)
        np.save(Path(root_path + '/t2/Y_train.npy'), t2_labels)

        np.save(Path(root_path + '/adc/X_train.npy'), adc_images)
        np.save(Path(root_path + '/adc/Y_train.npy'), adc_labels)

        np.save(Path(root_path + '/bval/X_train.npy'), bval_images)
        np.save(Path(root_path + '/bval/Y_train.npy'), bval_labels)

        np.save(Path(root_path + '/ktrans/X_train.npy'), ktrans_images)
        np.save(Path(root_path + '/ktrans/Y_train.npy'), ktrans_labels)

def main():
    is_training_data = False
    dataset_type = input('Which dataset are you working with? (1-Train; 2-Test):')
    if dataset_type == str(1):
        is_training_data = True

    if is_training_data:
        data = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/dataframes/training.pkl')
    else:
        data = pd.read_pickled('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/test/dataframes/testing.pkl')
    
    numpy_data = generate_image_sequence(is_training_data, data)
    persist_numpy_to_disk(is_training_data, numpy_data)

main()