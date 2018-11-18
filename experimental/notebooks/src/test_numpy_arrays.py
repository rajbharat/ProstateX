"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-11-17
Description: A script to plot significant findings in numpy arrays.
"""

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from showit import tile

#%% T2 Train
t2_train = np.load('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy/t2/X_train.npy')
tile(t2_train, grid=(70,8), size = 60)

#%% ADC Train
adc_train = np.load('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy/adc/X_train.npy')
tile(adc_train, grid=(70,8), size = 60)

#%% BVAL Train
bval_train = np.load('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy/bval/X_train.npy')
tile(bval_train, grid=(70,8), size = 60)

#%% KTRANS Train
ktrans_train = np.load('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy/ktrans/X_train.npy')
tile(ktrans_train, grid=(70,8), size = 60)