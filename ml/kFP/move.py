#!/bin/python3

import os
import shutil

# def copy_files(input_folder):
#     # Iterate over files and folders in the input folder
#     for folder_or_file in os.listdir(input_folder):
#         if '-' not in folder_or_file.split('\/')[-1]: continue
#         print(folder_or_file.split('\/')[-1]) 
#         folder_or_file_path = os.path.join(input_folder, folder_or_file)
#         # Check if it's a file
#         # Split the filename into num1 and num2
#         try:
#             [ num1, num2 ] = folder_or_file.split('\/')[-1].split('-')
#         except:
#             continue
#         # Calculate the new folder name
#         new_folder = str(int(num1) * 200 + int(num2))
#         # Create the new folder if it doesn't exist
#         new_folder_path = os.path.join(input_folder, new_folder)
#         if not os.path.exists(new_folder_path):
#             os.makedirs(new_folder_path)
#         # Copy the file to the new folder
# 
# 
#         if os.path.isfile(folder_or_file_path):
#             shutil.copy(folder_or_file_path, os.path.join(new_folder_path, folder_or_file))
#         else:
#             
#             shutil.copytree(folder_or_file_path, new_folder_path, dirs_exist_ok=True)

# Example usage
input_folder = '../tiktok/cw-ow-timing-class/data/'
# copy_files(input_folder)

for i in range(0, 200):
    new_folder_path = input_folder + str(i)
    folder_or_file_path = '../../../data-lwt/baseline-' + str(i)

    shutil.rmtree(new_folder_path)

    os.makedirs(new_folder_path)
    # Copy the file to the new folder


    if os.path.isfile(folder_or_file_path):
        shutil.copy(folder_or_file_path, os.path.join(new_folder_path, folder_or_file))
    else:
        shutil.copytree(folder_or_file_path, new_folder_path, dirs_exist_ok=True)


