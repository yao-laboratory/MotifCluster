from ast import Return
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.mixture import GaussianMixture

def normal_distribution(x, gm, i):
    return (1 / math.sqrt(2 * np.pi * gm.covariances_[i])) * np.exp(-1 *((x - gm.means_[i])**2) / (2 * gm.covariances_[i]))

def draw_gmm():
    # reload
    gm_name = '/home/eilene/Downloads/GMM'
    means = np.load(gm_name + '_means.npy')
    covar = np.load(gm_name + '_covariances.npy')
    loaded_gm = GaussianMixture(n_components = len(means), covariance_type='full')
    loaded_gm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(covar))
    loaded_gm.weights_ = np.load(gm_name + '_weights.npy')
    loaded_gm.means_ = means
    loaded_gm.covariances_ = covar
    for i in range(0,10):
        x_temp = np.linspace(loaded_gm.means_[i] - 6*math.sqrt(loaded_gm.covariances_[i]), loaded_gm.means_[i] + 6*math.sqrt(loaded_gm.covariances_[i]), 100)
        y_temp = normal_distribution(x_temp, loaded_gm, i)
        plt.plot(x_temp, y_temp, 'r', label='GMM')
    plt.legend()
    plt.grid()
    plt.show()