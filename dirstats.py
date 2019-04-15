#!/usr/bin/env python3

# This program outputs directory statistics about the current directory.
# Output diagrams of file size distribution and file type distribution are
# generated.
# Steps:
# 1. read current directory contents
# 2. traverse through directory content recursively:
#    if a file is found: store the following info in a list:
#       - full file path with file name
#       - file name
#       - file size
#       - file extension
# 3. aggregate the collected data
# 4. generate figure of:
#   - file name extension distribution histogram of the 20 most frequent file
#     name extensions


import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def process_folder(path):
    current_stats = []
    if os.access(path, os.R_OK) and os.path.isdir(path):
        current_dir = os.listdir(path)
        for file_name in current_dir:
            full_file_path = os.path.join(path, file_name)
            if os.path.isfile(full_file_path):
                file_size = os.stat(full_file_path).st_size
                file_ext = file_name.split(".")[-1]
                current_stat = {
                    "full_file_path": full_file_path,
                    "file_name":      file_name,
                    "file_ext":       file_ext,
                    "file_size":      file_size
                }
                current_stats.append(current_stat)
            else:
                folder_stats = process_folder(full_file_path)
                current_stats += folder_stats
    return current_stats

def file_ext_pd_aggregation_function(x):
    file_ext_sum = {
        'file_ext_number': x['file_ext_number'].sum()
    }
    return pd.Series(file_ext_sum, index=['file_ext_number'])


if __name__ == "__main__":
    path = "./" if len(sys.argv) < 2 else sys.argv[1]
    stats = process_folder(path)
    file_ext_rows_array = [["file_ext", "file_ext_number"]]
    for stat in stats:
        file_ext_rows_array.append([stat["file_ext"], 1.0])

    file_ext_rows_np_array = np.array(file_ext_rows_array)

    file_ext_pd_dataframe = pd.DataFrame(
        data    = file_ext_rows_np_array[1:,0:],
        columns = file_ext_rows_np_array[0,0:])

    file_ext_pd_dataframe.sort_values(
        by = ["file_ext"],
        ascending = True)


    file_ext_pd_aggregation = {
        "file_ext": {
            "number_of_files": "sum"
        }
    }

    file_ext_count_pd_dataframe = file_ext_pd_dataframe.groupby("file_ext").count()

    file_ext_count_pd_dataframe = file_ext_count_pd_dataframe.sort_values(
        by = ["file_ext_number"],
        ascending = False)

    file_ext_head = file_ext_count_pd_dataframe.head(30)
    file_ext_numbers_head = file_ext_head['file_ext_number'].tolist()
    file_ext_names_head = file_ext_head.index.tolist()

    barplot = plt.bar(range(len(file_ext_head)), file_ext_numbers_head, color='#4CC4FF')
    plt.ylim([0, max(file_ext_numbers_head)])
    xticks = plt.xticks(range(len(file_ext_head)), file_ext_names_head, rotation=45, color="#2BD5E1")
    plt.savefig('dirstats.png', bbox_inches='tight')
