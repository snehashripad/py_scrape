import json
import glob
import os
from fuzzywuzzy import fuzz


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def find_json_files(folder_path):
    return glob.glob(os.path.join(folder_path, '*.json'))


def fuzzy_match(value1, value2, threshold=80):
    return fuzz.partial_ratio(value1, value2) >= threshold


def main(source_folder, target_folder):
    source_files = find_json_files(source_folder)
    target_files = find_json_files(target_folder)
    for file_path in source_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data1 = json.load(f)
            keys = [(x['District Name'],x['Sub-District Name'], x['Gram Panchayat'], x['Assembly Constituency Name'])  for x in data1]
            keys

    for file_path in target_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data2 = json.load(f)
            # entries = [y for y in data2]
            # entries
            for key, value in data2.items():
                entries = [(y['district'], y['block'], y['panchayat']) for y in value]
                entries







if __name__ == '__main__':
    source_folder = r'D:\GP_details_maharastra\Parliamentary Constituency Ahmednagar 362\*'
    target_folder = r'D:\jjm\extracted_data\Ahmednagar_data'
    main(source_folder, target_folder)
