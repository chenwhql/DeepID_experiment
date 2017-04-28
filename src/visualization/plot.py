#coding=utf-8

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def err_plot(err_result_file):
    plt.figure()

    epochs = []
    train_error = []
    valid_error = []

    f = open(err_result_file, 'rb')
    for line in f:
        line = line.strip('\n')
        num, trainerr, validerr = line.split(' ')
        epoch = int(num)
        trainerr = float(trainerr)
        validerr = float(validerr)
        epochs.append(epoch)
        train_error.append(trainerr)
        valid_error.append(validerr)
    f.close()

    plt.plot(epochs, train_error, label="train error")
    plt.plot(epochs, valid_error, label="valid error")
    plt.xlabel("epochs")
    plt.ylabel("train and valid error")
    plt.xlim(0, epochs[-1])
    # plt.ylim(0, 100)
    plt.legend()
    plt.title("DeepID on CASIA-Webface")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s err_result_file' % (sys.argv[0])
        sys.exit()

    err_result_file = sys.argv[1]

    err_plot(err_result_file) 
    plt.show() 
