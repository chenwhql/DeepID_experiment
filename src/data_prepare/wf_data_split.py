#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random

def walk_through_folder_for_split(src_folder):
    test_set  = []
    train_set = []
    
    label = 0
    for people_folder in os.listdir(src_folder):
        people_path = src_folder + people_folder + '/'
        people_imgs = []
        img_files  = os.listdir(people_path)
        for img_file in img_files:
            img_path = people_path + img_file
            people_imgs.append((img_path, label))
        if len(people_imgs) < 20:
            continue
        random.shuffle(people_imgs)
        test_set  += people_imgs[0:4] # there is only one image in some folders, maybe error!
        train_set += people_imgs[4:20]

        label += 1
        sys.stdout.write('\rdone: ' + str(label))
        sys.stdout.flush()
    print ''
    print 'test  set num: %d' % (len(test_set))
    print 'train set num: %d' % (len(train_set))
    return test_set, train_set

def set_to_csv_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = item[0] + ',' + str(item[1]) + '\n'
        f.write(line)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python %s src_folder test_set_file train_set_file' % (sys.argv[0])
        sys.exit()
    src_folder     = sys.argv[1]
    test_set_file  = sys.argv[2]
    train_set_file = sys.argv[3]
    if not src_folder.endswith('/'):
        src_folder += '/'

    print '2. images split'
    
    test_set, train_set = walk_through_folder_for_split(src_folder)
    set_to_csv_file(test_set,  test_set_file)
    set_to_csv_file(train_set, train_set_file)
