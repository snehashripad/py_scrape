import os
import glob

def find_empty_folders(folder_pattern):
    for folder_path in glob.glob(folder_pattern):
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    if not os.listdir(dir_path):
                        print(f"Empty folder found: {dir_path}")

if __name__ == "__main__":
    folder_pattern = r"D:\jjm\extracted_json_data\*"
    find_empty_folders(folder_pattern)
