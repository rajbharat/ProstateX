## Project Description
Repository for my work in CISC 881 (Queen's University Medical Image Processing Course) that uses data from the [ProstateX challenge](https://www.aapm.org/GrandChallenge/PROSTATEx-2/).

### Data Preprocessing
01_generate_directories.py:  
This script generates the directory structure for the generated data in this project. The user is presented with an option to generate the directory structure for the training data or the test data when this script is executed. 

02_convert_to_nifti.py:   
This script converts DICOM (t2, adc, bval) and MHD (ktrans) files to NIFTI for processing. Conversion to NIFTI removes metadata that is not necessary for model training. The user is presented with an option to convert the raw data for the training set and test set when the script is executed. The dicom2nifti and SimpleITK packages are required in the user environment for this script to execute successfully.

03_resample_nifti.py:  
This script resamples NIFTI files using SimpleITK based on information obtained during exploratory data analysis. The user is presented with an option to resample the training or test datsets when the script is executed. Resampled images are saved in the nifti_resampled folder with the same hierarchy as the unprocessed data. 

04_compile_meta_data.py:
This script merges the ProstateX-Images (or ProstateX-Images-Ktrans) data frames with ProstateX-Findings. It also appends paths to the resampled NIFTI files for each case for use in the patch extraction script. The user is presented with the option to compile the meta data for the training or test datasets when the script is executed. Output is saved to the dataframes folder as appropriate.

#### Data Citation

Geert Litjens, Oscar Debats, Jelle Barentsz, Nico Karssemeijer, and Henkjan Huisman. "ProstateX Challenge data", The Cancer Imaging Archive (2017). ([data](https://doi.org/10.7937/K9TCIA.2017.MURS5CL))

#### Publication Citation

G. Litjens, O. Debats, J. Barentsz, N. Karssemeijer and H. Huisman. "Computer-aided detection of prostate cancer in MRI", IEEE Transactions on Medical Imaging 2014;33:1083-1092.

#### TCIA Citation

Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. ([paper](http://link.springer.com/article/10.1007%2Fs10278-013-9622-7))