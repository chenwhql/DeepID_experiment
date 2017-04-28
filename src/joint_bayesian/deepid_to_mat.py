#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import numpy as np
import pickle
from scipy.io import loadmat, savemat

def load_data_xy(dataset_path):
    print 'loading data of %s' % (dataset_path)
    f = open(dataset_path, 'rb')
    x, y = pickle.load(f)
    f.close()
    return x,y

def deepid_to_mat(dataset_folder, result_folder):
    deepid = []

    for i in range(14):
        file_name = str("%02d" % i) + '.pkl'
        dataset_path = dataset_folder + file_name
        x, y = load_data_xy(dataset_path)
        print x.shape
        for vec in x:
            deepid.append(vec)

    savemat(result_folder+'lbp_lfw_deepid.mat', {"lbp_lfw_deepid":deepid})


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s dataset_folder result_folder' % (sys.argv[0])
        sys.exit()

    dataset_folder = sys.argv[1]
    result_folder  = sys.argv[2]
    if not dataset_folder.endswith('/'):
        dataset_folder += '/'
    if not result_folder.endswith('/'):
        result_folder += '/'

    deepid_to_mat(dataset_folder, result_folder)