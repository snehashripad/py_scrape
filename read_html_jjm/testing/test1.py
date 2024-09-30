import glob
import json
import pandas as pd
import os


def read_json_and_extract_votes(folder_path):
    json_files = glob.glob(f"{folder_path}/*.json")
    results = []

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                # Check for 'ds2' key
                if 'ds2r2' not in data.get('ds', {}):
                    print(f"Skipping {json_file} as it does not contain 'ds2r2'.")
                    continue

                candidates = data['ds']['ds2r2'].get('results', {}).get('candidates', {})
                cost = data['ds']['ds2r2'].get('cost', 0)
                samples = data['ds']['ds2r2'].get('samples', 0)
                funnel_rate = data['ds']['ds2r2'].get('funnel_rate', 0)
                ac_number = os.path.basename(folder_path)

                # Extract values
                mahayuti_percentage, mahayuti_count = candidates.get('Mahayuti', [0, 0])
                maha_vikas_aghadi_percentage, maha_vikas_aghadi_count = candidates.get('Maha Vikas Aghadi', [0, 0])
                others_percentage, others_count = candidates.get('Others', [0, 0])

                # Format candidate data
                formatted_candidates = (
                    f'Mahayuti: [{mahayuti_percentage}, {mahayuti_count}]\n'
                    f'Maha Vikas Aghadi: [{maha_vikas_aghadi_percentage}, {maha_vikas_aghadi_count}]\n'
                    f'Others: [{others_percentage}, {others_count}]'
                )
                formatted_totals = (
                    f'Cost: {cost}\n'
                    f'Samples: {samples}\n'
                    f'Funnel Rate: {funnel_rate}'
                )

                result_entry = {
                    'ac_no': ac_number,
                    'Alliance': formatted_candidates,
                    'Total Cost': formatted_totals
                }

                results.append(result_entry)

            except json.JSONDecodeError:
                print(f"Error reading {json_file}.")
            except Exception as e:
                print(f"Error processing {json_file}: {e}")

    return results




def generate_excel(base_folder_path, ac_numbers, output_file):
    all_votes = []

    for ac_number in ac_numbers:
        folder_path = f"{base_folder_path}\\ac_{ac_number}"
        print(f"Processing folder: {folder_path}")
        votes = read_json_and_extract_votes(folder_path)

        all_votes.extend(votes)

    df = pd.DataFrame(all_votes)
    df.to_excel(output_file, index=False)


if __name__ == "__main__":
    base_folder_path = r'D:\rsync\trans_003\mh_2024\ivrs\acs'
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
    op_excel_file = rf"D:\Alliance_votes_summary2.xlsx"

    generate_excel(base_folder_path, ac_numbers, op_excel_file)
