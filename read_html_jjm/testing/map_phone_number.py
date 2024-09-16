import glob
import json
import os

# Define the folder path pattern using glob
folder_pattern = r'D:\local_bodies_mh\data\**\*.json'


# Function to process and transform JSON files
def transform_json_files(folder_pattern):
    # Use glob to get a list of all JSON files in the folder and subdirectories
    json_files = glob.glob(folder_pattern, recursive=True)

    # Iterate over all files found
    for file_path in json_files:
        try:
            # Read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Check if data is a list of dictionaries
            if not isinstance(data, list):
                print(f"Warning: Data in file {file_path} is not a list. Skipping.")
                continue

            transformed_data = {}
            for entry in data:
                if not isinstance(entry, dict):
                    print(f"Warning: Entry in file {file_path} is not a dictionary. Skipping entry.")
                    continue

                # Ensure 'Mobile' key exists in the dictionary
                if 'Mobile' not in entry:
                    print(f"Warning: 'Mobile' key not found in entry in file {file_path}. Skipping entry.")
                    continue

                mobile = entry['Mobile']
                transformed_data[mobile] = entry

            # Overwrite the original file with transformed data
            with open(file_path, 'w') as file:
                json.dump(transformed_data, file, indent=4)

            print(f'Updated data saved to {file_path}')

        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON in file {file_path}.")
        except Exception as e:
            print(f"An unexpected error occurred with file {file_path}: {e}")


if __name__ == "__main__":
    transform_json_files(folder_pattern)
