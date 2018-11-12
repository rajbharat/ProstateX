#%% DEPENDENCIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from pathlib import Path

#%% LOAD DATA
t2_train = pd.read_pickle('/home/alex/Documents/DataProjects/Data/MBI/ProstateX/generated/training_data/t2_training_data.pkl')
clin_sig = t2_train[t2_train.ClinSig == True]

#%%
def get_patches_for_case(patient_id, dataframe):
    patch = dataframe.loc[dataframe.ProxID == patient_id, 'patch']
    eq_patch = dataframe.loc[dataframe.ProxID == patient_id, 'eq_patch']
    eq_patch_90 = dataframe.loc[dataframe.ProxID == patient_id, 'eq_90']
    eq_patch_180 = dataframe.loc[dataframe.ProxID == patient_id, 'eq_180']
    eq_patch_270 = dataframe.loc[dataframe.ProxID == patient_id, 'eq_270']
    return (patch, eq_patch, eq_patch_90, eq_patch_180, eq_patch_270)

#%%
patches_0192 = get_patches_for_case('ProstateX-0192', clin_sig)