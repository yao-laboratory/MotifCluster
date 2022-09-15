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
# import Gaussion_Draw_function_0711
# output csv file
# import os
# import re
import sys
# import csv
from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool

from file_operations.Gaussion_0714_files_operation import *

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

def union_store_data(final_filename,x1,arr_final,data_sum,sequence,data_count,data_count_sum,arr_outliers):
    with open(final_filename,"r") as lines:
        class_id = 0
        flag = False
        for line in lines:
            line = line.split()
            # print(line)
            data_temp=[]
            for i in range(len(x1)):
                if int(x1[i]) > int(line[2]):
                    break
                elif int(x1[i]) >= int(line[1]) and int(x1[i]) <= int(line[2])-1:
                    # if((len(arr_final) - 1) == i):
                    #     continue
                    data_temp.append(x1[i])
                    data_sum.append(x1[i])
                    arr_final.append(class_id)
                    sequence.append(i)
                    flag = True        
            if flag == True:
                class_id += 1
            if len(data_temp) == 0:
                continue
            data_count.append(len(data_temp))          

    for i in range(len(x1)):
        if i not in sequence:
            arr_final.insert(i,-1)
            arr_outliers.append(i)
            sequence.insert(i,i)
            # class_belong.insert(i, -1)
            # data_count.insert(i, 1)
            data_sum.insert(i,x1[i])
    print(arr_final)
    print(arr_outliers)
    print(sequence)
    print(data_count)
    print(data_sum)
    data_count_temp = copy.deepcopy(data_count)
    # print(class_belong)
    # print(data_count)
    cnt = 0
    cnt_total = 0
    # cnt_2 = 0
    for j in range(len(data_count_temp)):
        cnt_total += data_count_temp[j]
    # print("????????????????????")
    # print(data_count_temp)
    # print(len(data_count_temp))
    # print("????????????????????")
    cnt_temp = 0
    for i in range(len(arr_final)):
        if arr_final[i] > -1:
            cnt += 1
        elif arr_final[i] == -1:
            # print(i,cnt)
            if cnt == 0:
                data_count.insert(i,1)
                # class_belong.insert(i, -1)
                cnt_temp += 1
            elif cnt > 0:
                if cnt == cnt_total:
                    data_count.append(1)
                    # class_belong.append(-1)
                else:
                    cnt_2 = 0
                    for j in range(len(data_count_temp)):
                        # print("????????????????????")
                        # print(len(data_count_temp))
                        if data_count_temp[j] != -1:
                            cnt_2 += data_count_temp[j]
                        # print(j, data_count_temp[j], cnt_2)
                        # print("????????????????????")
                        if cnt_2 == cnt:
                            # print("????????????????????")
                            # print(cnt_temp+j+1)
                            # print("????????????????????")
                            data_count.insert(j + 1 + cnt_temp, 1)
                            # class_belong.insert(j + 1 + cnt_temp, -1)
                            cnt_temp += 1
    # for id in class_belong:
    #     if id == -5:
    #         id = -1
        
    # # print(number_cnt)
    # print("*******************************************")
    # # print(arr_final)
    # print(len(arr_final))
    # # print(arr_outliers)
    # print(len(arr_outliers))
    # # print(x1)
    # print(len(x1))
    # # print(sequence)
    # print("*******************************************")
    # # if plot_flag == True:
    # #     Gaussion_Draw_function_0705.draw_figure(arr_final,"final",11, x1, y1, ax1)  
    # # plt.tight_layout()    
    # # plt.show()

    # # print(class_belong)
    # # print(len(class_belong))
    # # print(data_sum)
    # print(len(data_sum))
    # print(len(data_count))
    # # print(data_count)
    # print("7777777777777777777")
    cnt = 0
    for j in range(len(data_count)):
            cnt += data_count[j]
            # print(j)
            # print(cnt)
            data_count_sum.append(cnt)
    # print(data_count_new[0])
    # print(data_count_sum[0])
    print(len(data_count_sum)) 

# ??? how to calculate only one point's distance and how to calculate one point belong to which cluster   
def belong_which_class(distance, gm):
    maximum = 0
    class_id = SINGLE_POINT
    if distance == 0 or distance > 500:
        return class_id
    # if distance > 500:
    #     return -1
    for i in range(len(gm.means_)):
        value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        # print("p:")
        # print(value)
        if value > maximum:
            maximum = value
            class_id = i
    # print("final cluster:")
    # print(class_id)
    # print("---------------------")
    return class_id

#no need parameter id
def belong_which_class_better(class_0, class_1, id, distance, gm):
    temp_array = []
    if distance > 500:
        return -2
    for i in range(len(gm.means_)):
        # print(id,i)
        # sentence = "{interval_id}\t{class_id}\t{log_odds}\n"
        p_value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        if p_value != 0 and p_value != 1:
            log_odd = math.log(p_value/(1-p_value))
            #idth distance
            temp_array.append([id, i, log_odd])
            # f.write(sentence.format(interval_id = id, class_id = i, log_odds = log_odd))
    
    # print(temp_array)
    temp_array.sort(key=lambda x:x[2], reverse = True)
    # print(">>>>>>>>>>>>>>>>>>>>>>>")
    # print(temp_array)
    # print("!!!!!!!!!!!!!!")
    # if len(temp_array) > 0:
    #     print(temp_array[0][1])
    # print(class_0)
    # print(class_1)
    # temp_cluster=[]
    if len(temp_array) > 0:
        #if the best log odd belong to class_0 or class_1
        if temp_array[0][1] == class_0 or temp_array[0][1] == class_1:
            return temp_array[0][1]
        for i in range(len(temp_array) - 1):
            if abs(temp_array[i][2]) * 1.5 >= abs(temp_array[i+1][2]):
                if temp_array[i+1][1] == class_0 or temp_array[i+1][1] == class_1:
                    # print("???????????????????????????")
                    # print(temp_array[i+1][1])
                    return temp_array[i+1][1]
            else:
                break;
    return -2

#pre merge to divide class
def pre_merge_divide_class(final_filename,x1,gm,arr_final,data_sum,sequence,data_count,class_belong,average_distance):
    with open(final_filename,"r") as lines:
        class_id = 0
        flag = False
        for line in lines:
            line = line.split()
            # print(line)
            data_temp=[]
            for i in range(len(x1)):
                if int(x1[i]) > int(line[2]):
                    break
                elif int(x1[i]) >= int(line[1]) and int(x1[i]) <= int(line[2])-1:
                    # if((len(arr_final) - 1) == i):
                    #     continue
                    data_temp.append(x1[i])
                    data_sum.append(x1[i])
                    arr_final.append(class_id)
                    sequence.append(i)
                    flag = True        
            if flag == True:
                class_id += 1
            if len(data_temp) == 0:
                continue
            data_count.append(len(data_temp))
            # print(len(data_temp))
            # print(data_temp)
            data_distance_temp_=np.array([(int(data_temp[i+1]) - int(data_temp[i])) for i in range(len(data_temp)-1)])
            # print("data_distance=",data_distance_temp_)
            #根据样本数据求高斯分布的平均数
            ave_temp = 0 if len(data_distance_temp_) == 0 else average(data_distance_temp_)
            # print("ave_temp",ave_temp)
            # one point counts how many distance and score
            ave_final = MAXIMUM_DISTANCE if len(data_distance_temp_) == 0 else average(data_distance_temp_)
            average_distance.append(ave_final)
            # print(data_distance_temp_)
            # print("ave=",ave_temp)
            # print("ave_final=",ave_final)
            class_num = belong_which_class(ave_temp, gm)
            class_belong.append(class_num)        
    # f.close()
def pre_merge_store_data(x1,arr_final,data_sum,sequence,data_count,class_belong,arr_outliers):
        # add_outliers
    for i in range(len(x1)):
        if i not in sequence:
            arr_final.insert(i,-1)
            arr_outliers.append(i)
            sequence.insert(i,i)
            # class_belong.insert(i, -1)
            # data_count.insert(i, 1)
            data_sum.insert(i,x1[i])
    print(arr_final)
    # arr_final.insert(18,-1)
    # arr_final.insert(19,-1)
    # arr_final.append(-1)
    # arr_final.append(-1)
    # print(arr_final)
    data_count_temp = copy.deepcopy(data_count)
    # print(class_belong)
    # print(data_count)
    cnt = 0
    cnt_total = 0
    # cnt_2 = 0
    for j in range(len(data_count_temp)):
        cnt_total += data_count_temp[j]
    # print("????????????????????")
    # print(data_count_temp)
    # print(len(data_count_temp))
    # print("????????????????????")
    cnt_temp = 0
    for i in range(len(arr_final)):
        if arr_final[i] > -1:
            cnt += 1
        elif arr_final[i] == -1:
            # print(i,cnt)
            if cnt == 0:
                data_count.insert(i,1)
                class_belong.insert(i, -1)
                cnt_temp += 1
            elif cnt > 0:
                if cnt == cnt_total:
                    data_count.append(1)
                    class_belong.append(-1)
                else:
                    cnt_2 = 0
                    for j in range(len(data_count_temp)):
                        # print("????????????????????")
                        # print(len(data_count_temp))
                        if data_count_temp[j] != -1:
                            cnt_2 += data_count_temp[j]
                        # print(j, data_count_temp[j], cnt_2)
                        # print("????????????????????")
                        if cnt_2 == cnt:
                            # print("????????????????????")
                            # print(cnt_temp+j+1)
                            # print("????????????????????")
                            data_count.insert(j + 1 + cnt_temp, 1)
                            class_belong.insert(j + 1 + cnt_temp, -1)
                            cnt_temp += 1
    # for id in class_belong:
    #     if id == -5:
    #         id = -1
        
    # # print(number_cnt)
    # print("*******************************************")
    # # print(arr_final)
    # print(len(arr_final))
    # # print(arr_outliers)
    # print(len(arr_outliers))
    # # print(x1)
    # print(len(x1))
    # # print(sequence)
    # print("*******************************************")
    # # if plot_flag == True:
    # #     Gaussion_Draw_function_0705.draw_figure(arr_final,"final",11, x1, y1, ax1)  
    # # plt.tight_layout()    
    # # plt.show()

    # # print(class_belong)
    # print(len(class_belong))
    # # print(data_sum)
    # print(len(data_sum))
    # print(len(data_count))
    # # print(data_count)
    # print("7777777777777777777")
    
#merge to the left
def merge(data_sum,gm,data_count,class_belong,data_count_new,class_belong_new):
    sum_count = 0
    # set_value = False
    class_id = -3
    class_id_2 = -3
    # filename ="/home/eilene/Downloads/statistic_logodds.bdg"
    # f = open(filename,"w")
    i = 0
    # for i in range(len(data_count) - 3): 
    while i <= len(data_count) - 1:
        sum_count = 0
        # if sum_count >= (len(data_sum) - 1):
        #     break;
        j = 0
        while j <= i:
            sum_count += data_count[j]
            j += 1
        if i == 0:
            data_count_i = data_count[i]
            class_belong_i = class_belong[i]
        elif i != 0:
            data_count_i = data_count_new.pop()
            class_belong_i = class_belong_new.pop()
        #bundary condition
        if (i+1) > (len(data_count) - 1):
            data_count_new.append(data_count_i)
            class_belong_new.append(class_belong_i)
            break
        elif (i+2) > (len(data_count) - 1):
            #not finished
            data_count_new.append(data_count_i)
            data_count_new.append(data_count[i+1])
            class_belong_new.append(class_belong_i)
            class_belong_new.append(class_belong[i+1])
            break
        else:
            distance = data_sum[sum_count] - data_sum[sum_count - 1]
            distance_2 = data_sum[sum_count + 1] - data_sum[sum_count]
            if data_count[i+1] > 1 :
                if data_count_i > 1:
                    if class_belong_i == class_belong[i+1]:
                        class_id = belong_which_class_better(class_belong_i, class_belong[i+1], i, distance, gm)
                        # print("1111111111111111111")
                        # print(class_id)
                        #check gap
                        if class_id == class_belong_i:
                            data_count_new.append(data_count_i + data_count[i+1])
                            class_belong_new.append(class_belong_i)
                        else:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])  
                            class_belong_new.append(class_belong_i)
                            class_belong_new.append(class_belong[i+1])

                    else:
                        #not merge
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])  
                        class_belong_new.append(class_belong_i)
                        class_belong_new.append(class_belong[i+1])
                elif data_count_i == 1:
                    class_id = belong_which_class_better(class_belong_i, class_belong[i+1], i, distance, gm)
                    # print("22222222")
                    # print(class_id)
                    if class_id == class_belong[i+1]:
                        data_count_new.append(data_count_i + data_count[i+1])
                        class_belong_new.append(class_belong[i+1])
                    else:
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])  
                        class_belong_new.append(class_belong_i)
                        class_belong_new.append(class_belong[i+1]) 
                i += 1   
            elif data_count[i+1] == 1:
                if data_count_i > 1 and data_count[i+2] == 1:
                    class_id = belong_which_class_better(class_belong_i, class_belong[i+1], i, distance, gm)
                    # print("33333333")
                    # print(class_id)
                    if class_id == class_belong_i:
                        data_count_new.append(data_count_i + data_count[i+1])
                        class_belong_new.append(class_belong_i)
                    else:
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])  
                        class_belong_new.append(class_belong_i)
                        class_belong_new.append(class_belong[i+1]) 
                    i += 1
                elif data_count_i > 1 and data_count[i+2] > 1:
                    # check both side, which is better, not done yet
                    #check left side
                    # print("testtest")
                    distance = data_sum[sum_count] - data_sum[sum_count - 1]
                    distance_2 = data_sum[sum_count + 1] - data_sum[sum_count]
                    # print(sum_count)
                    # print(data_count_i)
                    # print(data_count[i+1])
                    # print(data_count[i+2])
                    # print(distance)
                    # print(distance_2)
                    # print("testfinish")
                    class_id = belong_which_class_better(class_belong_i, class_belong[i+1], i, distance, gm)
                    class_id_2 = belong_which_class_better(class_belong[i+1], class_belong[i+2], i, distance_2, gm)
                    # print("444444444441")
                    # print(class_id)
                    # print("44444444444442")
                    # print(class_id_2)
                    if class_belong_i != class_belong[i+2]:
                        # print("44444444444443")
                        if class_id  == class_belong_i and class_id_2 == class_belong[i+2]:
                            #not finished
                            data_count_new.append(data_count_i + data_count[i+1])
                            data_count_new.append(data_count[i+2])
                            class_belong_new.append(class_belong_i)
                            class_belong_new.append(class_belong[i+2])
                            # print("a")
                        else:
                            if class_id  == class_belong_i:
                                data_count_new.append(data_count_i + data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                                # print("b")
                            # elif class_id_2 != class_belong[i+2]:
                            #     data_count_new.append(data_count_i)
                            #     data_count_new.append(data_count[i+1])  
                            #     data_count_new.append(data_count[i+2])  
                            #     class_belong_new.append(class_belong_i)
                            #     class_belong_new.append(class_belong[i+1]) 
                            #     class_belong_new.append(class_belong[i+2]) 
                            if class_id_2 == class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1]+ data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                                # print("c")
                            elif class_id  != class_belong_i and class_id_2 != class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+1])
                                class_belong_new.append(class_belong[i+2])
                                
                                # print("d")
                                # print(data_count_new)
                                # print(class_belong_new)
                                # print(data_count_i)
                                # print(data_count[i+1])
                                # print(data_count[i+2])
                    elif class_belong_i == class_belong[i+2]:
                        #merge together
                        if class_id  == class_belong_i and class_id_2 == class_belong[i+2]:
                            #not finished
                            data_count_new.append(data_count_i + data_count[i+1] + data_count[i+2])
                            class_belong_new.append(class_belong_i)
                            # print("a")
                        else:
                            if class_id  == class_belong_i:
                                data_count_new.append(data_count_i + data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                                # print("c")
                            if class_id_2 == class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1] + data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                                # print("d")
                            elif class_id != class_belong_i and class_id_2 != class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+1])
                                class_belong_new.append(class_belong[i+2])
                                # print("e")
                    i += 2
                    
                elif data_count_i == 1:  
                    # if class_belong_i == -1 and class_belong[i+1] == -1:
                    #     data_count_new.append(data_count_i)
                    #     data_count_new.append(data_count[i+1])
                    #     class_belong_new.append(class_belong_i)
                    #     class_belong_new.append(class_belong[i+1])
                    # elif class_belong_i != -1 and class_belong[i+1] == -1:
                    #     class_id = belong_which_class_better(class_belong_i, class_belong[i+1], i, distance, gm)
                    #     # print("5555555555555")
                    #     # print(class_id)
                    #     if class_id == class_belong_i:
                    #         data_count_new.append(data_count_i + data_count[i+1])
                    #         class_belong_new.append(class_belong_i)
                    #     else:
                    #         data_count_new.append(data_count_i)
                    #         data_count_new.append(data_count[i+1])
                    #         class_belong_new.append(class_belong_i)
                    #         class_belong_new.append(class_belong[i+1])
                    # elif class_belong_i == -1 and class_belong[i+1] != -1:
                    #     class_id = belong_which_class_better(class_belong_i, class_belong[i+1], i, distance, gm)
                    #     # print("66666666666")
                    #     # print(class_id)
                    #     if class_id == class_belong[i+1]:
                    #         data_count_new.append(data_count_i + data_count[i+1])
                    #         class_belong_new.append(class_belong[i+1])
                    #     else:
                    #         data_count_new.append(data_count_i)
                    #         data_count_new.append(data_count[i+1])
                    #         class_belong_new.append(class_belong_i)
                    #         class_belong_new.append(class_belong[i+1])
                    if class_belong_i != -1 and class_belong[i+1] != -1:
                        class_id = belong_which_class(distance, gm)
                        # print("7777777777")
                        # print(class_id)
                        if class_belong_i == class_belong[i+1]:
                            if class_id != SINGLE_POINT:
                                data_count_new.append(data_count_i + data_count[i+1])
                                class_belong_new.append(class_id)
                            else:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+1])
                        elif class_belong_i != class_belong[i+1]:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])
                            class_belong_new.append(class_belong_i)
                            class_belong_new.append(class_belong[i+1])
                    else:  
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])
                            class_belong_new.append(class_belong_i)
                            class_belong_new.append(class_belong[i+1])  
                    i += 1
    # print("88888888888888888888888")
    # # print(data_count)
    # print(len(data_count))
    # # print(class_belong)
    # print(len(class_belong))
    # print("*******************")
    # # print(data_count_new)
    # print(len(data_count_new))
    # # print(class_belong_new)
    # print(len(class_belong_new))
    # print("8888888888888888888888")
def merge_store_data(data_count_new,data_count_sum,class_belong_new,final_data,arr_final,arr_final_draw):
    cnt = 0
    for j in range(len(data_count_new)):
            cnt += data_count_new[j]
            # print(j)
            # print(cnt)
            data_count_sum.append(cnt)
    # print(data_count_new[0])
    # print(data_count_sum[0])
    print(len(data_count_sum))   

    for i in range(len(data_count_new)):
        if data_count_new[i] == 1:
            if class_belong_new[i] == -1:
                final_data.append(-1)
            else:
                final_data.append(SINGLE_POINT)
            continue
        cnt = data_count_new[i]
        for j in range(cnt):
            final_data.append(class_belong_new[i]) 
    cnt = 0
    count = 0
    for i in range(len(data_count_new)):
        if data_count_new[i] == 1:
            if class_belong_new[i] == -1:
                arr_final_draw.append(-1)
            else:
                arr_final_draw.append(count)
                count += 4
            continue
        cnt = data_count_new[i]
        for j in range(cnt):
            arr_final_draw.append(count)
        count += 4
    # print(arr_final_2)
    # print(arr_final)
    # print(arr_final_draw)
    # print(final_data)
    # print(len(arr_final_draw)) 
    
#output csv file     
def store_file(path,x1,y1,gm,data_count_new,class_belong_new,data_count_sum,draw_input,final_data,arr_final,arr_final_draw):        
    #output csv file 
    if class_belong_new is None:
        res_dir = os.path.dirname(path)
        res_path = os.path.join(res_dir, 'result_union.csv')
        res_path2 = os.path.join(res_dir, 'result_middle_union.csv')
        res_path3 = os.path.join(res_dir, 'result_draw_union.csv')
        print(res_path)
        if os.path.exists(res_path):
            os.remove(res_path)
        if os.path.exists(res_path2):
            os.remove(res_path2)
        if os.path.exists(res_path3):
            os.remove(res_path3)
        # print("x1",len(x1))
        # print(x1)
        # print("final_data",len(final_data))
        # print(final_data)
        # write_result(res_path, x1, y1, final_data)
        # write_middle_result(res_path2, data_count_new, class_belong_new, data_count_sum)
        write_draw_input(res_path3, x1, y1, draw_input, len(gm.means_), arr_final, arr_final_draw)
    else:
        res_dir = os.path.dirname(path)
        res_path = os.path.join(res_dir, 'result.csv')
        res_path2 = os.path.join(res_dir, 'result_middle.csv')
        res_path3 = os.path.join(res_dir, 'result_draw.csv')
        print(res_path)
        if os.path.exists(res_path):
            os.remove(res_path)
        if os.path.exists(res_path2):
            os.remove(res_path2)
        if os.path.exists(res_path3):
            os.remove(res_path3)
        # print("x1",len(x1))
        # print(x1)
        # print("final_data",len(final_data))
        # print(final_data)
        write_result(res_path, x1, y1, final_data)
        write_middle_result(res_path2, data_count_new, class_belong_new, data_count_sum)
        write_draw_input(res_path3, x1, y1, draw_input, len(gm.means_), arr_final, arr_final_draw)
    
        # if plot_flag == True:
        #     Gaussion_Draw_function_0705.draw_figure(arr_final_draw,"final_2",12, x1, y1, ax1)  
        #     plt.tight_layout()    
        #     plt.show()

def cluster_and_merge(input_file1, start_axis, end_axis, merge_switch):
    if merge_switch == "open":
        merge_switch = True
    else:
        merge_switch = False   
    line_temp = []
    draw_input = []
    final_filename = "/home/eilene/Downloads/" + input_file1
    print("first, start reading total file:\n")
    data_axis=[]
    weight=[]
    f = open(final_filename,"r")
    with f as lines:
        class_id = 0
        for line in lines:
            line = line.split()
            # print(line)
            # center pos
            # data_axis.append(int(line[1])+ 8)
            raw_weight = ''.join(line[7][8:])
            mark_1 = raw_weight.rfind('e')
            mark_2 = raw_weight.rfind('-')
            num_part1 = float(raw_weight[0:mark_1])
            num_part2 = -int(raw_weight[mark_2 + 1:])
            # if num_part1 * math.pow(10,num_part2) <= 0.01:
            data_axis.append(int(line[1])+ 8)
            num = -math.log10(num_part1 * math.pow(10,num_part2))
            #original
            weight.append(num)
            # weight.append(10)

    f.close()
    # print(data_axis[0],data_axis[1])
    # print(data_axis)
    # print(len(data_axis))
    # rewrite data_weight
    data_weight = np.array(weight)
    # data_weight = np.random.randint(1,11,size=len(data_axis))
    # print("data weight=",data_weight)
    # print(len(data_weight))

    data=np.array([(data_axis[i+1] - data_axis[i]) for i in range(len(data_axis)-1)])
    # print("data=",data)
    # print(len(data))
    #根据样本数据求高斯分布的平均数
    ave=average(data)
    # print("ave=",ave)
    #根据样本求高斯分布的标准差
    sig=sigma(data,ave)
    # print("sig=",sig)

    #相邻点间距离为X轴的GMM拟合
    X_DISTANCE = data.reshape(len(data), 1)
    x_distance_temp = []
    for value in X_DISTANCE:
        if value <= 500:
            x_distance_temp.append(value)
    X_DISTANCE = np.array(x_distance_temp)
    # print(X_DISTANCE)
    # Set up a range of cluster numbers to try
    n_range = range(1,11)

    # Create empty lists to store the BIC and AIC values
    bic_score = []
    aic_score = []
    # max = 0
    component_num = 1
    Difference_value = 1
    min_score = 0xffffffff
    # print(min_score)
    global_class_num = 0
    # Loop through the range and fit a model
    for i in n_range:
        gm = GaussianMixture(n_components=i, 
                            random_state=100, 
                            n_init=10)
        gm.fit(X_DISTANCE)
        # print("\nMeans:\n", gm.means_)
        # Append the BIC and AIC to the respective lists
        bic_score.append(gm.bic(X_DISTANCE))
        aic_score.append(gm.aic(X_DISTANCE))
        # print(i)
        # print(bic_score[i-1])
        # print(aic_score[i-1])
        if aic_score[i-1] < min_score:
            # print(aic_score[i-1])
            min_score = aic_score[i-1]
            global_class_num = i
    print("global_class_num num:")
    print(global_class_num)
    gm = GaussianMixture(n_components = global_class_num, n_init = 10, random_state = 100)
    gm.fit(X_DISTANCE)
    # don't delete
    # print("Weights: ", gm.weights_)
    # print("\nMeans:\n", gm.means_)
    class_means_all = gm.means_
    # print("\nCovariances:\n", gm.covariances_)
    # cluster_covariances_all = gm.covariances_

    # don't delete
    # print("\nCovariances:\n", gm.covariances_)

    # area = np.pi * 2**2  # 点面积 
    # 画散点图

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
    # print("lalalalala")
    # print(len(x1))
    # print(label_space[0])
    # print(label_space[-1] + 1)
    for i in range(0, len(gm.means_)):
        # print("iiiiiiiiii")
        # print(i,len(gm.means_))
        gc.disable()
        #ORIGINAL
        db_temp = DBSCAN(eps = gm.means_[i] + 2 * math.sqrt(gm.covariances_[i]), min_samples = 8).fit(X_ORIGIN, y = None, sample_weight=data_weight)
        # gc.enable()
        # print("fffffffffffffff")
        labels = db_temp.labels_
        avg_show = str(gm.means_[i])
        print("means_"+str(i)+":\n"+str(gm.means_[i]))
        # print("labels_"+str(i)+":\n"+str(labels))
        # for i in range(int(len(labels)/1000)):
        #     print(labels[i])
        label_values = []
        init_value = -2
        flag_current = init_value
        value = init_value
        cnt = i
        # print("labels num:")
        # print(len(labels))
        print(".........")
        print(labels)
        for i in range(0,len(labels)):
            # print("i:",i)
            # print("labels[i]:",labels[i]) 
            # print("len(labels) - 1",len(labels) - 1)
            # print("data axis",len(data_axis))
            # print("value:",value)
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
        # avg_set.append(avg_show)
        # print(label_space[0])
        # print(label_space[-1] + 1)
        # print(x1,y1)
        # print(len(value_total))
        # if plot_flag == True:
        #     Gaussion_Draw_function_0705.draw_figure(label_drawing, avg_show, cnt+1, x1, y1, ax1)

    # plt.tight_layout()   
    # plt.show()
    
    # save GMM MODEL object
    gm_name = '/home/eilene/Downloads/GMM'
    np.save(gm_name + '_weights', gm.weights_, allow_pickle=False)
    np.save(gm_name + '_means', gm.means_, allow_pickle=False)
    np.save(gm_name + '_covariances', gm.covariances_, allow_pickle=False)
    
    # create and open file
    # print("lalalalala")
    # print(len(value_total))
    for cnt in range(len(value_total)):
        # cnt_temp = cnt+1
        filename ="/home/eilene/Downloads/class%d.bdg"%cnt
        f = open(filename,"w")

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
    classes=[]  
    filenames = []
    for cnt in range(len(value_total)):
        # cnt_temp = cnt+1
        filename ="/home/eilene/Downloads/class%d.bdg"%cnt
        classes.append(pybedtools.example_bedtool(filename))
        # print("cluster_"+str(cnt)+":\n")
        classes[cnt].head()
        filenames.append(filename)
        # print("------------------------------------")
        # print(filenames)
    final_filename = "/home/eilene/Downloads/total.bdg"
    BedTool().union_bedgraphs(i=filenames, output=final_filename)

    # cmd = "bedtools unionbedg -i "  + filenames +"-output " + final_filename
    # print(cmd)
    # output = os.system(cmd)
    print("merge_switch",merge_switch)
    if not merge_switch:
        print("second, start reading total file with not merge:\n")
        arr_final=[]
        arr_outliers=[]
        sequence=[]
        data_count=[]
        data_sum=[]
        data_count_sum=[]
        union_store_data(final_filename,x1,arr_final,data_sum,sequence,data_count,data_count_sum,arr_outliers)    
        # print(number_cnt)
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

        # print(class_belong)
        # print(len(class_belong))
        # print(data_sum)
        print(len(data_sum))
        print(len(data_count))
        # print(data_count)
        print("7777777777777777777")
        path = "/home/eilene/Downloads/"
        store_file(path,x1,y1,gm,data_count,None,data_count_sum,draw_input,None,arr_final,None)
    elif merge_switch:
        print("second, start reading total file with merge:\n")
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
        class_belong=[]
        data_count=[]
        data_sum=[]
        average_distance = []
        pre_merge_divide_class(final_filename,x1,gm,arr_final,data_sum,sequence,data_count,class_belong,average_distance)
        print("arr_final",arr_final)
        pre_merge_store_data(x1,arr_final,data_sum,sequence,data_count,class_belong,arr_outliers)
            # print(number_cnt)
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

        # print(class_belong)
        print(len(class_belong))
        # print(data_sum)
        print(len(data_sum))
        print(len(data_count))
        # print(data_count)
        print("7777777777777777777")

        # merge to the left
        data_count_new = []
        class_belong_new = []
        merge(data_sum,gm,data_count,class_belong,data_count_new,class_belong_new)
        print("88888888888888888888888")
        # print(data_count)
        print(len(data_count))
        # print(class_belong)
        print(len(class_belong))
        print("*******************")
        # print(data_count_new)
        print(len(data_count_new))
        # print(class_belong_new)
        print(len(class_belong_new))
        print("8888888888888888888888")
        data_count_sum = []   
        final_data = []
        arr_final_draw = []
        merge_store_data(data_count_new,data_count_sum,class_belong_new,final_data,arr_final,arr_final_draw)
        # print(arr_final_2)
        print("arr_final",arr_final)
        print("arr_final_draw",arr_final_draw)
        print("final_data",final_data)
        print(len(arr_final_draw))
        path = "/home/eilene/Downloads/"
        store_file(path,x1,y1,gm,data_count_new,class_belong_new,data_count_sum,draw_input,final_data,arr_final,arr_final_draw)