import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

### Setting the root path for the data folder
path_data = Path()
path_selection = input('Where is this being executed? 1: portable, 2: workstation: ')

if path_selection == 1:
    print('1')
    #path_data = Path('./Users/alexanders-13mbp/Documents/DataProjects/Data/MBI/ProstateX')
else:
    print('2')
    #path_data = Path('./Documents/DataProjects/Data/MBI/ProstateX')