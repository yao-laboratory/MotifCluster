import pandas as pd
import numpy as np
import re
import csv
import sys
import os

#new codes of dealing with files
def pre_process(input_name,output_name,chrome):
    package_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    tsv_filename = package_path + "/input_files/" + input_name
    output_path = package_path + "/input_files/" + output_name
    input_table = pd.read_csv(tsv_filename, sep='\t',header=0, index_col=False)
    print(input_table)
    input_table['p-value'] ='P-value=' + input_table['p-value'].astype(str)
    input_table['start'] = input_table['start'].astype(int)
    input_table['stop'] = input_table['stop'].astype(int)
    input_table['chrome'] = chrome
    input_table['blank1'] = ''
    input_table['blank2'] = ''
    input_table=input_table[['chrome','start','stop','matched_sequence','blank1','strand','blank2','p-value']]
    input_table.sort_values(by='start',inplace=True)
    # csv->Bed
    # bed = pd.read_csv(filepath_or_buffer= "/home/eilene/Downloads/laptop/0418/fimo_chr1.csv", sep="\t", header=None, index_col=False)
    input_table.to_csv(output_path, sep="\t", header=False, index=False)
    print("done.")
