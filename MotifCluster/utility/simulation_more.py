import random
from collections import Counter
from os import listdir, path, makedirs
import os
import numpy as np
import pandas as pd
import json
import sys
from Bio.Seq import Seq

def find_left_right_axis(filename):
    to_left = 0
    to_right = 0
    f = open(filename, "r")
    with f as lines:
        class_id = 0
        for line in lines:
            line = line.split("\t")
            # should add some judge if it is not null or valid in the first line
            to_left = (int(line[2]) - int(line[1])) // 2
            to_right = to_left + (int(line[2]) - int(line[1])) % 2
            break
    f.close()
    tmp = []
    tmp.append(to_left)
    tmp.append(to_right)
    return tmp

def read_config_file(config_file_path, original_bed_file_path):
    # Open the file in read mode
    with open(config_file_path, 'r') as jsonfile:
        # Load the JSON data from the file into a dictionary
        config = json.load(jsonfile)
    global MU_SIGMA, CHROME, MAX_AXIS, MAX_CLUSTER_SIZE, INIT_MIDDLE_AXIS, \
        MIN_PVALUE, MAX_PVALUE, OUTLIER_MIN_GAP, OUTLIER_MAX_GAP, \
        MIDDLE_AXIS_TO_START_AXIS_DISTANCE, MIDDLE_AXIS_TO_END_AXIS_DISTANCE, \
        GAUSSIAN_GROUP_NUMBER
    MU_SIGMA = config["MU_SIGMA"]
    CHROME = config["CHROME"]
    MAX_AXIS = config["MAX_AXIS"]
    MAX_CLUSTER_SIZE = config["MAX_CLUSTER_SIZE"]
    # INIT_MIDDLE_AXIS = config["INIT_MIDDLE_AXIS"]
    MIN_PVALUE = config["MIN_PVALUE"]
    MAX_PVALUE = config["MAX_PVALUE"]
    OUTLIER_MIN_GAP = config["FILTERING_OUT_MIN_GAP"]
    OUTLIER_MAX_GAP = config["FILTERING_OUT_MAX_GAP"]
    # MIDDLE_AXIS_TO_START_AXIS_DISTANCE = config["MIDDLE_AXIS_TO_START_AXIS_DISTANCE"]
    # MIDDLE_AXIS_TO_END_AXIS_DISTANCE = config["MIDDLE_AXIS_TO_END_AXIS_DISTANCE"]
    GAUSSIAN_GROUP_NUMBER = len(MU_SIGMA)
    # print(len(MU_SIGMA), MIN_PVALUE, MAX_PVALUE)
    tmp = []
    tmp = find_left_right_axis(original_bed_file_path)
    MIDDLE_AXIS_TO_START_AXIS_DISTANCE = int(tmp[0])
    MIDDLE_AXIS_TO_END_AXIS_DISTANCE = int(tmp[1])
    INIT_MIDDLE_AXIS = MIDDLE_AXIS_TO_START_AXIS_DISTANCE
    print(MIDDLE_AXIS_TO_START_AXIS_DISTANCE, MIDDLE_AXIS_TO_END_AXIS_DISTANCE, INIT_MIDDLE_AXIS)


def find_distribution_except_nearby(num):
    # This creates a nth Gaussian Distribution from 0th to 9th
    numbers = list(range(GAUSSIAN_GROUP_NUMBER))
    # print(numbers)
    if num in numbers:
        numbers.remove(num)
    # Now use random.choice to pick a number from the remaining ones
    random_number = random.choice(numbers)
    return random_number


def find_distribution_except_nearby_or_log_gap(num):
    # This creates (n) gaussian distributions and 1 gap distribution, totally (n+1) distributions
    #numbers = 0,1,...,n
    numbers = list(range(GAUSSIAN_GROUP_NUMBER+1))
    numbers.remove(num)
    # Now use random.choice to pick a number from the remaining ones
    random_number = random.choice(numbers)
    return random_number


def find_gap_between_cluster(num):
    between_cluster_gap = 0
    random_number = find_distribution_except_nearby_or_log_gap(num)
    if random_number == GAUSSIAN_GROUP_NUMBER:
        between_cluster_gap = random.randint(OUTLIER_MIN_GAP, OUTLIER_MAX_GAP)
    else:
        between_cluster_gap = MU_SIGMA[random_number][0]
        while between_cluster_gap <= (MIDDLE_AXIS_TO_START_AXIS_DISTANCE + MIDDLE_AXIS_TO_END_AXIS_DISTANCE):
            random_number = random.randint(0, len(MU_SIGMA) - 1)
            between_cluster_gap = MU_SIGMA[random_number][0]
    return random_number, between_cluster_gap

def select_pvalue_sequence(df):
    value = random.choice(df["pvalue"].unique().tolist())
    seq_list = df.loc[df["pvalue"] == value, "sequence"].tolist()
    seq = random.choice(seq_list)
    return value, seq

def generate_all_clusters(df):
    middle_axis = []
    p_value = []
    sequences = []
    clusters_size = []
    cluster_ids = []
    between_cluster_gap = 0
    random_number = 0
    num = 0
    last_middle_axis = 0
    cluster_cnt = 0
    while last_middle_axis < MAX_AXIS:
        # build each cluster
        # find new cluster gap distribution
        num = find_distribution_except_nearby(random_number)
        cluster_size = random.randint(1, MAX_CLUSTER_SIZE)
        if last_middle_axis == 0:
            middle_axis.append(INIT_MIDDLE_AXIS)
            pvalue, sequence = select_pvalue_sequence(df)
            p_value.append(pvalue)
            sequences.append(sequence)

        for i in range(1, cluster_size):
            # generate gap randomly
            # print("mu"+str(MU_SIGMA[num][0])+"sigma"+str(MU_SIGMA[num][1]))
            gap = 0
            while True:
                gap = np.random.normal(
                    MU_SIGMA[num][0], MU_SIGMA[num][1], size=None)
                gap = int(gap)
                if gap >= (MIDDLE_AXIS_TO_START_AXIS_DISTANCE + MIDDLE_AXIS_TO_END_AXIS_DISTANCE):
                    break
            
            gap = int(gap)
            last_middle_axis = middle_axis[-1]
            middle_axis.append(last_middle_axis + gap)
            pvalue, sequence = select_pvalue_sequence(df)
            p_value.append(pvalue)
            sequences.append(sequence)
        # build gap between two clusters
        cluster_cnt += 1
        last_middle_axis = middle_axis[-1]
        random_number, between_cluster_gap = find_gap_between_cluster(num)
        middle_axis.append(last_middle_axis + between_cluster_gap)
        pvalue, sequence = select_pvalue_sequence(df)
        p_value.append(pvalue)
        sequences.append(sequence)
        clusters_size.append(cluster_size)
        cluster_ids.extend([cluster_cnt] * cluster_size)
    # reemove the gap point added after the last cluster
    middle_axis.pop()
    p_value.pop()
    sequences.pop()
    return cluster_cnt, middle_axis, p_value, sequences, clusters_size, cluster_ids


def change_middle_to_start_end_axis(middle_axis):
    start_axis = []
    end_axis = []
    for i in range(len(middle_axis)):
        start_axis.append(middle_axis[i] - MIDDLE_AXIS_TO_START_AXIS_DISTANCE)
        end_axis.append(middle_axis[i] + MIDDLE_AXIS_TO_END_AXIS_DISTANCE)
    return start_axis, end_axis


def save_data(start_axis, end_axis, p_value, sequence, cluster_ids, bed_file_path, csv_file_path):

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    
    df = pd.DataFrame({
                        "start": start_axis,
                        "end": end_axis,
                        "sequence": sequence,
                        "strand": "+",
                        "id": cluster_ids
                      })

    df.to_csv(csv_file_path, index=False)
    # store data first
    data = []
    # ("chr1", 2000, 6000, "Feature2", 0, "-"),
    for i in range(len(start_axis)):
        data.append((CHROME, start_axis[i],
                    end_axis[i], sequence[i], "", "+", "", "P-value=" + f"{float(p_value[i]):.2e}"))
    if os.path.exists(bed_file_path):
        os.remove(bed_file_path)
    # write data to the bed file
    with open(bed_file_path, "w") as file:
        for line in data:
            file.write("\t".join(map(str, line)) + "\n")


def cluster_size_analysis(cluster_cnt, clusters_size):
    clusters_size = sorted(clusters_size)
    for number, count in Counter(clusters_size).items():
        print(f"cluster size {number} appears {count} times")

def prepare_df(original_bed_file_path):
    df1 = pd.read_csv(original_bed_file_path, sep="\t", header=None, names=["chrom", "start", "end", "sequence", "score", "strand", "motif", "pValue"])
    df = df1[df1["strand"] == "+"]
    motif_list = df["motif"].tolist()
    motif = motif_list[0]
    df["sequence"] = df["sequence"].astype(str)
    df["pvalue"] = df["pValue"].str.replace("P-value=", "", regex=False).astype(float)
    return df[["sequence", "pvalue"]], motif
    
def simulate_fa_file(csv_file_path):
    df = pd.read_csv(csv_file_path).reset_index(drop=True)
    nucleotides = ['A', 'T', 'C', 'G']
    fa_file_path = csv_file_path.replace(".csv", ".fa")
    if os.path.exists(fa_file_path):
        os.remove(fa_file_path)
    with open(fa_file_path, "w") as file:
        full_seq = ""
        gap_len = 0
        random_letter_gap = ""
        for i, row in df.iterrows():
            seq = str(row["sequence"])
            end = int(row["end"])

            # gap from this row's end to next row's start; random fill for last row
            if i + 1 < len(df):
                next_start = int(df.loc[i + 1, "start"])
                if next_start - end < 0:
                    print("error")
                    # print("next_start",next_start)
                    # print("end",end)
                gap_len = next_start - end
            else:
                gap_len = 0
            random_letter_gap = ''.join(random.choice(nucleotides) for _ in range(gap_len))
            # print(end,next_start,random_letter_gap)
            full_seq += seq
            full_seq += random_letter_gap
        

        file.write(">simulated_genome_reference\n")
        file.write(full_seq + "\n")

def simulation_for_comparison(output_name, original_bed_file):

    original_bed_file_path = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + "/input_files/" + original_bed_file
    if not os.path.exists(original_bed_file_path):
        print(f"Error: {original_bed_file_path} does not exist")
        sys.exit(1)

    folder_output = path.abspath(path.dirname(__file__))
    config_file_path = path.abspath(
        path.join(folder_output, "simulation_parameters.json"))
    read_config_file(config_file_path, original_bed_file_path)
    bed_file_path = path.abspath(
        path.join(folder_output, "utility_output", output_name))
    csv_file_path = path.abspath(
        path.join(folder_output, "utility_output", output_name.replace(".bed", ".csv")))
    
    orifinal_bed_file_colomns_df, motif = prepare_df(original_bed_file_path)
    print("simulation start: ")
    cluster_cnt = 0
    middle_axis = []
    p_value = []
    sequences = []
    start_axis = []
    end_axis = []
    clusters_size = []
    cluster_ids = []
    cluster_cnt, middle_axis, p_value, sequences, clusters_size, cluster_ids = generate_all_clusters(orifinal_bed_file_colomns_df)
    print("the number of clusters: ", cluster_cnt)
    print("clusters' size with generation order in a list:", clusters_size)
    start_axis, end_axis = change_middle_to_start_end_axis(middle_axis)
    # print("attention",middle_axis)
    save_data(start_axis, end_axis, p_value, sequences, cluster_ids, bed_file_path, csv_file_path)
    cluster_size_analysis(cluster_cnt, clusters_size)
    print("Simulation end.")
    print("Start to simulate genome reference file about motif {}.".format(motif))
    simulate_fa_file(csv_file_path)
    print("Simulated corresponding genome reference file from the existed motif bed file built successfully.")
