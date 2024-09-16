import json
import os


def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            print(f"Data read from file: {data}")  # Debugging line
            return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []


def extract_account_data(data):
    map_data = {}
    print(f"Data passed to extract_account_data: {data}")

    for entry in data:
        for location, details in entry.items():
            if isinstance(details, dict):
                ac_no = details.get('ac_no', '').strip()
                if ac_no:
                    if ac_no not in map_data:
                        map_data[ac_no] = []
                    map_data[ac_no].append(details)
                else:
                    district = details.get('district', 'UnknownDistrict')
                    block = details.get('block', 'UnknownBlock')
                    folder_name = f"{district}_{block}"

                    if folder_name not in map_data:
                        map_data[folder_name] = []
                    map_data[folder_name].append(details)
            else:
                print(f"Skipping entry due to incorrect format: {entry}")

    return map_data


def create_folders_and_files(account_data, base_dir):
    for key, entries in account_data.items():
        folder_name = f'ac_{key}'
        folder_path = os.path.join(base_dir, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        json_file_path = os.path.join(folder_path, 'list.json')
        with open(json_file_path, 'w') as file:
            json.dump(entries, file, indent=4)

        phone_numbers = [entry['Mobile'] for entry in entries if 'Mobile' in entry]

        text_file_path = os.path.join(folder_path, 'phone_numbers.txt')
        with open(text_file_path, 'w') as file:
            for number in phone_numbers:
                file.write(f"{number}\n")


if __name__ == "__main__":
    filename = r"D:\local_bodies_mh\mh_gp_process_ac_no1.json"
    base_dir = r'D:\local_bodies_mh\data1'
    data = read_json_file(filename)
    if data:
        account_data = extract_account_data(data)
        create_folders_and_files(account_data, base_dir)
    else:
        print("No data to process.")
