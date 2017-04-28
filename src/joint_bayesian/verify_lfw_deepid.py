#coding=utf-8
import sys
import numpy as np
from common import *
from scipy.io import loadmat
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from joint_bayesian import *

def excute_test(pairlist="./lfw_data_self/pairlist_lfw_cwh.mat", test_data="./lfw_data_self/lbp_lfw_deepid.mat", result_fold="./result/"):
    with open(result_fold+"A.pkl", "r") as f:  #windows
    # with open(result_fold+"A.pkl", "rb") as f: #linux
        A = pickle.load(f)
    with open(result_fold+"G.pkl", "r") as f:
    # with open(result_fold+"G.pkl", "rb") as f:
        G = pickle.load(f)

    pair_list = loadmat(pairlist)['pairlist_lfw_cwh']
    test_Intra = pair_list['IntraPersonPair'][0][0] - 1
    test_Extra = pair_list['ExtraPersonPair'][0][0] - 1


    print test_Intra, test_Intra.shape
    print test_Extra, test_Extra.shape

    data  = loadmat(test_data)['lbp_lfw_deepid']
    # data  = data_pre(data)
    data_to_pkl(data, result_fold+"pca_lfw_deepid.pkl")

    data = read_pkl(result_fold+"pca_lfw_deepid.pkl")
    print data.shape

    dist_Intra = get_ratios(A, G, test_Intra, data)
    dist_Extra = get_ratios(A, G, test_Extra, data)

    dist_all = dist_Intra + dist_Extra
    dist_all = np.asarray(dist_all)
    label    = np.append(np.repeat(1, len(dist_Intra)), np.repeat(0, len(dist_Extra)))

    data_to_pkl({"distance": dist_all, "label": label}, result_fold+"result_deepid.pkl")

if __name__ == "__main__":

    excute_test()
    excute_performance("./result/result_deepid.pkl", -100, 100, 5)
