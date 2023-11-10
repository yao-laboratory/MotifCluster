import csv
import os
from collections import namedtuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'


def draw_rank(final_filename1, final_filename2, output_folder):
    package_path = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + '/input_files/'
    package_path2 = os.path.abspath(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))))
    print(package_path)
    final_f1 = os.path.join(package_path, final_filename1)
    final_f2 = os.path.join(package_path, final_filename2)
    output_path = package_path2 + "/" + output_folder + "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    group_axis_head1 = []
    group_axis_tail1 = []
    group_axis_head2 = []
    group_axis_tail2 = []
    with open(final_f1) as f1:
        f_csv = csv.reader(f1)
        headers = next(f_csv)
        Row = namedtuple('Row', headers)
        id = 0
        for r in f_csv:
            if id >= 100:
                break
            row = Row(*r)
            group_axis_head1.append(int(float(row[2])))
            group_axis_tail1.append(int(float(row[4])))
            id += 1
    with open(final_f2) as f2:
        f_csv = csv.reader(f2)
        headers = next(f_csv)
        Row = namedtuple('Row', headers)
        id = 0
        for r in f_csv:
            if id >= 100:
                break
            row = Row(*r)
            group_axis_head2.append(int(float(row[2])))
            group_axis_tail2.append(int(float(row[4])))
            id += 1

    print(len(group_axis_head2))
    x_axis = []
    y_axis = []
    flag = False
    for i in range(len(group_axis_head1)):
        for j in range(len(group_axis_head2)):
            temp_count = 0
            temp_place = group_axis_head2[j]
            while temp_place < group_axis_tail2[j]:
                if temp_place >= group_axis_head1[i] and temp_place <= group_axis_tail1[i]:
                    temp_count += 1
                temp_place += 1
            if temp_count >= (group_axis_tail1[i] - group_axis_head1[i])/10 and temp_count >= 1:
                x_axis.append(i+1)
                y_axis.append(j+1)
    for i in range(1, 101):
        if i not in x_axis:
            # print(i)
            x_axis.append(i)
            y_axis.append(101)
    for i in range(1, 101):
        if i not in y_axis:
            # print(i)
            y_axis.append(i)
            x_axis.append(101)
    # draw line
    x_line = np.arange(0, 102, 1)
    y_line = x_line
    fig = plt.figure(figsize=(10, 10))
    # split window to the one column, one row, pick the first part
    ax1 = fig.add_subplot(1, 1, 1)
    # set title
    ax1.set_title('rank')
    # set x-axis name
    ax1.set_xlabel('chr12 p value < 0.001')
    # set y-axis name
    ax1.set_ylabel('chr12 p value < 0.01')
    # draw plots
    for i in range(len(x_axis)):
        if x_axis[i] == 101 and y_axis[i] != 101:
            plt.scatter(x_axis[i], y_axis[i], color='darkblue', s=15)
        elif y_axis[i] == 101 and x_axis[i] != 101:
            plt.scatter(x_axis[i], y_axis[i], color='steelblue', s=15)
        else:
            plt.scatter(x_axis[i], y_axis[i], color='mediumorchid', s=15)

    # draw line
    ax1.plot(x_line, y_line, c='brown', ls='--')
    # adjust bundaries of x-axis
    plt.xlim(xmax=103, xmin=0)
    plt.ylim(ymax=103, ymin=0)
    # show
    path = os.path.join(output_path, 'normal_vs_noise_rank.pdf')
    plt.savefig(path, bbox_inches='tight')
    plt.show()


def draw_score_size(final_filename, output_folder):
    package_path = os.path.abspath(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))))
    print(package_path)
    final_f1 = os.path.join(package_path, final_filename)
    output_path = package_path + "/" + output_folder + "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    group_cluster_size = []
    group_score = []
    with open(final_f1) as f1:
        f_csv = csv.reader(f1)
        headers = next(f_csv)
        Row = namedtuple('Row', headers)
        id = 0
        for r in f_csv:
            if id >= 100:
                break
            row = Row(*r)
            group_cluster_size.append(int(row[5]))
            group_score.append(float(row[len(row) - 1]))
            id += 1
    x = np.arange(1, 101)
    y1 = group_score
    y2 = group_cluster_size
    x = np.arange(1, len(y1)+1)
    fig = plt.figure(figsize=[15, 6])

    ax1 = fig.add_subplot(111)
    fig1 = ax1.plot(x, y1, color="b", label="score")
    ax1.scatter(x, y1, color='b', s=18)
    ax1.spines['left'].set_color('b')
    ax1.spines['left'].set_linewidth(3)
    ax1.yaxis.label.set_color('b')
    ax1.set_ylim([0, int(max(group_score))+5])
    ax1.set_ylabel('Y values for score')
    # this is the important function
    ax2 = ax1.twinx()
    fig2 = ax2.plot(x, y2, color="r", label="cluster size")
    ax2.scatter(x, y2, color='r', s=18)
    ax2.spines['right'].set_color('r')
    ax2.spines['right'].set_linewidth(3)
    ax2.yaxis.label.set_color('r')
    ax2.set_ylim([0, int(max(group_cluster_size))+5])
    ax2.set_ylabel('Y values for cluster size')
    ax2.set_xlim([0, 101])
    ax2.grid(linestyle='--', alpha=0.5)

    ax1.set_xlabel('Same X for score rank id')
    legends = fig1 + fig2
    labels = [l.get_label() for l in legends]
    plt.legend(legends, labels, loc=(0.85, 0.85))
    path = os.path.join(output_path, 'score_size.pdf')
    plt.savefig(path, bbox_inches='tight')
    plt.show()
