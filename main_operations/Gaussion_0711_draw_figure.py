import math
import threading
import time
import gc
import matplotlib as mpl
# import numpy as np
# import matplotlib.pyplot as plt
import pybedtools
import os
import warnings
# import operator
import copy
# output csv file
import csv,re
import sys
from collections import namedtuple
from draw_operations.Gaussion_0711_draw_function import *

from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool

MAXIMUM_DISTANCE = 1000
SINGLE_POINT = -5
# global_cluster_num = 10

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
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
    # reload GMM Model
    gm_name = '/home/eilene/Downloads/GMM'
    means = np.load(gm_name + '_means.npy')
    covar = np.load(gm_name + '_covariances.npy')
    loaded_gm = GaussianMixture(n_components = len(means), covariance_type='full')
    loaded_gm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(covar))
    loaded_gm.weights_ = np.load(gm_name + '_weights.npy')
    loaded_gm.means_ = means
    loaded_gm.covariances_ = covar
    global_cluster_num = len(loaded_gm.means_)
    print("global_cluster_num", global_cluster_num)
    
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
            if input_file1 == "result_draw.csv":
                arr_final_draw.append(row[global_cluster_num + 4])
            # draw_input.append(draw_input_temp)
            id += 1

    #三种mean值的DBSCAN聚类情况画图
    X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
    value_total = []
    # Fig,Axes=plt.subplots(global_cluster_num+2,1,sharex='col',sharey='row',figsize=(50,10))
    Fig,Axes=plt.subplots(global_cluster_num+2,1,sharex='col',sharey='row')
    # plt.setp(Axes[12], ylabel='y axis label')
    # for i in range(global_cluster_num+2):
    #     Axes[i].set_aspect(30)
    #     Axes[i].set_xlabel(None)
    #     Axes[i].set_ylabel(None)
    # ax1 = plt.subplot(12,1,1)
    # ax1.axes.xaxis.set_visible(False)

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
    print(x1)
    # print(draw_input)
    print(label_space[0])
    print(label_space[-1] + 1)
    print(draw_input[0][label_space[0]:label_space[-1] + 1])

    # print(label_space[0])
    # print(label_space[-1] + 1)
    print(loaded_gm.means_)
    for i in range(0, len(loaded_gm.means_)):
        avg_show = str(loaded_gm.means_[i])
        draw_input_temp = draw_input[i][label_space[0]:label_space[-1] + 1]
        print(draw_input_temp)
        draw_figure(draw_input_temp, avg_show, i, x1, y1, Axes)
    print("second step:\n")
    arr_1 = arr_final[label_space[0]:label_space[-1] + 1]
    print(arr_1)
    print(len(arr_1))
    draw_figure(arr_1,"final",global_cluster_num, x1, y1, Axes)  
    # plt.tight_layout()
    # plt.show()    
    # plt.show()
    print("third step:\n")
    arr_2 = arr_final_draw[label_space[0]:label_space[-1] + 1]
    print(arr_2)
    print(len(arr_2))
    draw_figure(arr_2,"final_2",global_cluster_num+1, x1, y1, Axes)

    for i in range(global_cluster_num+2):
        Axes[i].set_aspect(30)
        plt.setp(Axes[11], xlabel='')
        plt.setp(Axes[11], ylabel='')
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    plt.ylim(0, 10) 
    plt.savefig('tmp.pdf', bbox_inches='tight')
    #plt.savefig(pp, format='pdf')
    #pp.close()
    # plt.tight_layout()    
    plt.show()



    
    
    
        

        
   

   