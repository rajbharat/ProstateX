"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-11-17
Description: A script to plot significant findings.
"""

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from showit import tile

#%% Import training data
training_data = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/dataframes/training.pkl')

#%% Plot grid of t2 significant findings
t2_train = training_data[(training_data['sequence_type'] == 't2') & (training_data['ClinSig'] == True)]
t2_patches = t2_train['patch'].values
tile(t2_patches, grid=(50,8), size = 60)

#%% Plot grid of adc significant findings
adc_train = training_data[(training_data['sequence_type'] == 'adc') & (training_data['ClinSig'] == True)]
adc_patches = adc_train['patch'].values
tile(adc_patches, grid=(50,8), size = 60)

#%% Plot grid of bval significant findings
bval_train = training_data[(training_data['sequence_type'] == 'bval') & (training_data['ClinSig'] == True)]
bval_patches = bval_train['patch'].values
tile(bval_patches, grid=(50,8), size = 60)

#%% Plot grid of ktrans significant findings
ktrans_train = training_data[(training_data['sequence_type'] == 'ktrans') & (training_data['ClinSig'] == True)]
ktrans_patches = ktrans_train['patch'].values
tile(ktrans_patches, grid=(50,8), size = 60)