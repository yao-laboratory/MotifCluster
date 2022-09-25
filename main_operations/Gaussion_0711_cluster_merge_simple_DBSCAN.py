# import math
from email.headerregistry import Group
import threading
import time
import gc
from xml.dom.minidom import Identified
# import numpy as np
import matplotlib.pyplot as plt
import pybedtools
# import os
import warnings
import operator
import copy
import sys
# import csv
from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool

from file_operations.Gaussion_0714_files_operation import *
from main_operations.Gaussion_0711_cluster_merge import union_store_data,store_file

MAXIMUM_DISTANCE = 1000
SINGLE_POINT = -5

#delete warning
warnings.filterwarnings("ignore")

#print every 10 minutes
def print_function():
    # print('Now:', time.strftime('%H:%M:%S',time.localtime()))
    # print(line_temp)
    t = threading.Timer(60*5, print_function)
    t.start()
    return t

#均值
def average(data):
    return np.sum(data)/len(data)

#标准差
def sigma(data,avg):
    sigma_squ=np.sum(np.power((data-avg),2))/len(data)
    return np.power(sigma_squ,0.5)

#高斯分布概率
def prob(data,avg,sig):
    # print(data)
    sqrt_2pi=np.power(2*np.pi,0.5)
    coef=1/(sqrt_2pi*sig)
    powercoef=-1/(2*np.power(sig,2))
    mypow=powercoef*(np.power((data-avg),2))
    return coef*(np.exp(mypow))

# def getSample(cluster_num,cluster_distance,sample_total_num):
#     sample_list=[]
#     initial_num = 0
#     for i in range(cluster_num):
#         sample_num = sample_total_num / cluster_num
#         data_range = cluster_distance[i] * sample_num
#         sample = [round(initial_num + x * cluster_distance[i],2)for x in range(int(sample_num))]
#         sample_list += sample
#         initial_num += data_range
#         # print("sample_list:")
#         # print(sample_list)
#     return sample_list

# ??? how to calculate only one point's distance and how to calculate one point belong to which cluster   
def belong_which_cluster(distance, gm):
    maximum = 0
    cluster_id = SINGLE_POINT
    if distance == 0:
        return cluster_id
    # if distance > 500:
    #     return -1
    for i in range(len(gm.means_)):
        value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        # print("p:")
        if distance == None:
            print("value",value)  
        # print(value)
        if value > maximum:
            maximum = value
            cluster_id = i
    # print("final cluster:")
    # print(cluster_id)
    # print("---------------------")
    return cluster_id

#no need parameter id
def belong_which_cluster_better(cluster_0, cluster_1, id, distance, gm):
    temp_array = []
    if distance > 500:
        return -2
    for i in range(len(gm.means_)):
        # print(id,i)
        # sentence = "{interval_id}\t{cluster_id}\t{log_odds}\n"
        p_value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        if p_value != 0 and p_value != 1:
            log_odd = math.log(p_value/(1-p_value))
            #idth distance
            temp_array.append([id, i, log_odd])
            # f.write(sentence.format(interval_id = id, cluster_id = i, log_odds = log_odd))
    
    # print(temp_array)
    temp_array.sort(key=lambda x:x[2], reverse = True)
    # print(">>>>>>>>>>>>>>>>>>>>>>>")
    # print(temp_array)
    # print("!!!!!!!!!!!!!!")
    # if len(temp_array) > 0:
    #     print(temp_array[0][1])
    # print(cluster_0)
    # print(cluster_1)
    temp_cluster=[]
    if len(temp_array) > 0:
        #if the best log odd belong to cluster_0 or cluster_1
        if temp_array[0][1] == cluster_0 or temp_array[0][1] == cluster_1:
            return temp_array[0][1]
        for i in range(len(temp_array) - 1):
            if abs(temp_array[i][2]) * 1.5 >= abs(temp_array[i+1][2]):
                if temp_array[i+1][1] == cluster_0 or temp_array[i+1][1] == cluster_1:
                    # print("???????????????????????????")
                    # print(temp_array[i+1][1])
                    return temp_array[i+1][1]
            else:
                break;
    return -2

def cluster_and_merge_simple_dbscan(input_file1, start_axis, end_axis):
    line_temp = []
    draw_input = []
    final_filename = "/home/eilene/Downloads/" + input_file1
    print("first, start reading total file:\n")
    data_axis=[]
    weight=[]
    f = open(final_filename,"r")
    with f as lines:
        cluster_id = 0
        for line in lines:
            line = line.split()
            data_axis.append(int(line[1])+ 8)
            weight.append(10)
    f.close()
    data_weight = np.array(weight)

    data=np.array([(data_axis[i+1] - data_axis[i]) for i in range(len(data_axis)-1)])
    # print("data=",data)
    # print(len(data))
    #根据样本数据求高斯分布的平均数
    ave=average(data)
    # print("ave=",ave)
    #根据样本求高斯分布的标准差
    sig=sigma(data,ave)
    # print("sig=",sig)

    #三种mean值的DBSCAN聚类情况画图
    X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
    value_total = []
    plt.figure("final")
    ax1 = plt.subplot(12,1,1)

    # drawing 
    label_space=[]
    # label_drawing=[]
    i0 = 0
    if start_axis == "all" or end_axis =="all":
        while(i0 < int(len(data_axis))):
            # if (data_axis[i0] - 8) >= 6710000 and (data_axis[i0] + 8 + 1) <= 6724000:
            label_space.append(i0)
            # if (data_axis[i0] + 8 + 1) > 6724000:
            #     break
            i0 += 1
    else:
        while(i0 < int(len(data_axis))):
            if (data_axis[i0] - 8) >= int(start_axis) and (data_axis[i0] + 8 + 1) <= int(end_axis):
                label_space.append(i0)
            if (data_axis[i0] + 8 + 1) > int(end_axis):
                break
            i0 += 1

    x1 = data_axis[label_space[0]:label_space[-1] + 1]
    y1 = data_weight[label_space[0]:label_space[-1] + 1]
    print("len x1",len(x1))
    # y1 = data_weight[label_space[0]:label_space[-1] + 1]

    gc.disable()
    db_temp = DBSCAN(eps = ave, min_samples = 8).fit(X_ORIGIN, y = None, sample_weight = data_weight)
    # gc.enable()
    # print("fffffffffffffff")
    labels = db_temp.labels_
    label_values = []
    init_value = -2
    flag_current = init_value
    value = init_value
    # cnt = i
    # print("labels num:")
    # print(len(labels))
    print(".........")
    print(labels)
    for i in range(0,len(labels)):
        if i == len(labels) - 1:
            if labels[i] != -1:
                label_values += [i]
            else: 
                # print("value:",value)
                label_values += [value]
        if labels[i] == -1:
            continue
        if flag_current == init_value:
            label_values += [i]
            flag_current = labels[i]
            # print("flag_current2:",flag_current)
            # print("labels[i]:",labels[i])
        if flag_current != labels[i]:
            label_values += [value]
            label_values += [i]
            flag_current = labels[i]
            # print(label_values)
            # print("value:", value)
            # print("i:", i)
        value = i
        # print("label_values num:")
        # print(len(label_values))
        # print(label_values)
        
        # #label value is like [0,3,4,4,6,9]
    value_total.append(label_values)
    
    label_drawing = labels[label_space[0]:label_space[-1]+1]
    print("----------------")
    print(label_drawing)
    print(len(label_drawing))
    print("----------------")
    draw_input.append(label_drawing)

    
    # create and open file
    # print("lalalalala")
    # print(len(value_total))
    for cnt in range(len(value_total)):
        # cnt_temp = cnt+1
        final_filename ="/home/eilene/Downloads/total_single_DBSCAN%d.bdg"%cnt
        f = open(final_filename,"w")

        # write data to file 
        i = 0
        # f.write("genename start end")
        while(i < len(value_total[cnt])):
            sentence = "chr6\t{start}\t{end}\t{num}\n"
            # print("start and end:")
            # print(data_axis[i],data_axis[i+1])
            num_start = value_total[cnt][i]
            num_end = value_total[cnt][i+1]
            # print("*************************")
            # print(num_start, num_end)
            # if (num_start == num_end):
            f.write(sentence.format(start = data_axis[num_start], end = data_axis[num_end] + 1,num = 1))
            # else:
            #     f.write(sentence.format(start = data_axis[num_start], end = data_axis[num_end] + 1,num = 1))
            #     f.write(sentence.format(start = data_axis[num_start]-8,end = value_total[cnt][i+1], num = 1))
            # f.write(sentence.format(start = value_total[cnt][i],end = value_total[cnt][i+1],num = 1))
            i += 2
            
        # close file
        f.close() 
    cluster=[]  
    filenames = []

    print("second, start reading total file:\n")
    arr_final=[]
    arr_outliers=[]
    # data_axis_final_show = data_axis[label_space[0] : label_space[-1]+1]
    # print(label_space[0])
    # print(label_space[-1]+1)
    # print(len(data_axis_final_show))
    label_drawing_final=[]
    # number_cnt = label_space[0 : -1]
    # number_cnt.append(label_space[-1])
    # print(label_space)
    # print(number_cnt)
    sequence=[]
    # for i in range(len(data_axis)):
    #     if data_axis[i] >= 0 and data_axis[i] <= 110270000:
    #         data_axis_final_show.append(int(data_axis[i]))
    #         number_cnt.append(i)
    # cluster_belong=[]
    data_count=[]
    data_sum=[]
    data_count_sum=[]
    union_store_data(final_filename,x1,arr_final,data_sum,sequence,data_count,data_count_sum,arr_outliers)    

    print("*******************************************")
    # print(arr_final)
    print(len(arr_final))
    # print(arr_outliers)
    print(len(arr_outliers))
    # print(x1)
    print(len(x1))
    # print(sequence)
    print("*******************************************")
    # if plot_flag == True:
    #     Gaussion_Draw_function_0705.draw_figure(arr_final,"final",11, x1, y1, ax1)  
    # plt.tight_layout()    
    # plt.show()

    # print(cluster_belong)
    # print(len(cluster_belong))
    # print(data_sum)
    print(len(data_sum))
    print(len(data_count))
    # print(data_count)
    print("7777777777777777777")


    print("88888888888888888888888")
    # print(data_count)
    print(len(data_count))
    print("8888888888888888888888")
    
    # data_count_sum = []
    # cnt = 0
    # for j in range(len(data_count_new)):
    #         cnt += data_count_new[j]
    #         # print(j)
    #         # print(cnt)
    #         data_count_sum.append(cnt)
    # # print(data_count_new[0])
    # # print(data_count_sum[0])
    # print(len(data_count_sum))   
  
    #output csv file 
    path = "/home/eilene/Downloads/"
    # res_dir = os.path.dirname(path)
    # res_path = os.path.join(res_dir, 'result_simple_DBSCAN.csv')
    # res_path2 = os.path.join(res_dir, 'result_middle_simple_DBSCAN.csv')
    # res_path3 = os.path.join(res_dir, 'result_draw_simple_DBSCAN.csv')
    # print(res_path3)
    # if os.path.exists(res_path):
    #     os.remove(res_path)
    # if os.path.exists(res_path2):
    #     os.remove(res_path2)
    # if os.path.exists(res_path3):
    #     os.remove(res_path3)
    # write_result(res_path, x1, y1, final_data)
    # write_middle_result(res_path2, data_count_new, cluster_belong_new, data_count_sum)
    print(len(x1))
    print(len(draw_input[0]))
    print(len(arr_final))
    store_file(path,x1,y1,None,data_count,None,data_count_sum,draw_input,None,arr_final,None)
    # write_draw_input_single_DBSCAN(res_path3, x1, draw_input[0],arr_final)
    
    # if plot_flag == True:
    #     Gaussion_Draw_function_0705.draw_figure(arr_final_draw,"final_2",12, x1, y1, ax1)  
    #     plt.tight_layout()    
    #     plt.show()



    
    
    
        

        
   

   