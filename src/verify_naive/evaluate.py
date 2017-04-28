#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import pickle

def evaluate_precision(results):
    '''retrieval is right when right prediction appears in top-N'''
    num_samples  = len(results)
    right_cnt  = 0
    for line in results:
        test_label, predict_label = line
        if predict_label == test_label:
            right_cnt +=1
    right_precision = right_cnt * 1.0 / (num_samples)
    print 'precision: %f = %d / %d' % (right_precision, right_cnt, num_samples)
    return right_precision

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s verify_results_file' % (sys.argv[0])
        sys.exit()

    verify_results_file = sys.argv[1]
    f = open(search_results_file, 'rb')
    results = pickle.load(f)
    f.close()

    evaluate_precision(results)
    
