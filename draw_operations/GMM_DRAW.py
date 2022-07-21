from ast import Return
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.mixture import GaussianMixture

def normal_distribution(x, gm, i):
    # return np.exp(-1*((x-mean)**2)/(2*(sigma**2)))/(math.sqrt(2*np.pi) * sigma)
    return (1 / math.sqrt(2 * np.pi * gm.covariances_[i])) * np.exp(-1 *((x - gm.means_[i])**2) / (2 * gm.covariances_[i]))
        # print("p:")
        # print(value)

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
    
    # mean2, sigma2 = 0, 2
    # x2 = np.linspace(mean2 - 6*sigma2, mean2 + 6*sigma2, 100)
    
    # mean3, sigma3 = 5, 1
    # x3 = np.linspace(mean3 - 6*sigma3, mean3 + 6*sigma3, 100)
    
        y_temp = normal_distribution(x_temp, loaded_gm, i)
    # y2 = normal_distribution(x2, mean2, sigma2)
    # y3 = normal_distribution(x3, mean3, sigma3)
    
        plt.plot(x_temp, y_temp, 'r', label='GMM')
    # plt.plot(x2, y2, 'g', label='m=0,sig=2')
    # plt.plot(x3, y3, 'b', label='m=1,sig=1')
    plt.legend()
    plt.grid()
    plt.show()