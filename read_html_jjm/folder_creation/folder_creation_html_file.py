import os
import shutil
import glob

path_pattern = r'D:\jjm\Wardha\*\*\*.html'

html_files = glob.glob(path_pattern, recursive=True)

for file_path in html_files:
    # Extract the file name and directory path
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)

    folder_name = file_name.replace('.html', '')
    folder_path = os.path.join(file_dir, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    shutil.move(file_path, os.path.join(folder_path, file_name))

print("Folders created and files moved successfully.")
