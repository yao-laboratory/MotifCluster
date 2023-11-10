import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def draw_cluster_weight(input_file, output_folder):
    package_path = os.path.abspath(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))))
    print(package_path)
    final_filename = os.path.join(package_path, input_file)
    output_path = package_path + "/" + output_folder + "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    df = pd.read_csv(final_filename)
    cluster_num = int((len(df.columns) - 1)/2)
    print(cluster_num)
    cluster_weight_length = []
    s = df.iloc[0, cluster_num+1:cluster_num * 2+1]
    s = s.fillna('0').astype('int32', errors='ignore')
    cluster_weight_length = s.tolist()
    data_weight_cluster = [[] for i in range(cluster_num)]
    for i in range(0, cluster_num):
        data_weight_cluster[i] = df.iloc[:, i +
                                         1][0:cluster_weight_length[i]].tolist()
    plt.figure(figsize=(36, 10))
    cnt = int(cluster_num / 2)
    for i in range(0, cluster_num):
        y_temp = data_weight_cluster[i]
        if i < cnt:
            ax = plt.subplot(2, cnt, i+1)
            ns, edgeBin, patches = plt.hist(y_temp, bins=10, rwidth=0.8)
        else:
            ax = plt.subplot(2, cnt, i+1)
            ns, edgeBin, patches = plt.hist(y_temp, bins=10, rwidth=0.8)
        ax.xaxis.set_tick_params(rotation=45)
        ax.xaxis.set_ticks(np.arange(0, cluster_num, 1))
    plt.subplots_adjust(bottom=0.1, left=0.1, right=0.9,
                        top=0.9, wspace=0.4, hspace=0.4)
    path = os.path.join(output_path, 'cluster_weight_draw.pdf')
    plt.savefig(path, bbox_inches='tight')
    plt.show()
