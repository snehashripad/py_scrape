import glob
import json
import os
import srsly

# Define paths
input_json_files = glob.glob(r"D:\data_extraction\*.json")
base_output_directory = r"D:\ds3a"


def read_json_with_encoding(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}



for file_path in input_json_files:
    try:
        ac_no = file_path.split('\\')[2].split('.')[0].split('_')[1]
        file_data = read_json_with_encoding(file_path)

        output_directory = os.path.join(base_output_directory, f"ac_{ac_no}")
        os.makedirs(output_directory, exist_ok=True)

        payload = []
        all_phone_numbers = set()

        # Process the JSON data
        for gram_panchayat_name, gram_panchayat_info in file_data.items():
            restructured_data = {}
            for post, details in gram_panchayat_info.items():
                if post != "Gram Panchayat":
                    phone_number = details.get("Phone Number")
                    if phone_number:
                        restructured_data[phone_number] = {
                            "ac_no": ac_no,
                            "Name": details.get("Name", "Unknown"),
                            "Gram Panchayat": gram_panchayat_info.get("Gram Panchayat", "Unknown"),
                            "Post": post,
                        }
                        payload.append(restructured_data)
                        all_phone_numbers.add(phone_number)


        output_json_file = os.path.join(output_directory, 'list.json')
        srsly.write_json(output_json_file, payload)


        phone_numbers_file = os.path.join(output_directory, 'list_phone_numbers.txt')
        with open(phone_numbers_file, 'w', encoding='utf-8') as file:
            for phone_number in all_phone_numbers:
                file.write(f"{phone_number}\n")

        print(f"Transformed JSON data saved to {output_json_file}")
        print(f"Phone numbers saved to {phone_numbers_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
