import pandas as pd
import glob
import os


def merge_first_two_excel_files(input_directory, ac_nums):
    for ac_num in ac_nums:
        ac_folder_path = os.path.join(input_directory, f"ac_{ac_num}", "target_chunks", "ds2")
        if not os.path.exists(ac_folder_path):
            print(f"Directory does not exist: {ac_folder_path}")
            continue
        excel_files = glob.glob(os.path.join(ac_folder_path, '**', '*.xlsx'), recursive=True)
        excel_files += glob.glob(os.path.join(ac_folder_path, '**', '*.xls'), recursive=True)
        excel_files = [f for f in excel_files if f.lower().endswith(('.xlsx', '.xls'))]
        first_two_files = excel_files[1:3]
        dataframes = []

        for file in first_two_files:
            if os.path.isfile(file):
                try:
                    ext = os.path.splitext(file)[1]
                    print(f"Reading file: {file} with extension: {ext}")
                    df = pd.read_excel(file, header=None)
                    dataframes.append(df.iloc[:, 0])
                except ValueError as e:
                    print(f"ValueError reading {file}: {e}")
                except Exception as e:
                    print(f"Error reading {file}: {e}")

        if dataframes:
            op_path = rf"D:\merge_excel1\ac_{ac_num}.xlsx"
            merged_df = pd.concat(dataframes, ignore_index=True)
            merged_df.to_excel(op_path, index=False, header=None)
            print(f"Merged data written to {op_path} for folder: {ac_num}")
        else:
            print(f"No valid Excel files found to merge in folder: {ac_num}")


if __name__ == "__main__":
    input_directory = rf"D:\rsync\trans_003\mh_2024\ivrs\acs"
    # ac_nums = ['042']
    ac_nums = ['140', '039', '136', '030', '004', '058', '130', '021', '202', '069', '238', '045', '115',
               '190', '033', '248', '270', '258', '044', '215', '105', '063', '047', '035', '038',
               '116', '206', '267', '288', '087', '205', '036', '023', '228', '193', '260', '029',
               '086', '244', '042', '278', '138', '233', '015', '031', '234', '061', '099', '084',
               '078', '012', '237', '022', '060', '209', '114', '285', '280', '008', '077', '065',
               '007', '051', '041', '064', '132', '265', '096', '090', '003', '026', '203', '091', '151',
               '011', '006', '123', '192', '034', '062', '098', '188', '111', '133', '281', '095',
               '089', '150', '198', '094', '018', '143', '118', '013', '147', '066', '137', '139',
               '113', '040', '279', '085', '025', '005', '027', '274', '032', '204', '235', '145',
               '101', '127', '242', '002', '275', '109', '252', '102', '282', '124', '028', '001']

    merge_first_two_excel_files(input_directory, ac_nums)










