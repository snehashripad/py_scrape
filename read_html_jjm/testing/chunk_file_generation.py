import os
import random
import json
import string

import pandas as pd


def generate_random_key(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def load_existing_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file)
    return {}


def get_excel_file_info(folder_path, json_file_path):
    existing_data = load_existing_data(json_file_path)
    existing_keys = set(existing_data.keys())
    files = os.listdir(folder_path)
    excel_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.xls')]
    if not excel_files:
        return "No Excel files found in the folder."


    for excel_file_name in excel_files:
        while True:
            random_key = generate_random_key()
            if random_key not in existing_keys:
                break
        number_value = excel_file_name.split('_')[1].split('.')[0]
        file_path = os.path.join(folder_path, excel_file_name)
        df = pd.read_excel(file_path, header=None)
        output_file_path = rf"D:\rsync\trans_003\mh_2024\ivrs\acs\ac_{number_value}\target_chunks\ds2\{random_key}.xlsx"
        df.to_excel(output_file_path, header=None, index=False)
        print(f"File successfully written to: {output_file_path}")
        new_entry = {
            "ac": number_value,
            "ds": "ds2"
        }
        print(f"Adding entry: {random_key}: {new_entry}")
        existing_data[random_key] = new_entry

    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return existing_data


if __name__ == "__main__":
    folder_path = rf'D:\merge_excel'
    json_file_path = rf"D:\chunk_dup.json"
    info = get_excel_file_info(folder_path, json_file_path)
    print(info)
