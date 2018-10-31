"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-10-29 7:16 PM
Description: A script for exploring the images with clinically significant findings. 
Neuron is used in vscode to explore perform this rought EDA - can convert to ipynb
if necessary.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import SimpleITK as sitk
from pathlib import Path

t2_train_table = pd.read_pickle('/Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/t2_train.pkl')

# Filter significant cases
t2_significant_findings = t2_train_table[t2_train_table.ClinSig == True]
t2_significant_findings

# Plot the first significant case for t2
first_sig_case = t2_significant_findings.iloc[0]
first_sig_case_image = sitk.ReadImage(str(first_sig_case['path_to_resampled_file']))
first_sig_case_array = sitk.GetArrayViewFromImage(first_sig_case_image)

# Transform physical point (pos) to index (voxel)
#https://simpleitk-prototype.readthedocs.io/en/latest/user_guide/plot_image.html
pos = first_sig_case['pos']
first_sig_case_cancer_loc = first_sig_case_image.TransformPhysicalPointToIndex(pos)
print("Physical space: ", pos) #(-14.51, 49.44, 20.78)
print("Voxel: ", first_sig_case_cancer_loc) #(205, 150, 9)

# Check out array of image
print(first_sig_case_array.shape)
print(first_sig_case_array.ndim)

# View slice 9
plt.imshow(first_sig_case_array[9,:,:], cmap = 'gray', origin = 'lower')

# Isolating the cancer
# https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image

fig,ax = plt.subplots(1)
ax.imshow(first_sig_case_array[9,:,:], cmap = 'gray', origin = 'lower')
rect = patches.Rectangle((205-15,150-15),30,30,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
plt.show()

## ADC
adc_train_table = pd.read_pickle('/Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX/generated/tables/adc_train.pkl')

adc_significant_findings = adc_train_table[adc_train_table.ClinSig == True]
adc_significant_findings

adc_first_case = adc_significant_findings.iloc[0]
adc_first_image = sitk.ReadImage(str(adc_first_case['path_to_resampled_file']))
adc_first_array = sitk.GetArrayViewFromImage(adc_first_image)

adc_pos_sig_finding = adc_first_case['pos']
adc_loc_sig_finding = adc_first_image.TransformPhysicalPointToIndex(adc_pos_sig_finding)
print('Voxel: ', adc_loc_sig_finding)

plt.imshow(adc_first_array[9,:,:], cmap='gray', origin='lower')

fig,ax = plt.subplots(1)
ax.imshow(adc_first_array[9,:,:], cmap = 'gray', origin='lower')
rect = patches.Rectangle((45-3,53-3),6,6,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
plt.show()