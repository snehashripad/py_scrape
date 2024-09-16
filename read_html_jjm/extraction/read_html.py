import glob
import os

from bs4 import BeautifulSoup
import json
import re


def extract_data_with_headings(html_content, start_table_index=4):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Debug: Print the entire HTML content
    print("HTML Content:\n", soup.prettify())

    extracted_data = []

    # Find all tables in the HTML
    tables = soup.find_all('table')
    print(f"Found {len(tables)} table(s)")

    # Start processing from the specified table index
    for table_index, table in enumerate(tables[start_table_index:], start=start_table_index):
        print(f"Processing Table {table_index + 1}")

        # Extract headings from <th> elements
        headings = [th.get_text(strip=True) for th in table.find_all('th')]
        print(f"Headings: {headings}")

        if not headings:
            print("No headings found in this table.")
            continue

        # Iterate over each row in the table
        rows = table.find_all('tr')
        for row_index, row in enumerate(rows):
            # Extract columns from <td> elements
            columns = row.find_all('td')
            print(f"Processing Row {row_index + 1} with {len(columns)} columns")

            if len(columns) == 0:
                print("Row has 0 columns, skipping.")
                continue

            # Check if row contains data in columns
            if len(columns) != len(headings):
                print(f"Number of columns does not match number of headings.")
                print("Row data:")
                print(row.prettify())
                print(f"Expected number of columns: {len(headings)}")
                print(f"Actual number of columns: {len(columns)}")
                continue

            # Create a dictionary using headings as keys
            row_data = {headings[i]: columns[i].get_text(strip=True) for i in range(len(headings))}
            print(f"Row Data: {row_data}")

            # Validate and add row data
            extracted_data.append(row_data)

    return extracted_data

def read_local_html(file_path):
    if not isinstance(file_path, str):
        raise TypeError(f"Expected a string for file_path, but got {type(file_path).__name__}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_json(output_file, data):
    if not isinstance(output_file, str):
        raise TypeError(f"Expected a string for output_file, but got {type(output_file).__name__}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(file_path, output_file):
    # Validate file paths
    if not isinstance(file_path, str):
        raise TypeError(f"Expected a string for file_path, but got {type(file_path).__name__}")
    if not isinstance(output_file, str):
        raise TypeError(f"Expected a string for output_file, but got {type(output_file).__name__}")

    html_content = read_local_html(file_path)
    data = extract_data_with_headings(html_content)
    write_to_json(output_file, data)
    print(f"Data has been written to '{output_file}'")


if __name__ == "__main__":
    file_paths = glob.glob(r"D:\jjm\Maharashtra\Ahmednagar\*\*\*\*.html")  # List of HTML files
    for file_path in file_paths:
        # Extract the filename without extension for use in output file
        file_name = os.path.basename(file_path).replace('.html', '')
        output_file = rf'D:\jjm\extracted_data\Ahmednagar_data\{file_name}.json'

        print(f"Processing file: {file_path}")
        print(f"Output file: {output_file}")

        main(file_path, output_file)