import os
import shutil
from tqdm import tqdm
import re
import csv

# Task 1: Expand folders and move files to the parent folder
def move_files_up_in_folder(folder):
    # Traverse through all subfolders in the current folder
    for dir_name in os.listdir(folder):
        dir_path = os.path.join(folder, dir_name)
        
        # Process only subfolders
        if os.path.isdir(dir_path):
            # Traverse through all files and folders inside the subfolder
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                new_item_path = os.path.join(folder, item)

                # If it is a file, move it directly to the current folder
                if os.path.isfile(item_path):
                    shutil.move(item_path, new_item_path)
                # If it is a folder, recursively process the subfolder
                elif os.path.isdir(item_path):
                    move_files_up_in_folder(item_path)

# Task 2: Move files up from all subfolders in the main directory
def move_files_up(directory):
    # Get all subfolders in the current directory
    dir_names = [dir_name for dir_name in os.listdir(directory) if os.path.isdir(os.path.join(directory, dir_name))]

    # Use tqdm to add a progress bar
    for dir_name in tqdm(dir_names, desc="Processing Folders", unit="folder"):
        dir_path = os.path.join(directory, dir_name)
        
        # Expand the content inside each subfolder
        move_files_up_in_folder(dir_path)

# Task 3: Rename files by removing specific substrings
def rename_files_in_subfolders(directory):
    # Traverse through all subfolders in the current directory
    for dir_name in os.listdir(directory):
        dir_path = os.path.join(directory, dir_name)
        
        # Process only folders
        if os.path.isdir(dir_path):
            # Traverse through all files in the folder
            for item_name in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item_name)

                # Process only files
                if os.path.isfile(item_path):
                    new_name = item_name
                    # Remove specific substrings from the filename
                    new_name = new_name.replace("_s1", "")
                    new_name = new_name.replace("_s2", "")
                    new_name = new_name.replace("_cloudy", "")

                    # If the filename changes, rename the file
                    if new_name != item_name:
                        new_item_path = os.path.join(dir_path, new_name)
                        os.rename(item_path, new_item_path)

# Task 4: Create the necessary folders (s1, s2_cloudFree, and s2_cloudy)
def create_folders(directory):
    # Define the target folder paths
    s1_folder = os.path.join(directory, "s1")
    s2_cloudFree_folder = os.path.join(directory, "s2_cloudFree")
    s2_cloudy_folder = os.path.join(directory, "s2_cloudy")

    # Create the folders if they don't exist
    os.makedirs(s1_folder, exist_ok=True)
    os.makedirs(s2_cloudFree_folder, exist_ok=True)
    os.makedirs(s2_cloudy_folder, exist_ok=True)

# Task 5: Check if a file with the same name exists in the target folder
def check_for_existing_file(target_folder, item_name):
    if os.path.exists(os.path.join(target_folder, item_name)):
        raise FileExistsError(f"File '{item_name}' already exists in the target folder: {target_folder}")
    return item_name

# Task 6: Move files from subfolders to corresponding target folders
def move_files_to_folders(directory):
    # Traverse through all subfolders in the current directory
    for dir_name in os.listdir(directory):
        dir_path = os.path.join(directory, dir_name)

        # Process only subfolders that start with the letter 'R'
        if os.path.isdir(dir_path) and dir_name.startswith('R'):
            # Check the folder name and decide the target folder
            if '_cloudy' in dir_name:
                target_folder = os.path.join(directory, "s2_cloudy")
            elif '_s1' in dir_name:
                target_folder = os.path.join(directory, "s1")
            else:
                target_folder = os.path.join(directory, "s2_cloudFree")
            
            # Traverse through all files in the folder
            for item_name in tqdm(os.listdir(dir_path), desc=f"Moving files from {dir_name} to {target_folder}", unit="file"):
                item_path = os.path.join(dir_path, item_name)

                # Process only files
                if os.path.isfile(item_path):
                    # Check if a file with the same name exists in the target folder
                    item_name = check_for_existing_file(target_folder, item_name)
                    # Move the file to the target folder
                    shutil.move(item_path, os.path.join(target_folder, item_name))

# Task 7: Delete empty folders
def delete_empty_folders(directory):
    # Traverse through all subfolders in the current directory
    for dir_name in os.listdir(directory):
        dir_path = os.path.join(directory, dir_name)

        # Process only subfolders
        if os.path.isdir(dir_path):
            # Recursively delete empty folders inside subfolders
            delete_empty_folders(dir_path)

            # If the folder is empty, delete it
            if not os.listdir(dir_path):  # If the folder is empty, os.listdir returns an empty list
                os.rmdir(dir_path)

# Task 8: Get all files from the 's1' folder
def get_s1_files(directory):
    s1_folder = os.path.join(directory, 's1')
    return [f for f in os.listdir(s1_folder) if os.path.isfile(os.path.join(s1_folder, f))]

# Task 9: Create a CSV file and populate it with data
def create_csv(directory, filename="data.csv"):
    # Regular expression patterns for file matching
    pattern_test = re.compile(r'ROIs(1158_spring_(9|141)|1868_summer_(43|89|146)|1970_fall_(57|27|135)|2017_winter_(130|146|49))_p\d+\.tif')
    pattern_val = re.compile(r'ROIs(1158_spring_(77)_p\d+\.tif')
    
    # Get all files from the 's1' folder
    s1_files = get_s1_files(directory)

    # Open the CSV file and write data
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        
        # Populate the CSV with data
        for s1_file in s1_files:
            # Match the file name with regular expressions
            if pattern_test.match(s1_file):
                first_column = 3  # If the file name matches the pattern
            elif pattern_val.match(s1_file):
                first_column = 2  # If the file name matches the pattern
            else:
                first_column = 1  # If the file name doesn't match the patterns
            
            # Write a row: the first column is either 1 or 3, followed by predefined columns, and the last column is the filename
            writer.writerow([first_column, "s1", "s2_cloudFree", "s2_cloudy", s1_file])

# Main function to execute all tasks
def main():

    current_directory = '.'  # Current directory

    # Step 1: Move files up from subfolders
    move_files_up(current_directory)

    # Step 2: Rename files
    rename_files_in_subfolders(current_directory)
    
    # Step 3: Create necessary folders
    create_folders(current_directory)

    # Step 4: Move files to the appropriate folders
    move_files_to_folders(current_directory)
    
    # Step 5: Delete empty folders
    delete_empty_folders(current_directory)
    
    # Step 6: Create a CSV file with data
    create_csv(current_directory)
    
# Execute the main function
if __name__ == "__main__":
    main()
