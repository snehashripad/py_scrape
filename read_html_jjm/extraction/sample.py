import glob
import json

import logging

# Set up logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)


def extract_data_from_entry(entry_key, entry_data):
    try:
        print(f"Processing entry_key: {entry_key}")
        gram_panchayat_name = entry_key.split(': ')[1].split(' (')[0]
    except IndexError:
        logging.error(f"IndexError processing entry_key: {entry_key}")
        gram_panchayat_name = "Unknown"

    sarpanch_details = {}
    secretary_details = {}

    # Extract Sarpanch details
    for item in entry_data.get("Sarpanch", []):
        if '0' in item and '1' in item:
            if item['0'] == "Sarpanch Name":
                sarpanch_details["Name"] = item['1']
            elif item['0'] == "Mobile No.":
                sarpanch_details["Phone Number"] = item['1']

    # Extract Secretary details
    for item in entry_data.get("Secretary", []):
        if '0' in item and '1' in item:
            if item['0'] == "Secretary Name":
                secretary_details["Name"] = item['1']
            elif item['0'] == "Mobile No.":
                secretary_details["Phone Number"] = item['1']

    return {
        "Gram Panchayat": gram_panchayat_name,
        "Sarpanch": sarpanch_details,
        "Secretary": secretary_details
    }

def process_json_data(json_data):
    result = {}

    for key, entry_data in json_data.items():
        extracted_data = extract_data_from_entry(key, entry_data)
        result[key] = extracted_data

    return result


def write_to_json(output_file, data):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    processed_data = process_json_data(json_data)
    write_to_json(output_file, processed_data)
    print(f"Data has been written to '{output_file}'")



if __name__ == "__main__":
    json_file_path = glob.glob(rf'D:\GP_details\Maharastra\pc\*\*\data.json')
    for file_path in json_file_path:
        ac = file_path.split('\\')[5]
        main(file_path, rf"D:\data_extraction\{ac}.json")


