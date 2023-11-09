# from pickle import FALSE
# from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
import operator

# extend x axis
def extend_xplot(x, y, x_maxsize, id):
    plt.xlabel("X")
    plt.ylabel("Y")
    
    # change x internal size
    plt.gca().margins(x=0.1)
    plt.gcf().canvas.draw()
    
    # set size
    m = 0.2
    N =len(x)
    s = x_maxsize / plt.gcf().dpi * N + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]

    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])


def set_clusters_outlier_color(labels):
    group_color = []
    for la in labels:
        if la == -1:
            group_color.append('#000000')
    return group_color
    
def set_clusters_normal_color(labels):
    color_num = len(labels)
    clrs = []
    for i in np.linspace(16711680,255,color_num):
        c = int(i)
        clrs.append('#%06x'%c)
    
    use_colours = list(enumerate(clrs))
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
        if data[li] == -1:
            x_outlier.append(x1[li])
            y_outlier.append(y1[li])
        else:
            x_normal.append(x1[li])
            y_normal.append(y1[li])
    Axes[num].vlines(x_outlier, 0, y_outlier, colors=group_color_outlier, linestyles='dotted', label='', data=None) 
    Axes[num].vlines(x_normal, 0, y_normal, colors=group_color_normal, linestyles='solid', label='', data=None) 
    Axes[num].set_ylim(0, 10) 
    
