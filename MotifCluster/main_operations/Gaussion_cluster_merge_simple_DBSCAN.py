from email.headerregistry import Group
import threading
import time
import gc
from xml.dom.minidom import Identified
import matplotlib.pyplot as plt
import pybedtools
import warnings
import operator
import copy
import sys
from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool

from file_operations.Gaussion_files_operation import *
from main_operations.Gaussion_cluster_merge import union_store_data,store_file

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

def sigma(data,avg):
    sigma_squ=np.sum(np.power((data-avg),2))/len(data)
    return np.power(sigma_squ,0.5)

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

def belong_which_cluster(distance, gm):
    maximum = 0
    cluster_id = SINGLE_POINT
    if distance == 0:
        return cluster_id
    # if distance > 500:
    #     return -1
    for i in range(len(gm.means_)):
        value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        if distance == None:
            print("value",value)  
        # print(value)
        if value > maximum:
            maximum = value
            cluster_id = i
    return cluster_id

#no need parameter id
def belong_which_cluster_better(cluster_0, cluster_1, id, distance, gm):
    temp_array = []
    if distance > 500:
        return -2
    for i in range(len(gm.means_)):
        # sentence = "{interval_id}\t{cluster_id}\t{log_odds}\n"
        p_value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        if p_value != 0 and p_value != 1:
            log_odd = math.log(p_value/(1-p_value))
            #idth distance
            temp_array.append([id, i, log_odd])
            # f.write(sentence.format(interval_id = id, cluster_id = i, log_odds = log_odd))
    
    temp_array.sort(key=lambda x:x[2], reverse = True)
    temp_cluster=[]
    if len(temp_array) > 0:
        #if the best log odd belong to cluster_0 or cluster_1
        if temp_array[0][1] == cluster_0 or temp_array[0][1] == cluster_1:
            return temp_array[0][1]
        for i in range(len(temp_array) - 1):
            if abs(temp_array[i][2]) * 1.5 >= abs(temp_array[i+1][2]):
                if temp_array[i+1][1] == cluster_0 or temp_array[i+1][1] == cluster_1:
                    return temp_array[i+1][1]
            else:
                break;
    return -2

def cluster_and_merge_simple_dbscan(input_file1, start_axis, end_axis,output_folder):
    line_temp = []
    draw_input = []
    package_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    middle_results_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/example_middle_output/"
    output_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/" + output_folder + "/"
    if not os.path.exists(middle_results_path):
        os.makedirs(middle_results_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    final_filename = package_path + "/input_files/" + input_file1
    print("first, start reading total file:\n")
    tmp = []
    tmp = find_left_right_axis(final_filename)
    to_left = tmp[0]
    to_right = tmp[1] 
    data_axis=[]
    weight=[]
    f = open(final_filename,"r")
    with f as lines:
        cluster_id = 0
        for line in lines:
            line = line.split("\t")
            data_axis.append(int(line[1]) + to_left)
            weight.append(10)
    f.close()
    data_weight = np.array(weight)

    data=np.array([(data_axis[i+1] - data_axis[i]) for i in range(len(data_axis)-1)])
    data_reshape = data.tolist()
    data_new_cal = []
    for val in data_reshape:
        if val <= 500:
            data_new_cal.append(val)
    

    ave=average(data_new_cal)
    sig=sigma(data_new_cal,ave)

    #GMM fitting
    X_DISTANCE = data.reshape(len(data), 1)
    x_distance_temp = []
    for value in X_DISTANCE:
        if value <= 500:
            x_distance_temp.append(value)
    X_DISTANCE = np.array(x_distance_temp)
    # Set up a range of cluster numbers to try
    n_range = range(1,11)

    gm = GaussianMixture(n_components = 1, n_init = 10, random_state = 100)
    gm.fit(X_DISTANCE)
    # print("Weights: ", gm.weights_)
    # print("\nMeans:\n", gm.means_)
    class_means_all = gm.means_
    # print("global_cluster_num", len(gm.means_))
    # print("\nCovariances:\n", gm.covariances_)
    # save GMM MODEL object
    np.save(middle_results_path + 'GMM_weights', gm.weights_, allow_pickle=False)
    np.save(middle_results_path + 'GMM_means', gm.means_, allow_pickle=False)
    np.save(middle_results_path + 'GMM_covariances', gm.covariances_, allow_pickle=False)

    X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
    value_total = []
    plt.figure("final")
    ax1 = plt.subplot(12,1,1)

    # drawing 
    label_space=[]
    i0 = 0
    if start_axis == "all" or end_axis =="all":
        while(i0 < int(len(data_axis))):
            label_space.append(i0)
            i0 += 1
    else:
        while(i0 < int(len(data_axis))):
            if (data_axis[i0] - to_left) >= int(start_axis) and (data_axis[i0] + to_right) <= int(end_axis):
                label_space.append(i0)
            if (data_axis[i0] + to_right) > int(end_axis):
                break
            i0 += 1

    x1 = data_axis[label_space[0]:label_space[-1] + 1]
    y1 = data_weight[label_space[0]:label_space[-1] + 1]

    gc.disable()
    print("ave",ave)
    db_temp = DBSCAN(eps = ave, min_samples = 8).fit(X_ORIGIN, y = None, sample_weight = data_weight)
    print("Gaussion mean:",gm.means_[0])
    print("Gaussion covariance:",math.sqrt(gm.covariances_[0]))
    print("Gaussion eps:",gm.means_[0]+ 2 * math.sqrt(gm.covariances_[0]))
    labels = db_temp.labels_
    label_values = []
    init_value = -2
    flag_current = init_value
    value = init_value
    for i in range(0,len(labels)):
        if i == len(labels) - 1:
            if labels[i] != -1:
                label_values += [i]
            else: 
                label_values += [value]
        if labels[i] == -1:
            continue
        if flag_current == init_value:
            label_values += [i]
            flag_current = labels[i]
        if flag_current != labels[i]:
            label_values += [value]
            label_values += [i]
            flag_current = labels[i]
        value = i
        
    #label value is like [0,3,4,4,6,9]
    value_total.append(label_values)
    
    label_drawing = labels[label_space[0]:label_space[-1]+1]
    # print("----------------")
    # print(label_drawing)
    # print(len(label_drawing))
    # print("----------------")
    draw_input.append(label_drawing)

    
    # create and open file
    for cnt in range(len(value_total)):
        final_filename =middle_results_path + "total_single_DBSCAN%d.bdg"%cnt
        f = open(final_filename,"w")

        # write data to file 
        i = 0
        while(i < len(value_total[cnt])):
            sentence = "chr12\t{start}\t{end}\t{num}\n"
            num_start = value_total[cnt][i]
            num_end = value_total[cnt][i+1]
            f.write(sentence.format(start = data_axis[num_start], end = data_axis[num_end] + 1,num = 1))
            i += 2
            
        # close file
        f.close() 
    cluster=[]  
    filenames = []

    print("second, start reading total file:\n")
    arr_final=[]
    arr_outliers=[]
    label_drawing_final=[]
    sequence=[]
    data_count=[]
    data_sum=[]
    data_count_sum=[]
    union_store_data(final_filename,x1,arr_final,data_sum,sequence,data_count,data_count_sum,arr_outliers)    

    #output csv file 
    output_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/" + output_folder + "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    store_file(output_path,x1,y1,None,data_count,None,data_count_sum,draw_input,None,arr_final,None,to_left,to_right)
    print("done.")




    
    
    
        

        
   

   