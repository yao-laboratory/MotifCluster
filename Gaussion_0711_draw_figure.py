import math
import threading
import time
import gc
import numpy as np
import matplotlib.pyplot as plt
import pybedtools
import os
import warnings
import operator
import copy
import Gaussion_0711_draw_function
# output csv file
import os
import csv,re
import sys
from collections import namedtuple

from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool

MAXIMUM_DISTANCE = 1000
SINGLE_POINT = -5
global_cluster_num = 10

# #delete warning
# warnings.filterwarnings("ignore")

# #print every 10 minutes
# def print_function():
#     # print('Now:', time.strftime('%H:%M:%S',time.localtime()))
#     # print(line_temp)
#     t = threading.Timer(60*5, print_function)
#     t.start()
#     return t

def draw(input_file1, start_axis, end_axis):
    # reload
    gm_name = '/home/eilene/Downloads/GMM'
    means = np.load(gm_name + '_means.npy')
    covar = np.load(gm_name + '_covariances.npy')
    loaded_gm = GaussianMixture(n_components = len(means), covariance_type='full')
    loaded_gm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(covar))
    loaded_gm.weights_ = np.load(gm_name + '_weights.npy')
    loaded_gm.means_ = means
    loaded_gm.covariances_ = covar
    
    line_temp=[]
    final_filename = "/home/eilene/Downloads/" + input_file1
    data_axis = []
    data_weight = []
    arr_final = []
    arr_final_draw=[]
    # draw_input = []
    draw_input=[[] for i in range(global_cluster_num)]
    col_types_csv1=[int,int,float]
    for cnt_temp1 in range(0, global_cluster_num+2):
        col_types_csv1.append(int)
    with open(final_filename) as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        Row=namedtuple('Row',headers)
        id = 0
        for r in f_csv:
            row=Row(*r)
            # print(row)
            # print(type(row.IssueType))
            row=tuple(convert(value) for convert,value in zip(col_types_csv1,row))
            data_axis.append((row[1])) 
            data_weight.append(row[2])# 选择某一列加入到data数组中
            for cnt_temp2 in range(0, global_cluster_num):
                draw_input[cnt_temp2].append(row[cnt_temp2 + 3])
            arr_final.append(row[global_cluster_num + 3])
            arr_final_draw.append(row[global_cluster_num + 4])
            # draw_input.append(draw_input_temp)
            id += 1

    #三种mean值的DBSCAN聚类情况画图
    X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
    value_total = []
    plt.figure("final")
    ax1 = plt.subplot(12,1,1)

    # drawing 
    label_space=[]
    # label_drawing=[]
    i0 = 0
    while(i0 < int(len(data_axis))):
        if (data_axis[i0] - 8) >= int(start_axis) and (data_axis[i0] + 8 + 1) <= int(end_axis):
            label_space.append(i0)
        if (data_axis[i0] + 8 + 1) > int(end_axis):
            break
        i0 += 1

    x1 = data_axis[label_space[0]:label_space[-1] + 1]
    y1 = data_weight[label_space[0]:label_space[-1] + 1]

    # print(label_space[0])
    # print(label_space[-1] + 1)
    for i in range(0, len(loaded_gm.means_)):
        avg_show = str(loaded_gm.means_[i])
        draw_input_temp = draw_input[label_space[0]:label_space[-1] + 1][i]
        print(draw_input_temp)
        Gaussion_0711_draw_function.draw_figure(draw_input_temp, avg_show, i+1, x1, y1, ax1)
    print("second step:\n")
    arr_1 = arr_final[label_space[0]:label_space[-1] + 1]
    print(arr_1)
    print(len(arr_1))
    Gaussion_0711_draw_function.draw_figure(arr_1,"final",11, x1, y1, ax1)  
    # plt.tight_layout()
    # plt.show()    
    # plt.show()
    print("third step:\n")
    arr_2 = arr_final_draw[label_space[0]:label_space[-1] + 1]
    print(arr_2)
    print(len(arr_2))
    Gaussion_0711_draw_function.draw_figure(arr_2,"final_2",12, x1, y1, ax1)  
    plt.tight_layout()    
    plt.show()



    
    
    
        

        
   

   