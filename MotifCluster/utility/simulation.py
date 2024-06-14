import random
from collections import Counter
from os import listdir, path, makedirs
import os
import numpy as np
import pandas as pd
import json


def read_config_file(config_file_path):
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
    INIT_MIDDLE_AXIS = config["INIT_MIDDLE_AXIS"]
    MIN_PVALUE = config["MIN_PVALUE"]
    MAX_PVALUE = config["MAX_PVALUE"]
    OUTLIER_MIN_GAP = config["FILTERING_OUT_MIN_GAP"]
    OUTLIER_MAX_GAP = config["FILTERING_OUT_MAX_GAP"]
    MIDDLE_AXIS_TO_START_AXIS_DISTANCE = config["MIDDLE_AXIS_TO_START_AXIS_DISTANCE"]
    MIDDLE_AXIS_TO_END_AXIS_DISTANCE = config["MIDDLE_AXIS_TO_END_AXIS_DISTANCE"]
    GAUSSIAN_GROUP_NUMBER = len(MU_SIGMA)
    print(len(MU_SIGMA), MIN_PVALUE, MAX_PVALUE)


def find_distribution_except_nearby(num):
    # This creates a nth Gaussian Distribution from 0th to 9th
    numbers = list(range(GAUSSIAN_GROUP_NUMBER))
    if num in numbers:
        numbers.remove(num)
    # Now use random.choice to pick a number from the remaining ones
    random_number = random.choice(numbers)
    return random_number


def find_distribution_except_nearby_or_log_gap(num):
    # This creates (n) gaussian distributions and 1 gap distribution, totally (n+1) distributions
    numbers = list(range(GAUSSIAN_GROUP_NUMBER+1))
    numbers.remove(num)
    # Now use random.choice to pick a number from the remaining ones
    random_number = random.choice(numbers)
    return random_number


def find_gap_between_cluster(num):
    between_cluster_gap = 0
    random_number = find_distribution_except_nearby_or_log_gap(num)
    if random_number == 10:
        between_cluster_gap = random.randint(OUTLIER_MIN_GAP, OUTLIER_MAX_GAP)
    else:
        between_cluster_gap = MU_SIGMA[random_number][0]
    return random_number, between_cluster_gap


def generate_all_clusters():
    middle_axis = []
    p_value = []
    clusters_size = []
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
            p_value.append(random.uniform(
                MIN_PVALUE, MAX_PVALUE))

        for i in range(1, cluster_size):
            # generate gap randomly
            # print("mu"+str(MU_SIGMA[num][0])+"sigma"+str(MU_SIGMA[num][1]))
            gap = np.random.normal(
                MU_SIGMA[num][0], MU_SIGMA[num][1], size=None)
            gap = int(gap)
            last_middle_axis = middle_axis[-1]
            middle_axis.append(last_middle_axis + gap)
            p_value.append(random.uniform(
                MIN_PVALUE, MAX_PVALUE))
        # build gap between two clusters
        cluster_cnt += 1
        last_middle_axis = middle_axis[-1]
        random_number, between_cluster_gap = find_gap_between_cluster(num)
        middle_axis.append(last_middle_axis + between_cluster_gap)
        p_value.append(random.uniform(
            MIN_PVALUE, MAX_PVALUE))
        clusters_size.append(cluster_size)
    return cluster_cnt, middle_axis, p_value, clusters_size


def change_middle_to_start_end_axis(middle_axis):
    start_axis = []
    end_axis = []
    for i in range(len(middle_axis)):
        start_axis.append(middle_axis[i] - MIDDLE_AXIS_TO_START_AXIS_DISTANCE)
        end_axis.append(middle_axis[i] + MIDDLE_AXIS_TO_END_AXIS_DISTANCE)
    return start_axis, end_axis


def save_data_to_bedfile(start_axis, end_axis, p_value, bed_file_path):
    # store data first
    data = []
    # ("chr1", 2000, 6000, "Feature2", 0, "-"),
    for i in range(len(start_axis)):
        data.append((CHROME, start_axis[i],
                    end_axis[i], "", "", "", "", "P-value=" + str(p_value[i])))

    # write data to the bed file
    with open(bed_file_path, "w") as file:
        for line in data:
            file.write("\t".join(map(str, line)) + "\n")


def cluster_size_analysis(cluster_cnt, clusters_size):
    clusters_size = sorted(clusters_size)
    for number, count in Counter(clusters_size).items():
        print(f"cluster size {number} appears {count} times")


def simulation(output_name):
    folder_output = path.abspath(path.dirname(__file__))
    config_file_path = path.abspath(
        path.join(folder_output, "simulation_parameters.json"))
    read_config_file(config_file_path)

    bed_file_path = path.abspath(
        path.join(folder_output, "utility_output", output_name))
    print("simulation start: ")
    cluster_cnt = 0
    middle_axis = []
    p_value = []
    start_axis = []
    end_axis = []
    clusters_size = []
    cluster_cnt, middle_axis, p_value, clusters_size = generate_all_clusters()
    print("the number of clusters: ", cluster_cnt)
    start_axis, end_axis = change_middle_to_start_end_axis(middle_axis)
    save_data_to_bedfile(start_axis, end_axis, p_value, bed_file_path)
    cluster_size_analysis(cluster_cnt, clusters_size)
