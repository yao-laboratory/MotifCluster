import copy
import gc
import math
import os
import threading
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pybedtools
from file_operations.Gaussion_files_operation import *
from pybedtools import BedTool
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
# Suppress font warnings
import logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

MAXIMUM_DISTANCE = 1000
SINGLE_POINT = -5
STANDARD_WEIGHT = 10
MAXIMUM_TRIED_GROUP_NUMBER = 11
LONG_GAP_STANDARD = 500

# delete warning
warnings.filterwarnings("ignore")

# print every 10 minutes


def print_function():
    # print('Now:', time.strftime('%H:%M:%S',time.localtime()))
    t = threading.Timer(60*5, print_function)
    t.start()
    return t

# mean value


def average(data):
    return np.sum(data)/len(data)

# standard deviation


def sigma(data, avg):
    sigma_squ = np.sum(np.power((data-avg), 2))/len(data)
    return np.power(sigma_squ, 0.5)

# Gaussion Distribution


def prob(data, avg, sig):
    # print(data)
    sqrt_2pi = np.power(2*np.pi, 0.5)
    coef = 1/(sqrt_2pi*sig)
    powercoef = -1/(2*np.power(sig, 2))
    mypow = powercoef*(np.power((data-avg), 2))
    return coef*(np.exp(mypow))


def union_store_data(final_filename, x1, arr_final, data_sum, sequence, data_count, data_count_sum, arr_outliers):
    with open(final_filename, "r") as lines:
        cluster_id = 0
        flag = False
        for line in lines:
            line = line.split()
            data_temp = []
            for i in range(len(x1)):
                if int(x1[i]) > int(line[2]):
                    break
                elif int(x1[i]) >= int(line[1]) and int(x1[i]) <= int(line[2])-1:
                    data_temp.append(x1[i])
                    data_sum.append(x1[i])
                    arr_final.append(cluster_id)
                    sequence.append(i)
                    flag = True
            if flag == True:
                cluster_id += 1
            if len(data_temp) == 0:
                continue
            data_count.append(len(data_temp))

    for i in range(len(x1)):
        if i not in sequence:
            arr_final.insert(i, -1)
            arr_outliers.append(i)
            sequence.insert(i, i)
            data_sum.insert(i, x1[i])
    data_count_temp = copy.deepcopy(data_count)
    cnt = 0
    cnt_total = 0
    for j in range(len(data_count_temp)):
        cnt_total += data_count_temp[j]
    cnt_temp = 0
    for i in range(len(arr_final)):
        if arr_final[i] > -1:
            cnt += 1
        elif arr_final[i] == -1:
            if cnt == 0:
                data_count.insert(i, 1)
                cnt_temp += 1
            elif cnt > 0:
                if cnt == cnt_total:
                    data_count.append(1)
                else:
                    cnt_2 = 0
                    for j in range(len(data_count_temp)):
                        if data_count_temp[j] != -1:
                            cnt_2 += data_count_temp[j]
                        if cnt_2 == cnt:
                            data_count.insert(j + 1 + cnt_temp, 1)
                            cnt_temp += 1
    cnt = 0
    for j in range(len(data_count)):
        cnt += data_count[j]
        data_count_sum.append(cnt)


def belong_which_class(distance, gm):
    maximum = 0
    class_id = SINGLE_POINT
    if distance == 0 or distance > LONG_GAP_STANDARD:
        return class_id
    for i in range(len(gm.means_)):
        value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(
            distance - gm.means_[i], 2) / (2 * gm.covariances_[i]))
        if value > maximum:
            maximum = value
            class_id = i
    return class_id


def belong_which_class_better(class_0, class_1, id, distance, gm):
    temp_array = []
    if distance > LONG_GAP_STANDARD:
        return -2
    for i in range(len(gm.means_)):
        p_value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(
            distance - gm.means_[i], 2) / (2 * gm.covariances_[i]))
        if p_value != 0 and p_value != 1:
            log_odd = math.log(p_value/(1-p_value))
            # idth distance
            temp_array.append([id, i, log_odd])

    temp_array.sort(key=lambda x: x[2], reverse=True)
    if len(temp_array) > 0:
        # if the best log odd belong to class_0 or class_1
        if temp_array[0][1] == class_0 or temp_array[0][1] == class_1:
            return temp_array[0][1]
        for i in range(len(temp_array) - 1):
            if abs(temp_array[i][2]) * 1.5 >= abs(temp_array[i+1][2]):
                if temp_array[i+1][1] == class_0 or temp_array[i+1][1] == class_1:
                    return temp_array[i+1][1]
            else:
                break
    return -2

# pre merge to divide class


def pre_merge_divide_class(final_filename, x1, gm, arr_final, data_sum, sequence, data_count, class_belong, average_distance):
    with open(final_filename, "r") as lines:
        class_id = 0
        flag = False
        for line in lines:
            line = line.split()
            data_temp = []
            for i in range(len(x1)):
                if int(x1[i]) > int(line[2]):
                    break
                elif int(x1[i]) >= int(line[1]) and int(x1[i]) <= int(line[2])-1:
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
            data_distance_temp_ = np.array(
                [(int(data_temp[i+1]) - int(data_temp[i])) for i in range(len(data_temp)-1)])
            # calculate the Gaussion distribution's mean value according to the sample data
            ave_temp = 0 if len(data_distance_temp_) == 0 else average(
                data_distance_temp_)
            # one point counts how many distance and score
            ave_final = MAXIMUM_DISTANCE if len(
                data_distance_temp_) == 0 else average(data_distance_temp_)
            average_distance.append(ave_final)
            class_num = belong_which_class(ave_temp, gm)
            class_belong.append(class_num)
    # f.close()


def pre_merge_store_data(x1, arr_final, data_sum, sequence, data_count, class_belong, arr_outliers):
    # add_outliers
    for i in range(len(x1)):
        if i not in sequence:
            arr_final.insert(i, -1)
            arr_outliers.append(i)
            sequence.insert(i, i)
            data_sum.insert(i, x1[i])
    data_count_temp = copy.deepcopy(data_count)
    cnt = 0
    cnt_total = 0
    for j in range(len(data_count_temp)):
        cnt_total += data_count_temp[j]
    cnt_temp = 0
    for i in range(len(arr_final)):
        if arr_final[i] > -1:
            cnt += 1
        elif arr_final[i] == -1:
            if cnt == 0:
                data_count.insert(i, 1)
                class_belong.insert(i, -1)
                cnt_temp += 1
            elif cnt > 0:
                if cnt == cnt_total:
                    data_count.append(1)
                    class_belong.append(-1)
                else:
                    cnt_2 = 0
                    for j in range(len(data_count_temp)):
                        if data_count_temp[j] != -1:
                            cnt_2 += data_count_temp[j]
                        if cnt_2 == cnt:
                            data_count.insert(j + 1 + cnt_temp, 1)
                            class_belong.insert(j + 1 + cnt_temp, -1)
                            cnt_temp += 1

# merge to the left


def merge(data_sum, gm, data_count, class_belong, data_count_new, class_belong_new):
    sum_count = 0
    class_id = -3
    class_id_2 = -3
    i = 0
    while i <= len(data_count) - 1:
        sum_count = 0
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
        # bundary condition
        if (i+1) > (len(data_count) - 1):
            data_count_new.append(data_count_i)
            class_belong_new.append(class_belong_i)
            break
        elif (i+2) > (len(data_count) - 1):
            # not finished
            data_count_new.append(data_count_i)
            data_count_new.append(data_count[i+1])
            class_belong_new.append(class_belong_i)
            class_belong_new.append(class_belong[i+1])
            break
        else:
            distance = data_sum[sum_count] - data_sum[sum_count - 1]
            distance_2 = data_sum[sum_count + 1] - data_sum[sum_count]
            if data_count[i+1] > 1:
                if data_count_i > 1:
                    if class_belong_i == class_belong[i+1]:
                        class_id = belong_which_class_better(
                            class_belong_i, class_belong[i+1], i, distance, gm)
                        # check gap
                        if class_id == class_belong_i:
                            data_count_new.append(
                                data_count_i + data_count[i+1])
                            class_belong_new.append(class_belong_i)
                        else:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])
                            class_belong_new.append(class_belong_i)
                            class_belong_new.append(class_belong[i+1])

                    else:
                        # not merge
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])
                        class_belong_new.append(class_belong_i)
                        class_belong_new.append(class_belong[i+1])
                elif data_count_i == 1:
                    class_id = belong_which_class_better(
                        class_belong_i, class_belong[i+1], i, distance, gm)
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
                    class_id = belong_which_class_better(
                        class_belong_i, class_belong[i+1], i, distance, gm)
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
                    distance = data_sum[sum_count] - data_sum[sum_count - 1]
                    distance_2 = data_sum[sum_count + 1] - data_sum[sum_count]
                    class_id = belong_which_class_better(
                        class_belong_i, class_belong[i+1], i, distance, gm)
                    class_id_2 = belong_which_class_better(
                        class_belong[i+1], class_belong[i+2], i, distance_2, gm)
                    if class_belong_i != class_belong[i+2]:
                        if class_id == class_belong_i and class_id_2 == class_belong[i+2]:
                            # not finished
                            data_count_new.append(
                                data_count_i + data_count[i+1])
                            data_count_new.append(data_count[i+2])
                            class_belong_new.append(class_belong_i)
                            class_belong_new.append(class_belong[i+2])
                        else:
                            if class_id == class_belong_i:
                                data_count_new.append(
                                    data_count_i + data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                            if class_id_2 == class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(
                                    data_count[i+1] + data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                            elif class_id != class_belong_i and class_id_2 != class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+1])
                                class_belong_new.append(class_belong[i+2])
                    elif class_belong_i == class_belong[i+2]:
                        # merge together
                        if class_id == class_belong_i and class_id_2 == class_belong[i+2]:
                            # not finished
                            data_count_new.append(
                                data_count_i + data_count[i+1] + data_count[i+2])
                            class_belong_new.append(class_belong_i)
                        else:
                            if class_id == class_belong_i:
                                data_count_new.append(
                                    data_count_i + data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                            if class_id_2 == class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(
                                    data_count[i+1] + data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+2])
                            elif class_id != class_belong_i and class_id_2 != class_belong[i+2]:
                                data_count_new.append(data_count_i)
                                data_count_new.append(data_count[i+1])
                                data_count_new.append(data_count[i+2])
                                class_belong_new.append(class_belong_i)
                                class_belong_new.append(class_belong[i+1])
                                class_belong_new.append(class_belong[i+2])
                    i += 2

                elif data_count_i == 1:
                    if class_belong_i != -1 and class_belong[i+1] != -1:
                        class_id = belong_which_class(distance, gm)
                        if class_belong_i == class_belong[i+1]:
                            if class_id != SINGLE_POINT:
                                data_count_new.append(
                                    data_count_i + data_count[i+1])
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


def merge_store_data(data_count_new, data_count_sum, class_belong_new, final_data, arr_final, arr_final_draw):
    cnt = 0
    for j in range(len(data_count_new)):
        cnt += data_count_new[j]
        data_count_sum.append(cnt)

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

# output csv file


def store_file(path, x1, y1, gm, data_count_new, class_belong_new, data_count_sum, draw_input, final_data, arr_final, arr_final_draw, to_left, to_right):
    # output csv file
    if gm is None:
        res_dir = os.path.dirname(path)
        res_path = os.path.join(res_dir, 'result_simple_DBSCAN.csv')
        res_path2 = os.path.join(res_dir, 'result_middle_simple_DBSCAN.csv')
        res_path3 = os.path.join(res_dir, 'result_draw_simple_DBSCAN.csv')
        if os.path.exists(res_path):
            os.remove(res_path)
        if os.path.exists(res_path2):
            os.remove(res_path2)
        if os.path.exists(res_path3):
            os.remove(res_path3)
        write_result(res_path, x1, y1, final_data, to_left, to_right)
        write_middle_result(res_path2, data_count_new,
                            class_belong_new, data_count_sum)
        write_draw_input(res_path3, x1, y1, draw_input,
                         1, arr_final, arr_final_draw)
    elif class_belong_new is None:
        res_dir = os.path.dirname(path)
        res_path = os.path.join(res_dir, 'result_union.csv')
        res_path2 = os.path.join(res_dir, 'result_middle_union.csv')
        res_path3 = os.path.join(res_dir, 'result_draw_union.csv')
        if os.path.exists(res_path):
            os.remove(res_path)
        if os.path.exists(res_path2):
            os.remove(res_path2)
        if os.path.exists(res_path3):
            os.remove(res_path3)
        write_result(res_path, x1, y1, final_data, to_left, to_right)
        write_middle_result(res_path2, data_count_new,
                            class_belong_new, data_count_sum)
        write_draw_input(res_path3, x1, y1, draw_input, len(
            gm.means_), arr_final, arr_final_draw)
    else:
        res_dir = os.path.dirname(path)
        res_path = os.path.join(res_dir, 'result.csv')
        res_path2 = os.path.join(res_dir, 'result_middle.csv')
        res_path3 = os.path.join(res_dir, 'result_draw.csv')
        if os.path.exists(res_path):
            os.remove(res_path)
        if os.path.exists(res_path2):
            os.remove(res_path2)
        if os.path.exists(res_path3):
            os.remove(res_path3)
        write_result(res_path, x1, y1, final_data, to_left, to_right)
        write_middle_result(res_path2, data_count_new,
                            class_belong_new, data_count_sum)
        write_draw_input(res_path3, x1, y1, draw_input, len(
            gm.means_), arr_final, arr_final_draw)


def cluster_and_merge(input_file1, start_axis, end_axis, merge_switch, weight_switch, output_folder):
    if merge_switch == "on":
        merge_switch = True
        print("merge swith on")
    else:
        merge_switch = False
        print("merge switch off")
    if weight_switch == "on":
        weight_switch = True
        print("weight switch swith on")
    else:
        weight_switch = False
        print("weight switch off")
    line_temp = []
    draw_input = []
    package_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.abspath(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__)))) + "/" + output_folder + "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    middle_results_path = os.path.abspath(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__)))) + "/" + output_folder + "/tmp_output/"
    if not os.path.exists(middle_results_path):
        os.makedirs(middle_results_path)

    final_filename = package_path + "/input_files/" + input_file1
    print("first, start reading total file:\n")
    tmp = []
    tmp = find_left_right_axis(final_filename)
    to_left = tmp[0]
    to_right = tmp[1]
    data_axis = []
    weight = []
    chrome = ""
    f = open(final_filename, "r")
    with f as lines:
        class_id = 0
        for line in lines:
            line = line.split("\t")
            if "P-value=" not in str(line[7]):
                print("bed file format error, please compared with the example bed file in input_files!")
                exit()
            chrome = str(line[0]).strip()   
            p_value = float(str(line[7][8:]).strip())
            middle_axis = int(line[1]) + to_left
            data_axis.append(middle_axis)
            num = -math.log10(p_value)
            if weight_switch:
                weight.append(num)
            elif not weight_switch:
                weight.append(STANDARD_WEIGHT)

    f.close()
    data_weight = np.array(weight)
    data = np.array([(data_axis[i+1] - data_axis[i])
                    for i in range(len(data_axis)-1)])
    ave = average(data)
    #print(data_weight.min(), data_weight.max())
    # print("!!!ave:",ave)
    sig = sigma(data, ave)

    # GMM fitting
    X_DISTANCE = data.reshape(len(data), 1)
    x_distance_temp = []
    for value in X_DISTANCE:
        if value <= LONG_GAP_STANDARD:
            x_distance_temp.append(value)
    X_DISTANCE = np.array(x_distance_temp)
    # print(X_DISTANCE)
    # Set up a range of class numbers to try
    # original
    n_range = range(1, MAXIMUM_TRIED_GROUP_NUMBER)

    # Create empty lists to store the BIC and AIC values
    bic_score = []
    aic_score = []
    component_num = 1
    Difference_value = 1
    min_score = 0xffffffff
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
        if aic_score[i-1] < min_score:
            min_score = aic_score[i-1]
            global_class_num = i
    gm = GaussianMixture(n_components=global_class_num,
                         n_init=10, random_state=100)
    gm.fit(X_DISTANCE)
    # print("Weights: ", gm.weights_)
    # print("\nMeans:\n", gm.means_)
    class_means_all = gm.means_
    # print("\nCovariances:\n", gm.covariances_)

    # Drawing each line according to different mean values
    X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
    value_total = []
    plt.figure("final")
    ax1 = plt.subplot(global_class_num+2, 1, 1)

    # drawing
    label_space = []
    i0 = 0
    if start_axis == "all" or end_axis == "all":
        while (i0 < int(len(data_axis))):
            label_space.append(i0)
            i0 += 1
    else:
        while (i0 < int(len(data_axis))):
            if (data_axis[i0] - to_left) >= int(start_axis) and (data_axis[i0] + to_right) <= int(end_axis):
                label_space.append(i0)
            if (data_axis[i0] + to_right) > int(end_axis):
                break
            i0 += 1

    x1 = data_axis[label_space[0]:label_space[-1] + 1]
    y1 = data_weight[label_space[0]:label_space[-1] + 1]

    for i in range(0, len(gm.means_)):
        gc.disable()
        # ORIGINAL
        db_temp = DBSCAN(eps=gm.means_[i] + 2 * math.sqrt(gm.covariances_[i]),
                         min_samples=8).fit(X_ORIGIN, y=None, sample_weight=data_weight)
        labels = db_temp.labels_
        avg_show = str(gm.means_[i])
        label_values = []
        init_value = -2
        flag_current = init_value
        value = init_value
        cnt = i
        for i in range(0, len(labels)):
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

        # label value is like [0,3,4,4,6,9]
        value_total.append(label_values)

        label_drawing = labels[label_space[0]:label_space[-1]+1]
        draw_input.append(label_drawing)

    # save GMM MODEL object
    np.save(middle_results_path + 'GMM_weights',
            gm.weights_, allow_pickle=False)
    np.save(middle_results_path + 'GMM_means', gm.means_, allow_pickle=False)
    np.save(middle_results_path + 'GMM_covariances',
            gm.covariances_, allow_pickle=False)
    # create and open file
    for cnt in range(len(value_total)):
        filename = middle_results_path + "class%d.bdg" % cnt
        f = open(filename, "w")
        # write data to file
        i = 0
        # f.write("genename start end")
        while (i < len(value_total[cnt])):
            sentence = "{chrome}\t{start}\t{end}\t{num}\n"
            num_start = value_total[cnt][i]
            num_end = value_total[cnt][i+1]
            f.write(sentence.format(chrome=chrome,
                start=data_axis[num_start], end=data_axis[num_end] + 1, num=1))
            # f.write(sentence.format(
            #     start=data_axis[num_start], end=data_axis[num_end] + 1, num=1))
            i += 2

        f.close()
    classes = []
    filenames = []
    for cnt in range(len(value_total)):
        filename = middle_results_path + "class%d.bdg" % cnt
        classes.append(pybedtools.example_bedtool(filename))
        filenames.append(filename)
    final_filename = middle_results_path + "total.bdg"
    BedTool().union_bedgraphs(i=filenames, output=final_filename)

    if not merge_switch:
        print("second, start reading total file with not merge:\n")
        arr_final = []
        arr_outliers = []
        sequence = []
        data_count = []
        data_sum = []
        data_count_sum = []
        union_store_data(final_filename, x1, arr_final, data_sum,
                         sequence, data_count, data_count_sum, arr_outliers)
        store_file(output_path, x1, y1, gm, data_count, None, data_count_sum,
                   draw_input, None, arr_final, None, to_left, to_right)
    elif merge_switch:
        print("second, start reading total file with merge:\n")
        arr_final = []
        arr_outliers = []
        label_drawing_final = []
        sequence = []
        class_belong = []
        data_count = []
        data_sum = []
        average_distance = []
        pre_merge_divide_class(final_filename, x1, gm, arr_final, data_sum,
                               sequence, data_count, class_belong, average_distance)
        pre_merge_store_data(x1, arr_final, data_sum,
                             sequence, data_count, class_belong, arr_outliers)

        # merge to the left
        data_count_new = []
        class_belong_new = []
        merge(data_sum, gm, data_count, class_belong,
              data_count_new, class_belong_new)
        data_count_sum = []
        final_data = []
        arr_final_draw = []
        merge_store_data(data_count_new, data_count_sum,
                         class_belong_new, final_data, arr_final, arr_final_draw)
        store_file(output_path, x1, y1, gm, data_count_new, class_belong_new, data_count_sum,
                   draw_input, final_data, arr_final, arr_final_draw, to_left, to_right)
    print("done.")
