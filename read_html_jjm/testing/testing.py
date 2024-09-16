import srsly
from fuzzywuzzy import fuzz


def fuzzy_match(query, choices, scorer=fuzz.ratio):
    best_match = None
    highest_score = 0
    for choice in choices:
        score = scorer(query, choice)
        if score > highest_score:
            highest_score = score
            best_match = choice
    return best_match


def find_ac_no(process_gp_path, ac_list_path, output_path):
    gp_data = srsly.read_json(process_gp_path)
    ac_name_data = srsly.read_json(ac_list_path)
    if not isinstance(ac_name_data, dict) or 'flat_list' not in ac_name_data:
        print("Error: Invalid AC name data")
        return

    ac_list = ac_name_data['flat_list']
    ac_name_to_ac3 = {x['name1']: x['ac3'] for x in ac_list}
    cnt = 0
    not_cnt = 0

    for entry in gp_data:
        for key, value in entry.items():
            ac_name = value.get('ac_name', '')
            best_match = fuzzy_match(ac_name, ac_name_to_ac3.keys())

            if best_match:
                value['ac_no'] = ac_name_to_ac3.get(best_match, "")
                cnt += 1
            else:
                value['ac_no'] = ""
                not_cnt += 1

    print(f"\nFound {cnt} matches")
    print(f"Not found {not_cnt} matches")
    srsly.write_json(output_path, gp_data)


if __name__ == "__main__":
    process_gp_path = r"D:\local_bodies_mh\mh_gp_process_ac_name1.json"
    ac_list_path = r"C:\Users\HP\Downloads\ac_list_prep.json"
    output_path = r"D:\local_bodies_mh\mh_gp_process_ac_no1.json"

    find_ac_no(process_gp_path, ac_list_path, output_path)
