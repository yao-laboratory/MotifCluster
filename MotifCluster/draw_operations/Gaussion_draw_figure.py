# import math
# import threading
# import time
# import gc
import matplotlib as mpl
# import pybedtools
import os
# import warnings
# import copy
# import csv,re
# import sys
from collections import namedtuple
from draw_operations.Gaussion_draw_function import *
from file_operations.Gaussion_files_operation import *

# from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
# from pybedtools import BedTool

MAXIMUM_DISTANCE = 1000
SINGLE_POINT = -5

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

def draw(input_csv, input_bed, start_axis, end_axis,method, step1_folder, output_folder):
    if method== 1:
        print("MotifCluster: with peak intensity, with cluster merge (method d)")
    elif method == 2:  
        print("direct DBSCAN without groups (method a)")
    elif method == 3:  
        print("No peak intensity, no cluster merge (method b1)")
    elif method == 4:  
        print("No peak intensity, with cluster merge (method b2)")
    elif method == 5:  
        print("with peak intensity, no cluster merge (method c)")
    # reload GMM Model
    package_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print(package_path)
    middle_results_path = package_path + "/" + step1_folder + "/tmp_output/"
    output_path = package_path + "/" + output_folder + "/"
    if not os.path.exists(middle_results_path):
        os.makedirs(middle_results_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    bed_filename =  os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/input_files/" + input_bed
    print("first, start reading total file:\n")
    tmp = []
    tmp = find_left_right_axis(bed_filename)
    to_left = tmp[0]
    to_right = tmp[1] 
    means = np.load(middle_results_path + 'GMM_means.npy')
    covar = np.load(middle_results_path + 'GMM_covariances.npy')
    loaded_gm = GaussianMixture(n_components = len(means), covariance_type='full')
    loaded_gm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(covar))
    loaded_gm.weights_ = np.load(middle_results_path + 'GMM_weights.npy')
    loaded_gm.means_ = means
    loaded_gm.covariances_ = covar
    global_cluster_num = len(loaded_gm.means_)
    print("global_cluster_num", global_cluster_num)
    
    line_temp=[]
    final_filename = os.path.join(package_path + "/" + step1_folder, input_csv)
    data_axis = []
    data_weight = []
    arr_final = []
    arr_final_draw=[]
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
            row=tuple(convert(value) for convert,value in zip(col_types_csv1,row))
            data_axis.append((row[1])) 
            data_weight.append(row[2])
            for cnt_temp2 in range(0, global_cluster_num):
                draw_input[cnt_temp2].append(row[cnt_temp2 + 3])
            if method !=2: 
                arr_final.append(row[global_cluster_num + 3])
            if method == 1 or method == 4:
                arr_final_draw.append(row[global_cluster_num + 4])
            id += 1

    X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
    value_total = []

    Fig,Axes=plt.subplots(global_cluster_num+2,1,sharex='col',sharey='row')

    # drawing 
    label_space=[]
    # label_drawing=[]
    i0 = 0
    while(i0 < int(len(data_axis))):
        if (data_axis[i0] - to_left) >= int(start_axis) and (data_axis[i0] + to_right) <= int(end_axis):
            label_space.append(i0)
        if (data_axis[i0] + to_right) > int(end_axis):
            break
        i0 += 1

    x1 = data_axis[label_space[0]:label_space[-1] + 1]
    y1 = data_weight[label_space[0]:label_space[-1] + 1]
    # print(x1)
    # print(draw_input)
    # print(label_space[0])
    # print(label_space[-1] + 1)
    # print(draw_input[0][label_space[0]:label_space[-1] + 1])

    # print(label_space[0])
    # print(label_space[-1] + 1)
    # print(loaded_gm.means_)
    for i in range(0, len(loaded_gm.means_)):
        avg_show = str(loaded_gm.means_[i])
        draw_input_temp = draw_input[i][label_space[0]:label_space[-1] + 1]
        # print(draw_input_temp)
        draw_figure(draw_input_temp, avg_show, i, x1, y1, Axes)
    print("second step:\n")
    arr_1 = arr_final[label_space[0]:label_space[-1] + 1]
    # print(arr_1)
    # print(len(arr_1))
    draw_figure(arr_1,"final",global_cluster_num, x1, y1, Axes)  
    print("third step:\n")
    arr_2 = arr_final_draw[label_space[0]:label_space[-1] + 1]
    # print(arr_2)
    # print(len(arr_2))
    draw_figure(arr_2,"final_2",global_cluster_num+1, x1, y1, Axes)
    for i in range(global_cluster_num+2):
        Axes[i].set_aspect(30)
        plt.setp(Axes[global_cluster_num+1], xlabel='')
        plt.setp(Axes[global_cluster_num+1], ylabel='')

    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    plt.ylim(0, 10) 
    path = os.path.join(output_path, 'draw_figure.pdf')
    plt.savefig(path, bbox_inches='tight')
    plt.show()



    
    
    
        

        
   

   