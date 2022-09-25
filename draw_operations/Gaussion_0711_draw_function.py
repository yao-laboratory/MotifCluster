from pickle import FALSE
from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
import operator

# extend x axis
def extend_xplot(x, y, x_maxsize, id):
    # print(x,y)
    # plt.figure()
    # plt.plot(x, y)
    #plt.ylim((0, 1000))
    # plt.title("clusters radius: "+ id)
    plt.xlabel("X")
    plt.ylabel("Y")
    
    # change x internal size
    plt.gca().margins(x=0.1)
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
    color_num = len(labels)
    clrs = []
    # all_color = (65536 * 255) + (256 * 255) + 200
    # for i in np.linspace(256,all_color,color_num):
    for i in np.linspace(16711680,255,color_num):
        c = int(i)
        # print(c)
        clrs.append('#%06x'%c)
        # print(clrs)
    
    use_colours = list(enumerate(clrs))
    # use_colours = [(-1,"#000000")]
    # use_colours.append(other_colors)
    # print(use_colours)
    # print(labels)
    group_color = []
    label_temp = -100
    color_temp = 0
    for la in range(len(labels)):
        if labels[la] != -1: 
            if labels[la] != label_temp:
                b1 = operator.itemgetter(la)
                group_color.append(b1(use_colours)[1])
                color_temp = b1(use_colours)[1]
                label_temp = labels[la]
            else:
                group_color.append(color_temp)
    # print(group_color)
    return group_color
 
def draw_figure(data, id, num, x1, y1, Axes):
    plt.setp(Axes[num], ylabel='')
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
    # if num == 12:
    #     print("normal:")
    #     print(x_normal, y_normal)
    # if num > 1:
    # axn = plt.subplot(12,1,num,sharex=ax1,sharey = ax1)
    # if num < 12:
    #     axn.set_xticks([])
    # elif num == 12: 
        # axn.axes.xaxis.set_major_locator(plt.AutoLocator()) 
    # plt.sca(plt.subplot(12,1,num))
    # print(x_outlier)
    # print(x_normal)
    Axes[num].vlines(x_outlier, 0, y_outlier, colors=group_color_outlier, linestyles='dotted', label='', data=None) 
    Axes[num].vlines(x_normal, 0, y_normal, colors=group_color_normal, linestyles='solid', label='', data=None) 
    # if num == 12:
    #     plt.setp(plt.subplot(12,1,1).get_yticklabels(), fontsize=6)
    # Axes[num].subplots_adjust(wspace=0.01,hspace=0.01)
    # plt.tight_layout()
    # # plt.scatter(x1, y1, s=area, c=group_color, alpha=0.4, label='mean1')
    # # plt.legend()
    # # plt.savefig(r'E:\second semester\bioinformatics\notes\1.png', dpi=300)   
    # plt.show()
    # if num < 12:
    #     Axes[num].xaxis.set_tick_params(labelbottom=False)
    # Axes[num].set_box_aspect(aspect=1)
    Axes[num].set_ylim(0, 10) 
    
