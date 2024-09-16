from Maharastra.localbody import write_json


def merge_json():
    import json
    from fuzzywuzzy import fuzz

    # Load JSON data
    with open(r"D:\local_bodies_mh\mh_gp_process.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(r"C:\Users\HP\Downloads\ac_list_prep.json", "r", encoding="utf-8") as f:
        data1 = json.load(f)

    # Extract 'children' from data1
    da = [x['children'] for x in data1]

    # Flatten the list of children (if needed)
    flat_da = [item for sublist in da for item in sublist]

    # Prepare to store matches
    matches = []

    # Iterate through both datasets
    for data_item in data:
        village = data_item.get('Village','')
        for da1_item in flat_da:
            village1 = da1_item.get('village_name', '')

            # Perform fuzzy matching
            ratio = fuzz.ratio(village.lower(), village1.lower())

            if ratio >= 85:
                data_item.update({'node': da1_item})
                matches.append((village, village1, ratio))

    write_json(data, r"D:\excel_to_json\data_injection\kpcc.json")
    # Output the results
    for match in matches:
        print(f"Match found: {match[0]} <-> {match[1]} with ratio {match[2]}")

if __name__ == "__main__":
    merge_json()