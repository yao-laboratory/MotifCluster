# from tkinter import Y
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import operator
import csv
import pandas as pd

# global_cluster_num = 10

def draw_cluster_weight(input_file):
    final_filename = "/home/eilene/Downloads/" + input_file
    df = pd.read_csv(final_filename)
    cluster_num = int((len(df.columns) - 1)/2)
    print(cluster_num)
    cluster_weight_length = []
    s= df.iloc[0,cluster_num+1:cluster_num * 2+1]
    s = s.fillna('0').astype('int32' , errors='ignore' )
    cluster_weight_length = s.tolist()
    # print(cluster_weight_length)
    data_weight_cluster = [[] for i in range(cluster_num)]
    for i in range(0, cluster_num):
        data_weight_cluster[i] = df.iloc[:,i+1][0:cluster_weight_length[i]].tolist()
        # data_weight_cluster[i] = df.iloc[: i][0:1]
    # Implementation of matplotlib function
    # y1 = np.arange(1,1001) #1000个客户排名
    plt.figure(figsize=(36,10)) #创建幕布
    # bins = np.arange(0,11,1)
    # plt.xlim(0,10)
    # print(data_weight_cluster[4])
    # print(global_cluster_num)
    cnt = int(cluster_num /2)
    for i in range(0, cluster_num):
        y_temp = data_weight_cluster[i]
        if i < cnt:
            ax = plt.subplot(2,cnt,i+1) #截取幕布的一部分，121是简写，表示1行2列中的第1个图
            # bins = np.arange(0,11,1)
            ns,edgeBin,patches = plt.hist(y_temp, bins = 10, rwidth=0.8)
            # ax1.xaxis.set_tick_params(rotation=45) 
            # ax1.xaxis.set_ticks(np.arange(0,cluster_num,1))
            # ax1.xaxis.set_tick_params(rotation=45,labelsize=18,colors='w') 
            # start, end = ax1.get_xlim() 
            # ax1.xaxis.set_ticks(np.arange(start, end,1)) 
            # ax1.yaxis.tick_right()
            
        else:
            ax = plt.subplot(2,cnt,i+1)
            ns,edgeBin,patches = plt.hist(y_temp,bins=10,rwidth=0.8)
            # plt.xticks(rotation = 45)
        ax.xaxis.set_tick_params(rotation=45) 
        ax.xaxis.set_ticks(np.arange(0,cluster_num,1)) 
            # ax2.xaxis.set_tick_params(rotation=45,labelsize=18,colors='w') 
            # start, end = ax2.get_xlim() 
            # ax2.xaxis.set_ticks(np.arange(start, end,1)) 
            # ax2.yaxis.tick_right()
        # plt.xlim(0,10)
        # plt.title('新增客户排名分布')
    plt.subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    # plt.xticks(np.arange(0,cluster_num,1),rotation = 45)
    plt.show()