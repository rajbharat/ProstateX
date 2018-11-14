#%% Dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path

#%% LOAD DATA
t2_train = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/t2_training_data.pkl')
bval_train = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/bval_training_data.pkl')
adc_train = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/adc_training_data.pkl')
ktrans_train = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/ktrans_training_data.pkl')

#%% Get Signficant cases
t2_sig = t2_train[t2_train.ClinSig == True]
bval_sig = bval_train[bval_train.ClinSig == True]
adc_sig = adc_train[adc_train.ClinSig == True]
ktrans_sig = ktrans_train[ktrans_train.ClinSig == True]

#%% Generate significant patch arrays for plotting
t2_sig_patches = t2_sig['patch'].values
bval_sig_patches = bval_sig['patch'].values
adc_sig_patches = adc_sig['patch'].values
ktrans_sig_patches = ktrans_sig['patch'].values

#%% Plotting function
def plot_patches(patches_array):
    fig, ax = plt.subplots(8,8, figsize=(8,8))
    for i, axi in enumerate(ax.flat):
     axi.imshow(patches_array[i], cmap='gray', origin='lower')
     axi.set(xticks=[], yticks=[])

#%% Significant T2 Patches
plot_patches(t2_sig_patches)

#%% Significant BVAL Patches
plot_patches(bval_sig_patches)

#%% Significant ADC Patches
plot_patches(adc_sig_patches)

#%% Significant KTRANS Patches
plot_patches(ktrans_sig_patches)