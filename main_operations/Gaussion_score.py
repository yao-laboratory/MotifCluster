import threading
import time
import gc
from tkinter import Y
import matplotlib.pyplot as plt
import pybedtools
import warnings
import operator
import copy
from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool
from collections import namedtuple
from file_operations.Gaussion_files_operation import *

MINIMUM_VALUE = math.pow(10,-20)
SINGLE_POINT = -5

#mean values
def average(data):
    return np.sum(data)/len(data)

def find_gap_class(distance,gm):
    min = abs(distance - gm.means_[0])
    class_id = 0
    for id in range(len(gm.means_)):
        if abs(distance - gm.means_[id]) < min:
            min = abs(distance - gm.means_[id])
            class_id = int(id)
    return class_id
       
#start calculating the class distribution:
def cal_distance_in_groups(data_axis,data_weight, gm):
    group = [[] for i in range(len(gm.means_) + 1)]
    class_id = -1
    data = np.array([(data_axis[i+1] - data_axis[i]) for i in range(len(data_axis)-1)])
    for i in range(len(data_axis)):
        if i == 0:
            class_id = find_gap_class(data[0],gm)
            group[class_id].append(data_weight[i])
        elif i == len(data_axis) - 1:
            class_id = find_gap_class(data[len(data)-1],gm)
            group[class_id].append(data_weight[i])
        else:
            if (data[i-1] < 500):
                class_id = find_gap_class(data[i-1],gm)
                group[class_id].append(data_weight[i])
            elif data[i] < 500:
                class_id = find_gap_class(data[i],gm)
                group[class_id].append(data_weight[i])
            else:
                class_id = len(gm.means_)
                group[class_id].append(data_weight[i])
    group_final=[]
    for i in range(len(gm.means_) + 1):   
        group[i].sort()
    return group

# data_axis as the all data input
def score(input_file_0, input_file_score_1, input_file_score_2, debug):
    original_filename =  "/home/eilene/Downloads/" + input_file_0
    final_filename_1 = "/home/eilene/Downloads/" + input_file_score_1
    final_filename_2 = "/home/eilene/Downloads/" + input_file_score_2
    data_axis = []
    data_weight=[]
    final_data =[]
    
    data_count_new = []
    cluster_belong_new = []
    data_count_sum = []
    col_types_csv1=[int,int,int,int,int,str]
    # reload GMM Model
    gm_name = '/home/eilene/Downloads/GMM'
    means = np.load(gm_name + '_means.npy')
    loaded_gm = GaussianMixture(n_components = len(means), covariance_type='full')
    loaded_gm.means_ = means
    print("first, start reading total file:\n")
    ori_data_axis=[]
    ori_weight=[]
    f = open(original_filename,"r")
    with f as lines:
        cluster_id = 0
        for line in lines:
            line = line.split()
            raw_weight = ''.join(line[7][8:])
            mark_1 = raw_weight.rfind('e')
            mark_2 = raw_weight.rfind('-')
            num_part1 = float(raw_weight[0:mark_1])
            num_part2 = -int(raw_weight[mark_2 + 1:])
            if num_part1 * math.pow(10,num_part2) <= 0.01:
                ori_data_axis.append(int(line[1])+ 8)
                num = -math.log10(num_part1 * math.pow(10,num_part2))
                ori_weight.append(num)

    f.close()
    ori_data_weight = np.array(ori_weight)
    data_weight_cluster = cal_distance_in_groups(ori_data_axis,ori_data_weight, loaded_gm)
    
    with open(final_filename_1) as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        Row=namedtuple('Row',headers)
        for r in f_csv:
            row=Row(*r)
            row=tuple(convert(value) for convert,value in zip(col_types_csv1,row))
            data_axis.append((row[1])) 
            data_weight.append(row[5])# 选择某一列加入到data数组中
            final_data.append(row[4])
    col_types_csv2=[int,int,int,int]
    with open(final_filename_2) as f2:
        f_csv=csv.reader(f2)
        headers=next(f_csv)
        Row=namedtuple('Row',headers)
        for r in f_csv:
            row=Row(*r)
            row=tuple(convert(value) for convert,value in zip(col_types_csv2,row))
            #add one column to the arrays
            data_count_new.append((row[1])) 
            cluster_belong_new.append(row[2])
            data_count_sum.append(row[3])   
    global_cluster_num = len(loaded_gm.means_)
    print("third, start reading total file to place the order:\n")
    p_score=[]
    for i in range(len(data_count_sum)):
        cluster_flag = cluster_belong_new[i]
        if cluster_flag == -1:
            continue
        if cluster_flag == SINGLE_POINT:
            cluster_flag = global_cluster_num
        cnt = 0
        p_new = 1
        p_ig_total = 0
        group_distance = []
        average_gap = 0
        max_data_weight = 0
        while(cnt < data_count_new[i] ):
            count_1 = 0
            data_cnt = cnt if i == 0 else (data_count_sum[i-1] + cnt)
            if (cnt + 1) < data_count_new[i]:
                group_distance.append(data_axis[data_cnt + 1] - data_axis[data_cnt])
            max_data_weight = max(max_data_weight, float(data_weight[data_cnt]))
            for id_cluster in range(len(data_weight_cluster[cluster_flag])):
                if float(data_weight[data_cnt]) > data_weight_cluster[cluster_flag][id_cluster]:
                    count_1 += 1
                else:
                    p_ig_score = (1 - MINIMUM_VALUE) if count_1 == 0 else -math.log(1 - count_1 / len(data_weight_cluster[cluster_flag]))
                    p_ig_total  +=  p_ig_score
                    break
            cnt += 1
        average_gap = 0 if len(group_distance) == 0 else average(np.array(group_distance))
        p_score.append((i, round(p_ig_total,6), round(average_gap,6), round(max_data_weight,6)))

    p_score_final = sorted(p_score, key=lambda x: x[1], reverse=True) 
    path = "/home/eilene/Downloads/"
    res_dir = os.path.dirname(path)
    res_path = os.path.join(res_dir, 'result_score.csv')
    res_path2 = os.path.join(res_dir, 'result_cluster_weight.csv')
    if os.path.exists(res_path):
        os.remove(res_path)
    if os.path.exists(res_path2):
        os.remove(res_path2)
    write_score_result(res_path, data_axis, data_weight, final_data, p_score_final, data_count_sum, data_count_new)
    write_weight_result(res_path2, data_weight_cluster, global_cluster_num)

 
    
    
    
        

        
   

   