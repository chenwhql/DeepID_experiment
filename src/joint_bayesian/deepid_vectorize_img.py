#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random
import numpy as np
import PIL.Image as Image

def read_csv_file(csv_file):
    path_and_labels = []
    f = open(csv_file, 'rb')
    for line in f:
        line = line.strip('\r\n')
        path, label = line.split(',')
        label = int(label)
        path_and_labels.append((path, label))
    f.close()
    random.shuffle(path_and_labels)
    return path_and_labels

def vectorize_imgs(path_and_labels, image_size):
    image_vector_len = np.prod(image_size)
    
    arrs   = []
    labels = [] 
    i = 0
    for path_and_label in path_and_labels:
        path, label = path_and_label
        img = Image.open(path)
        # img = Image.open(path).convert("RGB")
        arr_img = np.asarray(img, dtype='float64')
        arr_img = arr_img.transpose(2,0,1).reshape((image_vector_len, ))
        
        labels.append(label)
        arrs.append(arr_img)

        i += 1
        # if i % 100 == 0:
        sys.stdout.write('\rdone: ' + str(i))
        sys.stdout.flush()
    print ''
    arrs = np.asarray(arrs, dtype='float64')
    labels = np.asarray(labels, dtype='int32')
    return (arrs, labels)

def cPickle_output(vars, file_name):
    import cPickle
    f = open(file_name, 'wb')
    cPickle.dump(vars, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()

def output_data(vector_vars, vector_folder, batch_size=1000):
    if not vector_folder.endswith('/'):
        vector_folder += '/'
    if not os.path.exists(vector_folder):
        os.mkdir(vector_folder)
    x, y = vector_vars
    n_batch = len(x) / batch_size
    for i in range(n_batch):
        file_name = vector_folder + str("%02d" % i) + '.pkl'
        batch_x = x[ i*batch_size: (i+1)*batch_size]
        batch_y = y[ i*batch_size: (i+1)*batch_size]
        cPickle_output((batch_x, batch_y), file_name)
    if n_batch * batch_size < len(x):
        batch_x = x[n_batch*batch_size: ]
        batch_y = y[n_batch*batch_size: ]
        file_name = vector_folder + str("%02d" % n_batch) + '.pkl'
        cPickle_output((batch_x, batch_y), file_name)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s data_set_file data_vector_folder' % (sys.argv[0])
        sys.exit()
    data_set_file  = sys.argv[1]
    data_vector_folder  = sys.argv[2]
    
    data_path_and_labels  = read_csv_file(data_set_file)

    print '3. images vectorize'

    print 'data  img num: %d' % (len(data_path_and_labels))

    img_size = (3, 55, 47)  # channel, height, width
    data_vec  = vectorize_imgs(data_path_and_labels, img_size)

    output_data(data_vec,  data_vector_folder)

