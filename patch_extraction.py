import pandas as pd
import numpy as np 
import matplotlib.pyplot
from pathlib import Path

images_train = pd.read_csv('data/test_labels/ProstateX-Images-Train.csv')
ktrans_train = pd.read_csv('data/test_labels/ProstateX-Images-KTrans-Train.csv')
findings = pd.read_csv('data/test_labels/ProstateX-Findings-Train.csv')

print(images_train.head())
print(findings.head())

# The lesion information in ProstateX-Findings-Train.csv contains location 
# of the findings (biopsy) in each patient in the world coordinate system (LPS) 
# and the pathology for each finding. Some patients may have more than one finding. 

# Need to extract only the region of interest around the biopsy site to 
# learn the characteristics of cancer. At end of process, should have an
# aggregated array per sequence (num_of_findings, crop_size_x, crop_size_y, crop_size_z)

# four sequences = four arrays

# t2
#ProxID - match to patient ID
#Name - to lowercase match to lowercase filename
#DCMSerDescr - to lowercase match to lowercase filename
#log unsuccessful

# create dataframe containing | Patient_ID | image_name (without extension)



