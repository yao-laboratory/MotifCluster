import math
import threading
import time
import gc
from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
import pybedtools
import os
import warnings
import operator
from scipy import stats
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from pybedtools import BedTool

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

def getSample(cluster_num,cluster_distance,sample_total_num):
    sample_list=[]
    initial_num = 0
    for i in range(cluster_num):
        sample_num = sample_total_num / cluster_num
        data_range = cluster_distance[i] * sample_num
        sample = [round(initial_num + x * cluster_distance[i],2)for x in range(int(sample_num))]
        sample_list += sample
        initial_num += data_range
        # print("sample_list:")
        # print(sample_list)
    return sample_list

# extend x axis
def extend_xplot(x, y, x_maxsize, id):
    # plt.figure()
    # plt.plot(x, y)
    #plt.ylim((0, 1000))
    # plt.title("clusters radius: "+ id)
    plt.xlabel("X")
    plt.ylabel("Y")
    
    # change x internal size
    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    
    # set size
    # maxsize = x_maxsize
    m = 0.2
    N =len(x)
    s = x_maxsize / plt.gcf().dpi * N + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]
    
    # plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

    # plt.savefig("%s%s.jpg"%(save_path, "Demo"), bbox_inches='tight')
    # plt.close()

# 设置渐变色
def set_clusters_outlier_color(labels):
    group_color = []
    for la in labels:
        if la == -1:
            group_color.append('#000000')
    return group_color
    
def set_clusters_normal_color(labels):
    color_num = max(labels) + 1
    # print(color_num)
    clrs = []
    for i in np.linspace(16711680,255,color_num):
        c = int(i)
        clrs.append('#%06x'%c)
        # print(clrs)
    
    use_colours = list(enumerate(clrs))
    # use_colours = [(-1,"#000000")]
    # use_colours.append(other_colors)
    # print(use_colours)
    group_color = []
    for la in labels:
        if la != -1:
            b1 = operator.itemgetter(la)
            group_color.append(b1(use_colours)[1])
    return group_color
    # print(group_color) 
 
def draw_figure(data,id,num):
    group_color = []
    group_color_outlier = set_clusters_outlier_color(data)
    group_color_normal = set_clusters_normal_color(data)
    extend_xplot(x1, y1, 200, id)
    x_outlier = []
    y_outlier = []
    x_normal = []
    y_normal = []
    for li in range(len(data)):
        # print("&&&&&&&&&&&&&&&&&&&&")
        if data[li] == -1:
            # print("x1 outlier:")
            # print(li,x1[li])
            x_outlier.append(x1[li])
            y_outlier.append(y1[li])
        else:
            # print("nomal x1:")
            # print(li,x1[li])
            x_normal.append(x1[li])
            y_normal.append(y1[li])
    # linestyle='--'
    # print("outliers:")
    # print(x_outlier,y_outlier)
    # print("normal:")
    # print(x_normal, y_normal)
   
    if num > 1:
        axn = plt.subplot(12,1,num,sharex=ax1, sharey=ax1)
    plt.sca(plt.subplot(12,1,num))
    plt.vlines(x_outlier, 0, y_outlier, colors=group_color_outlier, linestyles='--', label='', data=None) 
    plt.vlines(x_normal, 0, y_normal, colors=group_color_normal, linestyles='solid', label='', data=None) 
    if num == 1:
        plt.setp(ax1.get_xticklabels(), fontsize=6)
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    # plt.tight_layout()
    # # plt.scatter(x1, y1, s=area, c=group_color, alpha=0.4, label='mean1')
    # # plt.legend()
    # # plt.savefig(r'E:\second semester\bioinformatics\notes\1.png', dpi=300)   
    # plt.show()

def set_outliers(filename, arr_final):
    arr_temp=[]
    with open(final_filename,"r") as lines:
        for line in lines:
            line = line.split()
            # print(line)
            count = 0
            for i in range(len(line) - 3):
                count += int(line[-1-i])
            # print(count)     
            if(count >= 1):
                cnt = len(arr_temp)-1
                if(cnt < 0):
                    arr_temp.append(line[1])
                elif arr_temp[cnt] == line[1]:
                    arr_temp.pop()
                else:
                    arr_temp.append(line[1])
                arr_temp.append(line[2])
        # for i in range(len(arr_temp) - 2):
        # print(arr_temp)
        i = 0
        while i < (len(arr_temp) - 2):
            # print(arr_temp[i+2])
            # print(arr_temp[i+1])
            # temp_i = i
            interval = int(arr_temp[i+2]) - int(arr_temp[i+1])
            if (interval > 1):
                for cnt in range(interval - 1):
                    # print(arr_temp[i+1])
                    arr_final.insert(int(arr_temp[i+1]) + 1, -1)
            i += 2
        if (int(arr_temp[len(arr_temp) -1]) < (len(data_axis) - 1)):
            for cnt in range(len(data_axis)-1-arr_temp[len(arr_temp)-1]):
                arr_final.insert(int(arr_temp[len(arr_temp)] + 1),-1)
    f.close()
    
def belong_which_cluster(distance, gm):
    maximum = 0
    cluster_id = -1
    for i in range(len(gm.means_)):
        value = (1 / math.sqrt(2 * math.pi * gm.covariances_[i])) * math.exp(-math.pow(distance - gm.means_[i],2) / (2 * gm.covariances_[i]))
        # print("p:")
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
    
            
        

#样本数据
# cluster_num = 4
# cluster_distance = [1,5,20,100]
# data_axis = getSample(cluster_num,cluster_distance,200)
# print(data_axis)
MINIMUM_VALUE = math.pow(10,-20)
MAXIMUM_DISTANCE = 1000
line_temp=[]
final_filename = "/home/eilene/Downloads/total_chr12.bed"
print("start reading total file:\n")
data_axis=[]
weight=[]
f = open(final_filename,"r")
with f as lines:
    cluster_id = 0
    for line in lines:
        line = line.split()
        # print(line)
        data_axis.append(int(line[1])+ 8)
        # data_axis.append(int(line[2]))
        raw_weight = ''.join(line[7][8:])
        mark_1 = raw_weight.rfind('e')
        mark_2 = raw_weight.rfind('-')
        num_part1 = float(raw_weight[0:mark_1])
        num_part2 = -int(raw_weight[mark_2 + 1:])
        num = -math.log10(num_part1 * math.pow(10,num_part2))
        weight.append(round(num,4))

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
global_cluster_num = 0
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
        global_cluster_num = i
# print("global_cluster_num num:")
# print(global_cluster_num)
gm = GaussianMixture(n_components = global_cluster_num, n_init = 10, random_state = 100)
gm.fit(X_DISTANCE)
# don't delete
# print("Weights: ", gm.weights_)
# print("\nMeans:\n", gm.means_)
cluster_means_all = gm.means_
# print("\nCovariances:\n", gm.covariances_)
# cluster_covariances_all = gm.covariances_

# don't delete
# print("\nCovariances:\n", gm.covariances_)

#画散点图
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
#matplotlib画图中中文显示会有问题，需要这两行设置默认字体
 
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.xlim(xmax=max(data_axis),xmin=0)
# plt.ylim(ymax=11,ymin=0)
#画两条（0-xmax,0-ymax）的坐标轴并设置轴标签x，y
 
x1 = data_axis
y1 = data_weight


# area = np.pi * 2**2  # 点面积 
# 画散点图

#三种mean值的DBSCAN聚类情况画图
X_ORIGIN = np.array(data_axis).reshape(len(data_axis), 1)
value_total = []
plt.figure("final")
ax1 = plt.subplot(12,1,1)
# ax2 = plt.subplot(512)
# ax3 = plt.subplot(513)
# ax4 = plt.subplot(514)
# ax5 = plt.subplot(515)
for i in range(0, len(gm.means_)):
    # print("iiiiiiiiii")
    # print(i,len(gm.means_))
    gc.disable()
    db_temp = DBSCAN(eps = gm.means_[i] + 2 * math.sqrt(gm.covariances_[i]), min_samples = 8).fit(X_ORIGIN, y = None, sample_weight=data_weight)
    # gc.enable()
    # print("fffffffffffffff")
    labels = db_temp.labels_
    avg_show = str(gm.means_[i])
    # print("means_"+str(i)+":\n"+str(gm.means_[i]))
    # print("labels_"+str(i)+":\n"+str(labels))
    label_values = []
    init_value = -2
    flag_current = init_value
    value = init_value
    cnt = i
    # print("labels num:")
    # print(len(labels))
    for i in range(0,len(labels)):
        # print("i:",i)
        # print("labels[i]:",labels[i]) 
        # print("len(labels) - 1",len(labels) - 1)
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
            # print("value:",value)
            # print("i:",i)
        value = i
    # print("label_values num:")
    # print(len(label_values))
    # print(label_values)
    #label value is like [0,3,4,4,6,9]
    value_total.append(label_values)
    
    # # del sample_weight
    # gc.collect
    label_space=[]
    label_drawing=[]
    i0 = 0
    while(i0 < len(label_values)):
        if (data_axis[label_values[i0]] - 8) >= 6710000 and (data_axis[label_values[i0]] + 8 + 1) <= 6724000:
            label_space.append(i0)
            # print("************************")
            # print(i0)
        if (data_axis[label_values[i0]] + 8 + 1) > 6724000:
            break;
        i0 += 1
    # print(label_values[label_space[0]],label_values[label_space[-1]])
    label_drawing = labels[label_values[label_space[0]]:label_values[label_space[-1]]+1]
    # print("----------------")
    # print(label_drawing)
    # print(len(label_drawing))
    # print("----------------")
    x1 = data_axis[label_values[label_space[0]]:label_values[label_space[-1]]+1]
    y1 = data_weight[label_values[label_space[0]]:label_values[label_space[-1]]+1]
    # print(x1,y1)
    # print(len(value_total))
    draw_figure(label_drawing, avg_show, cnt+1)

plt.tight_layout()   
# plt.show()

# create and open file
# print(len(value_total))
for cnt in range(len(value_total)):
    # cnt_temp = cnt+1
    filename ="/home/eilene/Downloads/cluster%d.bdg"%cnt
    f = open(filename,"w")

    # write data to file 
    i = 0
    # f.write("genename start end")
    while(i < len(value_total[cnt])):
        sentence = "chr12\t{start}\t{end}\t{num}\n"
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
for cnt in range(len(value_total)):
    # cnt_temp = cnt+1
    filename ="/home/eilene/Downloads/cluster%d.bdg"%cnt
    cluster.append(pybedtools.example_bedtool(filename))
    # print("cluster_"+str(cnt)+":\n")
    cluster[cnt].head()
    filenames.append(filename)
    # print("------------------------------------")
    # print(filenames)
final_filename = "/home/eilene/Downloads/total.bdg"
BedTool().union_bedgraphs(i=filenames, output=final_filename)

# cmd = "bedtools unionbedg -i "  + filenames +"-output " + final_filename
# print(cmd)
# output = os.system(cmd)

print("start reading total file:\n")
arr_final=[]
arr_outliers=[]
data_axis_final_show=[]
label_drawing_final=[]
number_cnt=[]
sequence=[]
for i in range(len(data_axis)):
    if data_axis[i] >= 6717000 and data_axis[i] <= 6724000:
        data_axis_final_show.append(int(data_axis[i]))
        number_cnt.append(i)

with open(final_filename,"r") as lines:
    cluster_id = 0
    flag = False
    for line in lines:
        line = line.split()
        # print(line)
        for i in range(len(data_axis_final_show)):
            if int(data_axis_final_show[i]) >= int(line[1]) and int(data_axis_final_show[i]) <= int(line[2])-1:
                # if((len(arr_final) - 1) == i):
                #     continue
                arr_final.append(cluster_id)
                sequence.append(i)
                flag = True
        if flag == True:
            cluster_id += 1
f.close()
# set_outliers(final_filename,arr_final)

# print(arr_temp)
x1 = data_axis[number_cnt[0]:number_cnt[-1]+1]
y1 = data_weight[number_cnt[0]:number_cnt[-1]+1]
# print(sequence)
for i in range(len(arr_final)):
    if sequence[i]!= i:
        arr_final.insert(i,-1)
        arr_outliers.append(i)
        sequence.insert(i,i)

# print(number_cnt)
print("*******************************************")
print(arr_final)
print(len(arr_final))
print(arr_outliers)
print(len(arr_outliers))
print(x1)
print(len(x1))
draw_figure(arr_final,"final",11)  
# plt.tight_layout()    
# plt.show()

print("start reading total file again:\n")
arr_final=[]
cluster_belong=[]
data_count=[]
data_sum=[]
weight_sum=[]
x_temp = x1
y_temp = y1
average_distance = []
with open(final_filename,"r") as lines:
    cluster_id = 0
    for line in lines:
        line = line.split()
        # print(line)
        data_temp=[]
        for i in range(len(x_temp)):
            if (x_temp[i] >= int(line[1]) and x_temp[i] < int(line[2])):
                # print("aaaaaaaaaaa")
                # print(x_temp[i])
                # print(int(line[1]))
                # print(int(line[2]))
                # print("aaaaaaaaaaa")
                data_temp.append(x_temp[i])
                weight_sum.append(y_temp[i])
                data_sum.append(x_temp[i])

        if len(data_temp) == 0:
            continue
        data_count.append(len(data_temp))
        # print(len(data_temp))
        # print(data_temp)
        data_distance_temp_=np.array([(int(data_temp[i+1]) - int(data_temp[i])) for i in range(len(data_temp)-1)])
        # print("data=",data_distance_temp_)
        #根据样本数据求高斯分布的平均数
        ave_temp = average(data_distance_temp_)
        # one point counts how many distance and score
        ave_final = MAXIMUM_DISTANCE if len(data_distance_temp_) == 0 else average(data_distance_temp_)
        average_distance.append(round(ave_final,4))
        # print(data_distance_temp_)
        # print("ave=",ave_temp)
        # print("ave_final=",ave_final)
        cluster_num = belong_which_cluster(ave_temp, gm)
        cluster_belong.append(cluster_num)         
f.close()
data_count_temp = data_count
# cnt = 0
for i in arr_outliers:
    cnt = 0 
    for j in range(len(data_count)):
        cnt += data_count[j]
        # print(j)
        # print(cnt)
        if cnt == i: 
            # print("6666666666666666666") 
            # print(i)
            # print(j)
            cluster_belong.insert(j+1, -1)
            data_count.insert(j+1, 1)
            # print(cluster_belong)
            # print(data_count)
            break
    data_sum.insert(i,x_temp[i])

print(cluster_belong)
print(data_sum)
print(len(data_sum))
print("7777777777777777777")
print(data_count)


# merge to the left
sum_count = 0
data_count_new = []
cluster_belong_new = []
set_value = False
cluster_id = -3
cluster_id_2 = -3
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
        cluster_belong_i = cluster_belong[i]
    elif i != 0:
        data_count_i = data_count_new.pop()
        cluster_belong_i = cluster_belong_new.pop()
    #bundary condition
    if (i+1) > (len(data_count) - 1):
        data_count_new.append(data_count_i)
        cluster_belong_new.append(cluster_belong_i)
        break
    elif (i+2) > (len(data_count) - 1):
        #not finished
        data_count_new.append(data_count_i)
        data_count_new.append(data_count[i+1])
        cluster_belong_new.append(cluster_belong_i)
        cluster_belong_new.append(cluster_belong[i+1])
        break
    else:
        distance = data_sum[sum_count] - data_sum[sum_count - 1]
        distance_2 = data_sum[sum_count + 1] - data_sum[sum_count]
        if data_count[i+1] > 1 :
            if data_count_i > 1:
                if cluster_belong_i == cluster_belong[i+1]:
                    cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                    # print("1111111111111111111")
                    # print(cluster_id)
                    #check gap
                    if cluster_id == cluster_belong_i:
                        data_count_new.append(data_count_i + data_count[i+1])
                        cluster_belong_new.append(cluster_belong_i)
                    else:
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])  
                        cluster_belong_new.append(cluster_belong_i)
                        cluster_belong_new.append(cluster_belong[i+1])

                else:
                    #not merge
                    data_count_new.append(data_count_i)
                    data_count_new.append(data_count[i+1])  
                    cluster_belong_new.append(cluster_belong_i)
                    cluster_belong_new.append(cluster_belong[i+1])
            elif data_count_i == 1:
                cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                # print("22222222")
                # print(cluster_id)
                if cluster_id == cluster_belong[i+1]:
                    data_count_new.append(data_count_i + data_count[i+1])
                    cluster_belong_new.append(cluster_belong[i+1])
                else:
                    data_count_new.append(data_count_i)
                    data_count_new.append(data_count[i+1])  
                    cluster_belong_new.append(cluster_belong_i)
                    cluster_belong_new.append(cluster_belong[i+1]) 
            i += 1   
        elif data_count[i+1] == 1:
            if data_count_i > 1 and data_count[i+2] == 1:
                cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                # print("33333333")
                # print(cluster_id)
                if cluster_id == cluster_belong_i:
                    data_count_new.append(data_count_i + data_count[i+1])
                    cluster_belong_new.append(cluster_belong_i)
                else:
                    data_count_new.append(data_count_i)
                    data_count_new.append(data_count[i+1])  
                    cluster_belong_new.append(cluster_belong_i)
                    cluster_belong_new.append(cluster_belong[i+1]) 
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
                cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                cluster_id_2 = belong_which_cluster_better(cluster_belong[i+1], cluster_belong[i+2], i, distance_2, gm)
                # print("444444444441")
                # print(cluster_id)
                # print("44444444444442")
                # print(cluster_id_2)
                if cluster_belong_i != cluster_belong[i+2]:
                    # print("44444444444443")
                    if cluster_id  == cluster_belong_i and cluster_id_2 == cluster_belong[i+2]:
                        #not finished
                        data_count_new.append(data_count_i + data_count[i+1])
                        data_count_new.append(data_count[i+2])
                        cluster_belong_new.append(cluster_belong_i)
                        cluster_belong_new.append(cluster_belong[i+2])
                        # print("a")
                    else:
                        if cluster_id  == cluster_belong_i:
                            data_count_new.append(data_count_i + data_count[i+1])
                            data_count_new.append(data_count[i+2])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+2])
                            # print("b")
                        # elif cluster_id_2 != cluster_belong[i+2]:
                        #     data_count_new.append(data_count_i)
                        #     data_count_new.append(data_count[i+1])  
                        #     data_count_new.append(data_count[i+2])  
                        #     cluster_belong_new.append(cluster_belong_i)
                        #     cluster_belong_new.append(cluster_belong[i+1]) 
                        #     cluster_belong_new.append(cluster_belong[i+2]) 
                        if cluster_id_2 == cluster_belong[i+2]:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1]+ data_count[i+2])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+2])
                            # print("c")
                        elif cluster_id  != cluster_belong_i and cluster_id_2 != cluster_belong[i+2]:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])
                            data_count_new.append(data_count[i+2])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+1])
                            cluster_belong_new.append(cluster_belong[i+2])
                            
                            # print("d")
                            # print(data_count_new)
                            # print(cluster_belong_new)
                            # print(data_count_i)
                            # print(data_count[i+1])
                            # print(data_count[i+2])
                elif cluster_belong_i == cluster_belong[i+2]:
                    #merge together
                    if cluster_id  == cluster_belong_i and cluster_id_2 == cluster_belong[i+2]:
                        #not finished
                        data_count_new.append(data_count_i + data_count[i+1] + data_count[i+2])
                        cluster_belong_new.append(cluster_belong_i)
                        # print("a")
                    else:
                        if cluster_id  == cluster_belong_i:
                            data_count_new.append(data_count_i + data_count[i+1])
                            data_count_new.append(data_count[i+2])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+2])
                            # print("c")
                        if cluster_id_2 == cluster_belong[i+2]:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1] + data_count[i+2])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+2])
                            # print("d")
                        elif cluster_id != cluster_belong_i and cluster_id_2 != cluster_belong[i+2]:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])
                            data_count_new.append(data_count[i+2])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+1])
                            cluster_belong_new.append(cluster_belong[i+2])
                            # print("e")
                i += 2
                
            elif data_count_i == 1:  
                if cluster_belong_i == -1 and cluster_belong[i+1] == -1:
                    data_count_new.append(data_count_i)
                    data_count_new.append(data_count[i+1])
                    cluster_belong_new.append(cluster_belong_i)
                    cluster_belong_new.append(cluster_belong[i+1])
                elif cluster_belong_i != -1 and cluster_belong[i+1] == -1:
                    cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                    # print("5555555555555")
                    # print(cluster_id)
                    if cluster_id == cluster_belong_i:
                        data_count_new.append(data_count_i + data_count[i+1])
                        cluster_belong_new.append(cluster_belong_i)
                    else:
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])
                        cluster_belong_new.append(cluster_belong_i)
                        cluster_belong_new.append(cluster_belong[i+1])
                elif cluster_belong_i == -1 and cluster_belong[i+1] != -1:
                    cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                    # print("66666666666")
                    # print(cluster_id)
                    if cluster_id == cluster_belong[i+1]:
                        data_count_new.append(data_count_i + data_count[i+1])
                        cluster_belong_new.append(cluster_belong[i+1])
                    else:
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])
                        cluster_belong_new.append(cluster_belong_i)
                        cluster_belong_new.append(cluster_belong[i+1])
                elif cluster_belong_i != -1 and cluster_belong[i+1] != -1:
                    cluster_id = belong_which_cluster_better(cluster_belong_i, cluster_belong[i+1], i, distance, gm)
                    # print("7777777777")
                    # print(cluster_id)
                    if cluster_belong_i == cluster_belong[i+1]:
                        if cluster_id == cluster_belong_i:
                            data_count_new.append(data_count_i + data_count[i+1])
                            cluster_belong_new.append(cluster_belong_i)
                        else:
                            data_count_new.append(data_count_i)
                            data_count_new.append(data_count[i+1])
                            cluster_belong_new.append(cluster_belong_i)
                            cluster_belong_new.append(cluster_belong[i+1])
                    elif cluster_belong_i != cluster_belong[i+1]:
                        data_count_new.append(data_count_i)
                        data_count_new.append(data_count[i+1])
                        cluster_belong_new.append(cluster_belong_i)
                        cluster_belong_new.append(cluster_belong[i+1])     
                i += 1
print(data_count)
print(cluster_belong)
print("*******************")
print(data_count_new)
print(cluster_belong_new)

arr_final_draw = []
cnt = 0
count = 0
for i in range(len(data_count_new)):
    if data_count_new[i] == 1:
        arr_final_draw.append(-1)
        continue
    cnt = data_count_new[i]
    for j in range(cnt):
        arr_final_draw.append(count)
    count += 4

# print(arr_final_2)
# print(len(arr_final_2))
draw_figure(arr_final_draw,"final_2",12)  
plt.tight_layout()    
# plt.show()

final_data = []
for i in range(len(data_count_new)):
    if data_count_new[i] == 1:
        final_data.append(-1)
        continue
    cnt = data_count_new[i]
    for j in range(cnt):
        final_data.append(cluster_belong_new[i])
print(final_data)

data_weight_cluster = [[] for i in range(global_cluster_num)]
for i in range(len(final_data)):
    # num = final_data[id]
    # if the point is the outlier, no need to do anything
    cluster_flag = final_data[i]
    if cluster_flag == -1:
        continue
    else:
        data_weight_cluster[cluster_flag].append(data_weight[i])
 
for num in range(global_cluster_num):        
    data_weight_cluster[num].sort()
    print(data_weight_cluster[num])


print("start reading total file to place the order:\n")

data_count_sum = []
cnt = 0
for j in range(len(data_count_new)):
        cnt += data_count_new[j]
        # print(j)
        # print(cnt)
        data_count_sum.append(cnt)
print(data_count_sum)

# probability_ig=[]
p_score=[]
data_partial = np.array(average_distance)

p_g = -gm.score_samples(data_partial.reshape(len(data_partial), 1))
print(p_g)
for i in range(len(data_count_sum)):
    cluster_flag = cluster_belong_new[i]
    if cluster_flag == -1:
        continue
    cnt = 0
    p_new = 1
    p_ig_total = 0
    while(cnt < data_count_new[i] ):
        count_1 = 0
        data_cnt = cnt if i == 0 else (data_count_sum[i-1] + cnt)
        for id_cluster in range(len(data_weight_cluster[cluster_flag])):
            # print("@@@@@@@@@@")
            # print(cluster_flag)
            # print(data_weight[data_cnt])
            # print(data_weight_cluster[cluster_flag][id_cluster])
            if data_weight[data_cnt] > data_weight_cluster[cluster_flag][id_cluster]:
                count_1 += 1
            else:
                print("@@@@@@@@@@")
                # print(count_1) 
                # print(len(data_weight_cluster[cluster_flag]))
                # calculate P(X >= x)
                #??the probality of first number and the last number
                p_ig_score = (1 - MINIMUM_VALUE) if count_1 == 0 else -math.log(1 - count_1 / len(data_weight_cluster[cluster_flag]))
                # print(count_1 / len(data_weight_cluster[cluster_flag]))
                # probability_ig.append(p_ig_score)
                p_ig_total  +=  round(p_ig_score,4)
                print(p_ig_total)
                break
        cnt += 1
    p_score.append((i, p_ig_total + p_g[i]))

p_score_final = sorted(p_score, key=lambda x: x[1], reverse=True) 
print(p_score_final)
for i in range(len(p_score_final)):
    if i < 100:
        print(x1[data_count_sum[p_score_final[i][0]]])
        print(data_count_sum[p_score_final[i][0]])
        print(p_score_final[i])
plt.show()        

    
    
    
        

        
   

   