import glob
import os
from bs4 import BeautifulSoup
import json

def find_table_start_index(soup, start_text):
    divs = soup.find_all('div', class_='w3-col')
    for i, div in enumerate(divs):
        h5 = div.find('h5')
        if h5 and start_text in h5.get_text(strip=True):
            return i
    raise ValueError(f"Table with header containing '{start_text}' not found.")

def extract_table_data(table, location_info):
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) == len(headers):
            row_data = {headers[i]: cell.get_text(strip=True) for i, cell in enumerate(cells)}
            # Add location information to each row
            row_data.update(location_info)
            rows.append(row_data)
    return rows

def extract_location_info(soup):
    state = soup.find('span', id='CPHPage_lblState')
    dist = soup.find('span', id='CPHPage_lblDistrict')
    block = soup.find('span', id='CPHPage_lblBlock')
    panchayat = soup.find('span', id='CPHPage_lblPanchayat')
    village = soup.find('span', id='CPHPage_lblVillage')

    return {
        'state': state.get_text(strip=True) if state else 'N/A',
        'district': dist.get_text(strip=True) if dist else 'N/A',
        'block': block.get_text(strip=True) if block else 'N/A',
        'panchayat': panchayat.get_text(strip=True) if panchayat else 'N/A',
        'village': village.get_text(strip=True) if village else 'N/A'
    }

def extract_tables_to_json(html_content, start_text, location_info, skip_tables=4):
    soup = BeautifulSoup(html_content, 'html.parser')
    start_index = find_table_start_index(soup, start_text)
    divs = soup.find_all('div', class_='w3-col')
    flat_data = []

    table_count = 0
    for i in range(start_index, len(divs)):
        div = divs[i]
        tables_in_div = div.find_all('table', class_='w3-table-all')
        for table in tables_in_div:
            if table_count < skip_tables:
                table_count += 1
                continue
            table_data = extract_table_data(table, location_info)
            flat_data.extend(table_data)

    return flat_data

def main(html_file_path, json_file_path, start_text):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    vill_info = extract_location_info(soup)
    tables_data = extract_tables_to_json(html_content, start_text, vill_info)

    result = {
        # 'Village_info': vill_info,
        'Village_level_functionary_contacts': tables_data
    }

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=4)

if __name__ == "__main__":
    file_paths = glob.glob(r"D:\jjm\Maharashtra\Bhandara\*\*\*\*.html")
    start_text = 'Village level functionaries contacts'

    for index, file_path in enumerate(file_paths):
        file_name = os.path.basename(file_path).replace('.html', '')
        json_file_path = rf'D:\jjm\extracted_json_data\Bhandara\{index+1}.json'
        main(file_path, json_file_path, start_text)
