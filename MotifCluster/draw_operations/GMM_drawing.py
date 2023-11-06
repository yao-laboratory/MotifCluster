from ast import Return
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.mixture import GaussianMixture
import os

def normal_distribution(x, gm, i):
    return (1 / math.sqrt(2 * np.pi * gm.covariances_[i])) * np.exp(-1 *((x - gm.means_[i])**2) / (2 * gm.covariances_[i]))

def draw_gmm(output_folder):
    # reload
    package_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print(package_path)
    middle_results_path = package_path + "/example_middle_output/"
    output_path = package_path + "/" + output_folder + "/"
    if not os.path.exists(middle_results_path):
        os.makedirs(middle_results_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    means = np.load(middle_results_path + 'GMM_means.npy')
    covar = np.load(middle_results_path + 'GMM_covariances.npy')
    loaded_gm = GaussianMixture(n_components = len(means), covariance_type='full')
    loaded_gm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(covar))
    loaded_gm.weights_ = np.load(middle_results_path + 'GMM_weights.npy')
    loaded_gm.means_ = means
    loaded_gm.covariances_ = covar
    for i in range(0,10):
        x_temp = np.linspace(loaded_gm.means_[i] - 6*math.sqrt(loaded_gm.covariances_[i]), loaded_gm.means_[i] + 6*math.sqrt(loaded_gm.covariances_[i]), 100)
        y_temp = normal_distribution(x_temp, loaded_gm, i)
        plt.plot(x_temp, y_temp, 'r', label='GMM')
    plt.legend()
    path = os.path.join(output_path, 'GMM_drawing.pdf')
    plt.savefig(path, bbox_inches='tight')
    plt.grid()
    plt.show()