#!/usr/bin/env python
# -*- coding:utf8 -*-

from load_data import *
from pre_process import *
from parse import *
from evaluate import evaluate_precision
import sklearn.metrics.pairwise as pw
# from verify_pre.vectorize_img import cPickle_output
import numpy as np
import sys
import os

def load_left_and_right(right_data_folder, left_data_folder):
    right_file_names  = get_files(right_data_folder)
    left_file_names = get_files(left_data_folder)
    right_x, right_y   = load_data_xy(right_file_names)
    left_x, left_y = load_data_xy(left_file_names)
    print 'right_x:  ', right_x.shape
    print 'right_y:  ', right_y.shape
    print 'left_x: ', left_x.shape
    print 'left_y: ', left_y.shape
    return right_x, right_y, left_x, left_y

def cPickle_output(vars, file_name):
    import cPickle
    f = open(file_name, 'wb')
    cPickle.dump(vars, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()

def verify(right_x, right_y, left_x, left_y, str_pre_process, str_sim_metric, params, threshold):
    pre_process_method = pre_process_methods_set[str_pre_process]
    if pre_process_method != None:
        right_x, left_x = pre_process_method(right_x, left_x, params)

    sim_metric_method = sim_metric_methods_set[str_sim_metric]
    if str_sim_metric == 'cos':
        right_x, left_x = norm_data(right_x, left_x)

    assert right_x.shape[1] == left_x.shape[1]
    verify_sample_num = len(right_x)

    verify_results = []
    predicts = []
    # 提取值
    for i in range(verify_sample_num):
        left = left_x[i]
        right = right_x[i]
        sim_result = sim_metric_method(left, right)
        predicts.append(sim_result)

    # 归一化
    for i in range(verify_sample_num):
        predicts[i] = (predicts[i]-np.min(predicts))/(np.max(predicts)-np.min(predicts))
        # print right_y[i], predicts[i]

    # 二值化
    print 'threshold: ' + str(threshold)
    predict_bool = np.empty((verify_sample_num,))
    for i in range(verify_sample_num):
        if float(predicts[i]) > float(threshold):
            predict_bool[i] = 1
            # print right_y[i], predicts[i], predict_bool[i]
        else:
            predict_bool[i] = 0
            # print right_y[i], predicts[i], predict_bool[i]
        # print right_y[i], predicts[i]

    # 生成结果对
    for i in range(verify_sample_num):
        right_label = right_y[i]

        verify_results.append((right_label, predict_bool[i]))

        sys.stdout.write('\rdone: ' + str(i + 1))
        sys.stdout.flush()
    print ''
    return verify_results

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s exp_param result_file' % (sys.argv[0])
        sys.exit()

    exp_params_file = sys.argv[1]
    verify_results_file = sys.argv[2]
    # threshold = sys.argv[3]
    params_results, right_data_folder, left_data_folder = parse_params(exp_params_file)
    right_x, right_y, left_x, left_y = load_left_and_right(right_data_folder, left_data_folder)

    print ''
    print '%d experiments' % (len(params_results))

    for params in params_results:
        description = params['description']
        exp_id = params['id']
        print ''
        print '*************************************************'
        print exp_id, '--', description
        str_pre_process = params['pre_process_method']
        str_sim_metric  = params['sim_metric_method']

        # 将多参数尝试的结果保存
        file_name = str_pre_process + '_' + str_sim_metric + '.csv'
        f = open(file_name, 'wb')
        threshold = 0.1
        for i in range(45):
            verify_results = verify(right_x, right_y, left_x, left_y, 
                    str_pre_process, str_sim_metric, params, threshold)
            right_precision = evaluate_precision(verify_results)
            line = str(threshold) + ',' + str(right_precision) + '\n'
            f.write(line)
            threshold += 0.02
        f.close()

    # cPickle_output(verify_results, verify_results_file)

