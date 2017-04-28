#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random

def walk_through_folder_for_split(src_folder):
    data_set  = []
    
    label = 0
    for people_folder in os.listdir(src_folder):
        people_path = src_folder + people_folder + '/'
        img_files  = os.listdir(people_path)
        for img_file in img_files:
            img_path = people_path + img_file
            data_set.append((img_path, label))

        label += 1
        sys.stdout.write('\rdone: ' + str(label))
        sys.stdout.flush()
    print ''
    print 'data set num: %d' % (len(data_set))
    return data_set

def set_to_csv_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = item[0] + ',' + str(item[1]) + '\n'
        f.write(line)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s src_folder data_set_file' % (sys.argv[0])
        sys.exit()
    src_folder     = sys.argv[1]
    data_set_file  = sys.argv[2]
    if not src_folder.endswith('/'):
        src_folder += '/'

    print '2. images split'
    
    data_set = walk_through_folder_for_split(src_folder)
    set_to_csv_file(data_set,  data_set_file)
