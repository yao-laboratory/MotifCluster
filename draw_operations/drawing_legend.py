import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import csv,re
from collections import namedtuple

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'

colors = ["mediumorchid", "steelblue", "darkblue"]
f = lambda m,c: plt.plot([],[],marker="o", color=c, ls="none")[0]
handles = [f("s", colors[i]) for i in range(3)]
labels = colors
legend = plt.legend( ['both rank <= 100', 'rank <= 100 in chr12 p value < 0.001 except rank <= 100 in chr12 p value < 0.005 ','rank <= 100 in chr12 p value < 0.005 except rank <= 100 in chr12 p value < 0.001'],
            fancybox=True,loc='center left', bbox_to_anchor=(0.2, 1.12))

def export_legend(legend, filename="legend.pdf"):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)

export_legend(legend)
plt.show()