#%% Dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path

#%% Load Data
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
    n_images = len(patches_array)
    fig, ax = plt.subplots(10,int(np.ceil(n_images/float(10))), figsize=(8,8))
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

#%% Plotting non-significant cases
t2_non = t2_train[t2_train.ClinSig == False]
bval_non = bval_train[bval_train.ClinSig == False]
adc_non = adc_train[adc_train.ClinSig == False]
ktrans_non = ktrans_train[ktrans_train.ClinSig == False]

#%% Generate non-significant patch arrays for plotting
t2_non_patches = t2_non['patch'].values
bval_non_patches = bval_non['patch'].values
adc_non_patches = adc_non['patch'].values
ktrans_non_patches = ktrans_non['patch'].values

#%% Non-significant T2 patches
plot_patches(t2_non_patches)


#%% Non-signiciatn BVAL patches
plot_patches(bval_non_patches)


#%% Non-significant ADC patches
plot_patches(adc_non_patches)


#%% Non-signicant KTRANS patches
plot_patches(ktrans_non_patches)