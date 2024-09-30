import glob
import json
import os
import pandas as pd


# Function to convert the JSON data into Excel format
def convert_to_excel_format_2d(sheetname, dictv, headers):
    if not dictv or 'ds' not in dictv or 'results' not in dictv['ds']:
        return {}

    candidates_data = dictv['ds']['results'].get('candidates', {})

    rows = []
    for candidate, values in candidates_data.items():
        row = [candidate] + values
        rows.append(row)

    return {
        'sheet_name': sheetname,
        'headers': headers,
        'rows': rows,
    }

def read_json_files_from_ac_numbers(base_directory, ac_numbers):
    results = []
    for ac_num in ac_numbers:
        folder_path = os.path.join(base_directory, ac_num)
        json_files = glob.glob(f"{folder_path}/*.json")

        for filepath in json_files:
            with open(filepath, 'r') as file:
                try:
                    json_data = json.load(file)
                    sheetname = os.path.basename(filepath)[:-5]  # Removing .json to use as sheet name

                    candidates_data = json_data['ds']['results'].get('candidates', {})
                    if candidates_data:
                        headers = ["Candidate"] + [f"Value {i + 1}" for i in
                                                   range(len(next(iter(candidates_data.values()))))]
                    else:
                        headers = ["Candidate"]

                    result = convert_to_excel_format_2d(sheetname, json_data, headers)
                    if result['rows']:
                        results.append(result)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filepath}: {e}")
    return results


# Function to write results to an Excel file
def write_to_excel(results, output_file):
    if not results:
        print("No data to write to Excel.")
        return

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for result in results:
            if result['rows']:
                df = pd.DataFrame(result['rows'], columns=result['headers'])
                df.to_excel(writer, sheet_name=result['sheet_name'], index=False)


# Specify the base directory and ac_numbers
base_directory = r'D:\rsync\trans_003\mh_2024\ivrs\acs'
ac_numbers = ["003", "004", "005", "006", "007", "008", "011", "012", "013", "015", "018", "021", "022", "023",
                  "025", "026", "027", "029", "030", "031", "032", "033", "034", "035", "036", "038", "039", "040",
                  "041", "042", "044", "045", "047", "049", "050", "051", "052", "053", "054", "055", "056", "057",
                  "058", "059", "060", "061", "062", "063", "064", "065", "066", "068", "069", "070", "071", "072",
                  "073", "074", "075", "076", "077", "078", "080", "082", "084", "085", "086", "087", "089", "090",
                  "091", "093", "094", "095", "096", "098", "099", "101", "105", "106", "107", "108", "111", "113",
                  "114", "115", "116", "118", "123", "127", "130", "132", "133", "136", "137", "138", "139", "140",
                  "142", "143", "145", "147", "148", "149", "150", "151", "188", "190", "192", "193", "195", "198",
                  "200", "202", "203", "204", "205", "206", "208", "209", "212", "214", "215", "228", "233", "234",
                  "235", "237", "238", "239", "241", "242", "244", "248", "249", "250", "251", "252", "256", "258",
                  "260", "265", "267", "270", "274", "275", "276", "278", "279", "280"]
output_file = r'D:\processed_data.xlsx'  # Ensure this ends with .xlsx
all_results = read_json_files_from_ac_numbers(base_directory, ac_numbers)
write_to_excel(all_results, output_file)

print(f"Data has been written to {output_file}")
