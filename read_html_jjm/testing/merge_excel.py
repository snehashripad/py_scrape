import pandas as pd
import os

def merge_excel_files(folder_path, output_file=rf'D:\merged_data.xlsx', start_file=31, end_file=60):

    all_data = []
    files_to_merge = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            files_to_merge.append(filename)
    files_to_merge = files_to_merge[start_file - 1:end_file]

    for filename in files_to_merge:
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path)
        all_data.append(df.iloc[:, 0])

    if all_data:
        merged_data = pd.concat(all_data, ignore_index=True)
        merged_data.to_excel(output_file, index=False)
        print(f'Merged {len(all_data)} files from {start_file} to {end_file} into {output_file}')
    else:
        print('No Excel files found in the specified range.')



merge_excel_files(rf'D:\merge_excel')
