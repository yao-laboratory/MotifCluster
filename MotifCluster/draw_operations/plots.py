import matplotlib
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import operator
import csv
import pandas as pd

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'

# global_cluster_num = 10
x_axis = [10000,20000,50000,100000,150000,200000,227307]
cluster_y_axis = [5.720, 18.258, 104.222, 377.188, 868.760, 1542.814, 1888.677]
score_y_axis = [1.024, 3.318,19.768, 72.874, 167.406, 337.943, 394.552]
plt.figure(figsize=(20,20)) 
plt.plot(x_axis,cluster_y_axis)
plt.scatter(x_axis,cluster_y_axis,c='red',s=50)
plt.xticks(x_axis)
plt.xlim(0,250000)
plt.ylim(0,2000)

plt.plot(x_axis,score_y_axis)
plt.scatter(x_axis,score_y_axis,c='red',s=50)
plt.xticks(x_axis)
plt.savefig('time_calculate.pdf', bbox_inches='tight')
