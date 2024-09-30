import glob

import srsly
from tqdm import tqdm
import re
from thefuzz.fuzz import token_set_ratio


def fuzzy_match(term, target, MATCH_THRESHOLD=90):
    # 1. Whole String Match
    if token_set_ratio(str(term).lower().strip(), str(target).lower().strip()) > MATCH_THRESHOLD:
        return True

    # 2. Partial String Match
    words = re.split(' /()', term)
    ratios = [token_set_ratio(str(x).strip().lower(), str(target).strip().lower()) for x in words]
    max_term = max(ratios)
    if max_term >= MATCH_THRESHOLD:
        return True


def get_marge_all_local__files(file_path: list):
    payload = []
    for file in tqdm(file_path):

        try:
            load_lb = srsly.read_json(file)
            # divt_ = {f"{x['District Name']}- {x['Sub-District Name']}":x for x in load_lb}
            for lb in load_lb:
                lb['match'] = f"{lb['District Name']}- {lb['Sub-District Name'].upper()}"
            payload.extend(load_lb)
        except:
            print(file)
    srsly.write_json(rf"D:\local_bodies_mh\mh_local_bodies_com.json", payload)


def get_marge_all_villages_files(file_path):
    paylaod = []
    for file in tqdm(file_path):
        load_data = srsly.read_json(file)
        gp_data = load_data.get('Village_level_functionary_contacts', [])
        divt_ = {f"{x['district']}- {x['block']}": x for x in gp_data}
        paylaod.append(divt_)

    srsly.write_json(rf"D:\local_bodies_mh\mh_gp_com.json", paylaod)


def processs_data(gp_path, lb_path):
    gp_data = srsly.read_json(gp_path)
    lb_data = srsly.read_json(lb_path)
    cnt = 0
    fnd = 0
    l_b_names = set([x['match'] for x in lb_data])
    # orig_ac_name = {x['match']:x for x in lb_data}

    for gp in tqdm(gp_data):

        for key, val in gp.items():
            try:
                key = key.upper()
                val['ac_name'] = [x for x in lb_data if x['match'] == key.upper()][-1].get('Assembly Constituency Name',
                                                                                           '')
                # val['ac_name'] = orig_ac_name[key]['Assembly Constituency Name']
                fnd += 1
            except:
                try:
                    mat = [x for x in l_b_names if fuzzy_match(x, key.title())][-1]
                    val['ac_name'] = mat
                    fnd += 1
                except:
                    val['ac_name'] = ''
                    cnt += 1

    payload = []
    for gp in gp_data:
        for k, v in gp.items():
            payload.append(v)

    print(f"\n not-found{cnt}")
    print(f"\n found{fnd}")
    # print(fnd)
    srsly.write_json(rf"D:\local_bodies_mh\mh_gp_process_ac_name1.json", gp_data)


def find_ac_no(process_gp):
    gp_data = srsly.read_json(process_gp)
    ac_list_path = rf"C:\Users\HP\Downloads\ac_list_prep.json"
    ac_name_data = srsly.read_json(ac_list_path)

    if not isinstance(ac_name_data, dict) or 'flat_list' not in ac_name_data:
        print("Error")
        return

    ac_list = ac_name_data['flat_list']
    # l_b_names = set([x['match'] for x in lb_data])
    ac_mapping = set()
    cnt = 0
    not_cnt = 0
    for gp in gp_data:
        try:
            gp['ac_no'] = [x for x in ac_list if fuzzy_match(x['name1'], gp['ac_name'])][-1].get('ac3')
            cnt += 1
        except:
            gp['ac_no'] = ""
            not_cnt += 1
    print(f"\n found {cnt}")
    print(f"\n not found{not_cnt}")
    srsly.write_json(rf"D:\local_bodies_mh\mh_gp_process_ac_no1.json", gp_data)


if __name__ == '__main__':
    file_paths_local_bodies = glob.glob(rf"D:\GP_details_maharastra\*\*\data.json")
    gp_data_file_path = glob.glob(rf"D:\jjm\extracted_json_data\*\*.json")
    # get_marge_all_local__files(file_paths_local_bodies)
    # get_marge_all_villages_files(gp_data_file_path)
    gp_path = rf"D:\local_bodies_mh\mh_gp_com.json"
    lb_path = rf"D:\local_bodies_mh\mh_local_bodies_com.json"
    # processs_data(gp_path, lb_path)
    process_gp = rf"D:\local_bodies_mh\mh_gp_process_ac_name1.json"
    find_ac_no(process_gp)
