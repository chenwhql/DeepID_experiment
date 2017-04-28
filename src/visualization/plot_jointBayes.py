#coding=utf-8

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def prec_plot(threshold, prec_false, prec_true, prec):
    plt.figure()

    plt.plot(threshold, prec_false, label="precision on Neg")
    plt.plot(threshold, prec_true, label="Precision on Pos")
    plt.plot(threshold, prec, label="Precision total")
    plt.xlabel("precision")
    plt.ylabel("threshold")
    # plt.xlim(0, epochs[-1])
    # plt.ylim(0, 100)
    plt.legend()
    plt.title("Verification Precision on LFW")

def recall_plot(threshold, recall_false, recall_true, recall):
    plt.figure()

    plt.plot(threshold, recall_false, label="Recall on Neg")
    plt.plot(threshold, recall_true, label="Recall on Pos")
    plt.plot(threshold, recall, label="Recall total")
    plt.xlabel("Recall")
    plt.ylabel("threshold")
    # plt.xlim(0, epochs[-1])
    # plt.ylim(0, 100)
    plt.legend()
    plt.title("Verification Recall on LFW")

def f1_plot(threshold, f1_false, f1_true, f1):
    plt.figure()

    plt.plot(threshold, f1_false, label="f1-score on Neg")
    plt.plot(threshold, f1_true, label="f1-score on Pos")
    plt.plot(threshold, f1, label="f1-score total")
    plt.xlabel("f1-score")
    plt.ylabel("threshold")
    # plt.xlim(0, epochs[-1])
    # plt.ylim(0, 100)
    plt.legend()
    plt.title("Verification f1-score on LFW")


def plot(err_result_file):

    threshold = []

    prec_false = []
    prec_true = []
    prec = []

    recall_false = []
    recall_true = []
    recall = []

    f1_false = []
    f1_true = []
    f1 = []

    file = open(err_result_file, 'rb')
    for line in file:
        line = line.strip(' \n')
        thre, pf, rf, ff, pt, rt, ft, p, r, fs, nl = line.split(' ')
        
        threshold.append(float(thre))

        prec_false.append(float(pf))
        recall_false.append(float(rf))
        f1_false.append(float(ff))

        prec_true.append(float(pt))
        recall_true.append(float(rt))
        f1_true.append(float(ft))

        prec.append(float(p))
        recall.append(float(r))
        f1.append(float(fs))

    file.close()

    prec_plot(threshold, prec_false, prec_true, prec)
    recall_plot(threshold, recall_false, recall_true, recall)
    f1_plot(threshold, f1_false, f1_true, f1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s err_result_file' % (sys.argv[0])
        sys.exit()

    err_result_file = sys.argv[1]

    plot(err_result_file) 
    plt.show() 
