#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random

def walk_through_pairs_for_split(lfwdir, pairslist, ext='jpg'):
    left_set    = []
    right_set = []

    num = 0
    for lines in pairslist:

        dir_left=lfwdir+lines['img1']+'/'
        dir_right=lfwdir+lines['img2']+'/'

        file_left=lines['img1']+'_'+str("%04d" % int(lines["num1"]))+'.'+ext
        file_right=lines['img2']+'_'+str("%04d" % int(lines["num2"]))+'.'+ext

        path_left=dir_left+file_left
        path_right=dir_right+file_right

        if int(lines["flag"])==1:
            label = 1
        else:
            label = 0

        left_set.append((path_left, label))
        right_set.append((path_right, label))
            
        num += 1
        sys.stdout.write('\rdone: ' + str(num))
        sys.stdout.flush()

    print '\nleft set num: %d' % (len(left_set))
    print 'right set num: %d' % (len(right_set))
    return left_set, right_set

#读取LFW的pairs.txt保存到result中
def read_paris(filelist="pairs.txt"):
    filelist=str(filelist)
    fp=open(filelist,'r')
    result=[]
    for lines in fp.readlines():
        lines=lines.replace("\n","").split("\t")
        if len(lines)==2:
            print "lenth=2:"+str(lines)
            continue
        elif len(lines)==3:
            pairs={
                    'flag':1,
                    'img1':lines[0],
                    'img2':lines[0],
                    'num1':lines[1],
                    'num2':lines[2],
                    }
            result.append(pairs)
            continue
        elif len(lines)==4:
            pairs={
                'flag':2,
                'img1':lines[0],
                'num1':lines[1],
                'img2':lines[2],
                'num2':lines[3],
                }
            result.append(pairs)
        else:
            print "read file Error!"
            exit()
    fp.close
    print "Read paris.txt DONE!"
    return result


def set_to_csv_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = item[0] + ',' + str(item[1]) + '\n'
        f.write(line)
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: python %s src_folder pairs_file left_set_file right_set_file' % (sys.argv[0])
        sys.exit()
    src_folder        = sys.argv[1]
    pairs_file        = sys.argv[2]
    left_set_file     = sys.argv[3]
    right_set_file    = sys.argv[4]
    if not src_folder.endswith('/'):
        src_folder += '/'

    print '2. images split'

    pairslist = read_paris(pairs_file)
    
    left_set, right_set = walk_through_pairs_for_split(src_folder, pairslist, 'jpg')
    set_to_csv_file(left_set, left_set_file)
    set_to_csv_file(right_set, right_set_file)


    



