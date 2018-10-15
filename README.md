Repository for my work in CISC 881 (Queen's University Medical Image Processing Course) that uses data from the [ProstateX challenge](https://www.aapm.org/GrandChallenge/PROSTATEx-2/).

Part 1:

- Remove DICOM metadata by converting to nifti format. (convert_dicom2nifti.py)
- Convert ktrans data (mhd files) to nifti (convert_mhd2nifti.py)
- Complete EDA (plots) on newly created dataset - mainly determine voxel space for t2, adc, bval, and ktrans datasets for further maniputation in second assignment (plot_generation.py)

Part 2:

- Histogram equalization experimentation (histogram_equalization.ipynb)
- Filtering in frequency domain (2dfft.ipynd)
- Resampling voxel spacing of nifti files to represent the majority class for t2, adc, bval, and ktrans (See EDA in part 1).
- Patch cropping for training set in deep learning model (TBI)