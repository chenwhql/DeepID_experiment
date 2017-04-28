#coding=utf-8

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def err_plot():
    plt.figure()

    threshold = []
    euc_prec1 = []
    cos_prec1 = []
    f = open("pca_euc_cos.csv", 'rb')
    for line in f:
        line = line.strip('\n')
        thre, euc, cos = line.split(',')
        threshold.append(float(thre))
        euc_prec1.append(float(euc))
        cos_prec1.append(float(cos))
    f.close()

    euc_prec2 = []
    cos_prec2 = []
    f = open("deepid_20_euc_cos.csv", 'rb')
    for line in f:
        line = line.strip('\n')
        thre, euc, cos = line.split(',')
        # threshold.append(float(thre))
        euc_prec2.append(float(euc))
        cos_prec2.append(float(cos))
    f.close()

    euc_prec3 = []
    cos_prec3 = []
    f = open("deepid_50_euc_cos.csv", 'rb')
    for line in f:
        line = line.strip('\n')
        thre, euc, cos = line.split(',')
        # threshold.append(float(thre))
        euc_prec3.append(float(euc))
        cos_prec3.append(float(cos))
    f.close()

    plt.plot(threshold, euc_prec1, label="Euclidean precision PCA")
    plt.plot(threshold, cos_prec1, label="Cosine precision PCA")
    plt.plot(threshold, euc_prec2, label="Euclidean precision DeepID_20")
    plt.plot(threshold, cos_prec2, label="Cosine precision DeepID_20")
    plt.plot(threshold, euc_prec3, label="Euclidean precision DeepID_50")
    plt.plot(threshold, cos_prec3, label="Cosine precision DeepID_50")
    plt.xlabel("threshold")
    plt.ylabel("precision")
    # plt.xlim(0, epochs[-1])
    # plt.ylim(0, 100)
    plt.legend()
    plt.title("Naive verification method precision")

if __name__ == '__main__':

    err_plot() 
    plt.show() 
