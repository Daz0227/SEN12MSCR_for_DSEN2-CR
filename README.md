# DSEN2-CR Model Data Preprocessing for SEN12MSCR Dataset

## Instructions for Using the Preprocessing Script

Follow the steps below to use this preprocessing script for the **SEN12MSCR** dataset to prepare the data for training the **DSEN2-CR model**.

### 1. Download the SEN12MSCR Dataset
First, download the **SEN12MSCR dataset** from the following URL:  
[https://patricktum.github.io/cloud_removal/sen12mscr/](https://patricktum.github.io/cloud_removal/sen12mscr/)

### 2. Place the Script in the SEN12MSCR Folder
Once you have downloaded the dataset, place this Python preprocessing script (`SEN12MSCR_for_DSEN2-CR.py`) in the folder where the dataset is located (i.e., inside the `SEN12MSCR` folder).
### 3. Customizing Dataset Splits (Training/Validation/Testing)

The dataset is split based on the file names using regular expressions in the script. The default split can be adjusted by modifying the regular expressions in the script:

- **Testing set pattern**:
  ```python
  pattern_test = re.compile(r'ROIs(1158_spring_(9|141)|1868_summer_(43|89|146)|1970_fall_(57|27|135)|2017_winter_(130|146|49))_p\d+\.tif')
  ```
  This pattern defines the files that are part of the testing set.

- **Validation set pattern**:
  ```python
  pattern_val = re.compile(r'ROIs(1158_spring_(77)_p\d+\.tif')
  ```
  This pattern defines the files that are part of the validation set.

You can modify these regular expressions to adjust the dataset splits according to your needs. For instance, if you want to use different files for training and validation, you can update the patterns accordingly.
### 4. Run the Script
Open a terminal and navigate to the `SEN12MSCR` folder. Then, run the preprocessing script by executing the following commands:

```bash
cd SEN12MSCR
python SEN12MSCR_for_DSEN2-CR.py
```

This will initiate the preprocessing process, which will automatically:

- Move files from subdirectories to the parent folder.
- Rename files to remove unnecessary substrings (`_s1`, `_s2`, `_cloudy`).
- Create the necessary folders (`s1`, `s2_cloudFree`, `s2_cloudy`).
- Organize files into their respective folders based on their naming patterns.
- Clean up any empty folders.
- Generate a CSV file (`data.csv`) with the necessary metadata.

### 5. Continue with DSEN2-CR Training

After running the preprocessing script, you can continue with the next steps outlined in the [**DSEN2-CR GitHub repository**](https://github.com/ameraner/dsen2-cr) to start training your model with the preprocessed SEN12MSCR dataset.

The repository contains instructions on how to set up the training environment, configure parameters, and run the training process.
