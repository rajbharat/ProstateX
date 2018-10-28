"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-10-28 10:51 AM
Description: A script to generate dataframes containing all the
necessary information to complete path extraction and generation
of training and test datasets.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

### Loading the ProstateX datasets
images_train = pd.read_csv('../data/raw/train_labels/ProstateX-Images-Train.csv')
ktrans_train = pd.read_csv()
findings_train = pd.read_csv()