# import math
import threading
import time
import gc
from tkinter import Y
# import numpy as np
import matplotlib.pyplot as plt
import pybedtools
# import csv,re
# import os
import warnings
import operator
import copy
from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool
from collections import namedtuple
from file_operations.Gaussion_0714_files_operation import *

MINIMUM_VALUE = math.pow(10,-20)
SINGLE_POINT = -5
global_cluster_num = 10

#均值
def average(data):
    return np.sum(data)/len(data)

# data_axis as the all data input
def score(input_file_score_1, input_file_score_2, debug):
    final_filename_1 = "/home/eilene/Downloads/" + input_file_score_1
    final_filename_2 = "/home/eilene/Downloads/" + input_file_score_2
    data_axis = []
    data_weight=[]
    final_data =[]
    
    data_count_new = []
    cluster_belong_new = []
    data_count_sum = []
    col_types_csv1=[int,int,int,int,int,str]
    with open(final_filename_1) as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        # print(headers)
        Row=namedtuple('Row',headers)
        for r in f_csv:
            row=Row(*r)
            # print(row)
            # print(type(row.IssueType))
            row=tuple(convert(value) for convert,value in zip(col_types_csv1,row))
            data_axis.append((row[1])) 
            data_weight.append(row[5])# 选择某一列加入到data数组中
            final_data.append(row[4])
            # print(row)
    col_types_csv2=[int,int,int,int]
    with open(final_filename_2) as f2:
        f_csv=csv.reader(f2)
        headers=next(f_csv)
        # print(headers)
        Row=namedtuple('Row',headers)
        for r in f_csv:
            row=Row(*r)
            # print(row)
            # print(type(row.IssueType))
            row=tuple(convert(value) for convert,value in zip(col_types_csv2,row))
            data_count_new.append((row[1])) 
            cluster_belong_new.append(row[2])# 选择某一列加入到data数组中
            data_count_sum.append(row[3])
            # print(row)
    
    # data=np.array([(data_axis[i+1] - data_axis[i]) for i in range(len(data_axis)-1)])
    # # print("data=",data)
    # # print(len(data))
    # #相邻点间距离为X轴的GMM拟合
    # X_DISTANCE = data.reshape(len(data), 1)
    # x_distance_temp = []
    # for value in X_DISTANCE:
    #     if value <= 500:
    #         x_distance_temp.append(value)
            
    # X_DISTANCE = np.array(x_distance_temp)
    # # print(X_DISTANCE)
    # gm = GaussianMixture(n_components = global_cluster_num, n_init = 10, random_state = 100)
    # gm.fit(X_DISTANCE)

    # p_g = []     
    # for i in range(len(data_count_new)):
    #     if data_count_new[i] == 1:
    #         p_g.append(0)
    #     else:
    #         data_distance_temp_ = np.array([(int(x1[j+1]) - int(x1[j])) for j in range(total_start, total_start + data_count_new[i] - 1)])
    #         p_g.append(round(-gm.score(data_distance_temp_.reshape(len(data_distance_temp_), 1)),4))
    #     total_start += data_count_new[i]
    print("*******")    
    # final_data = []
    # for i in range(len(data_count_new)):
    #     if data_count_new[i] == 1:
    #         final_data.append(-1)
    #         continue
    #     cnt = data_count_new[i]
    #     for j in range(cnt):
    #         final_data.append(cluster_belong_new[i])
    # print(final_data)
    data_weight_cluster = [[] for i in range(global_cluster_num + 1)]
    for i in range(len(final_data)):
        # num = final_data[id]
        # if the point is the outlier, no need to do anything
        cluster_flag = final_data[i]
        if cluster_flag == -1 or cluster_flag == SINGLE_POINT:
            data_weight_cluster[global_cluster_num].append(data_weight[i])
        else:
            data_weight_cluster[cluster_flag].append(data_weight[i])
    
    for num in range(global_cluster_num + 1):        
        data_weight_cluster[num].sort()
        # print(data_weight_cluster[num])


    print("third, start reading total file to place the order:\n")

    # probability_ig=[]
    p_score=[]
    # data_partial = np.array(average_distance)
    # p_g = -gm.score_samples(data_partial.reshape(len(data_partial), 1))
    # print(p_g)
    for i in range(len(data_count_sum)):
        cluster_flag = cluster_belong_new[i]
        # print(cluster_flag)
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
            # if int(data_weight[data_cnt]) > max_data_weight:
            #     max_data_weight = int(data_weight[data_cnt]
            max_data_weight = max(max_data_weight, float(data_weight[data_cnt]))
            # print(cluster_flag)
            # print(len(data_weight_cluster[cluster_flag]))
            for id_cluster in range(len(data_weight_cluster[cluster_flag])):
                # print("aaa")
                # print(cluster_flag)
                # print(data_weight[data_cnt])
                # print(data_weight_cluster[cluster_flag][id_cluster])
                if data_weight[data_cnt] > data_weight_cluster[cluster_flag][id_cluster]:
                    count_1 += 1
                else:
                    # print("@@@@@@@@@@")
                    # print(count_1) 
                    # print(len(data_weight_cluster[cluster_flag]))
                    # calculate P(X >= x)
                    #??the probality of first number and the last number
                    p_ig_score = (1 - MINIMUM_VALUE) if count_1 == 0 else -math.log(1 - count_1 / len(data_weight_cluster[cluster_flag]))
                    # print(count_1 / len(data_weight_cluster[cluster_flag]))
                    # probability_ig.append(p_ig_score)
                    p_ig_total  +=  p_ig_score
                    # print(i)
                    # print(p_ig_total)
                    break
            cnt += 1
        # p_score.append((i, p_ig_total + p_g[i]))
        average_gap = 0 if len(group_distance) == 0 else average(np.array(group_distance))
        p_score.append((i, round(p_ig_total,4), round(average_gap,4), round(max_data_weight,4)))

    p_score_final = sorted(p_score, key=lambda x: x[1], reverse=True) 
    path = "/home/eilene/Downloads/"
    res_dir = os.path.dirname(path)
    res_path = os.path.join(res_dir, 'result_score.csv')
    res_path2 = os.path.join(res_dir, 'result_cluster_weight.csv')
    # print(res_path)
    if os.path.exists(res_path):
        os.remove(res_path)
    if os.path.exists(res_path2):
        os.remove(res_path2)
    write_score_result(res_path, data_axis, data_weight, final_data, p_score_final, data_count_sum, data_count_new)
    write_weight_result(res_path2, data_weight_cluster, global_cluster_num)
    # # print(p_score_final)
    # for i in range(len(p_score_final)):
    #     # if x1[data_count_sum[p_score_final[i][0]]-1] > start and x1[data_count_sum[p_score_final[i][0]]-1]< end:
    #     print("rank")
    #     print(i)
    #     print(data_axis[data_count_sum[p_score_final[i][0]]-1])
    #     print(data_weight[data_count_sum[p_score_final[i][0]]-1])
    #     print(data_count_sum[p_score_final[i][0]])
    #     print(p_score_final[i])

 
    
    
    
        

        
   

   