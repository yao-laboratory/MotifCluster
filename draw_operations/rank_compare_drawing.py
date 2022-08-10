import numpy as np
import matplotlib.pyplot as plt
import math
import csv,re
from collections import namedtuple

def draw_rank(final_filename1, final_filename2):
    group_axis_head1 = []
    group_axis_tail1 = []
    group_axis_head2 = []
    group_axis_tail2 = []
    with open(final_filename1) as f1:
        f_csv=csv.reader(f1)
        headers=next(f_csv)
        Row=namedtuple('Row',headers)
        id = 0
        for r in f_csv:
            if id >= 100:
                break
            row=Row(*r)
            group_axis_head1.append(int(row[2]))
            group_axis_tail1.append(int(row[4]))
            id += 1
    with open(final_filename2) as f2:
        f_csv=csv.reader(f2)
        headers=next(f_csv)
        Row=namedtuple('Row',headers)
        id = 0
        for r in f_csv:
            if id >= 100:
                 break
            row=Row(*r)
            group_axis_head2.append(int(row[2]))
            group_axis_tail2.append(int(row[4]))
            id += 1

    print(len(group_axis_head2))
    x_axis = []
    y_axis = []
    flag = False
    for i in range(len(group_axis_head1)):
        for j in range(len(group_axis_head2)):
            # if group_axis_head2[j] > group_axis_tail1[i]:
            #     break
            temp_count = 0
            temp_place = group_axis_head2[j]
            while temp_place < group_axis_tail2[j]:
                if temp_place >= group_axis_head1[i] and temp_place <= group_axis_tail1[i]:
                    temp_count += 1   
                temp_place += 1
            if temp_count >= (group_axis_tail1[i] - group_axis_head1[i])/10 and temp_count >=1:
                x_axis.append(i+1)
                y_axis.append(j+1)
    for i in range(1,101):
        if i not in x_axis:
            print(i)
            x_axis.append(i)
            y_axis.append(101)
            # else:
            #     x_axis.append(i+1)
            #     y_axis.append(101)
    # draw line
    x_line =np.arange(0,102,1)
    y_line = x_line            
    fig = plt.figure()
    # 将画图窗口分成1行1列，选择第一块区域作子图
    ax1 = fig.add_subplot(1, 1, 1)
    # 设置标题
    ax1.set_title('rank')
    # 设置横坐标名称
    ax1.set_xlabel('chr12 p value < 0.001')
    # 设置纵坐标名称
    ax1.set_ylabel('chr12 p value < 0.01')
    # 画散点图
    plt.scatter(x_axis, y_axis, color='b')
    plt.scatter(x_axis, y_axis, marker='o', edgecolors='g', s=20)
    # draw line
    ax1.plot(x_line, y_line, c='b', ls='--')
    # 调整横坐标的上下界
    plt.xlim(xmax = 101, xmin = 0)
    plt.ylim(ymax = 102, ymin = 0)
    # 显示
    plt.show()
 
 

                