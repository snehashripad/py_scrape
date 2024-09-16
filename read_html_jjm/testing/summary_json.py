import glob
import srsly
import os


def count_phone_numbers_in_json(data):
    return len(data)


def generate_summary_from_folder(parent_folder_path):
    summary = {}
    folder_paths = glob.glob(os.path.join(parent_folder_path, '*'))

    for folder_path in folder_paths:
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            summary[folder_name] = 0
            json_files = glob.glob(os.path.join(folder_path, '*.json'))

            for file_path in json_files:
                try:
                    json_data = srsly.read_json(file_path)
                    count = count_phone_numbers_in_json(json_data)
                    summary[folder_name] += count
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return summary


def write_summary_to_file(summary, summary_file_path):
    try:
        srsly.write_json(summary_file_path, summary, indent=4)
        print(f"Summary written to {summary_file_path}")
    except Exception as e:
        print(f"Error writing to {summary_file_path}: {e}")


if __name__ == '__main__':
    parent_folder_path = r"D:\local_bodies_mh\data1"
    summary_file_path = r"D:\local_bodies_mh\summary.json"
    summary = generate_summary_from_folder(parent_folder_path)
    write_summary_to_file(summary, summary_file_path)
