#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random
import numpy as np
import PIL.Image as Image
from scipy.io import savemat

#读取LFW的pairs.txt保存到result中
def read_paris(filelist="pairs.txt"):
    filelist=str(filelist)
    fp=open(filelist,'r')
    intra_result = []
    extra_result = []
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
            intra_result.append(pairs)
            continue
        elif len(lines)==4:
            pairs={
                'flag':2,
                'img1':lines[0],
                'num1':lines[1],
                'img2':lines[2],
                'num2':lines[3],
                }
            extra_result.append(pairs)
        else:
            print "read file Error!"
            exit()
    fp.close
    print "Read paris.txt DONE!"
    return intra_result, extra_result

def pairs_to_index(pair_list, data_set, img_label):
    num = 0
    s = len(pair_list)
    PersonPair = []


    for lines in pair_list:
        num = num + 1
        if num % 100 == 0:
            print str(num)+"/"+str(s)
        img1_name = lines['img1']+'_'+str("%04d" % int(lines["num1"]))+'.jpg'
        img2_name = lines['img2']+'_'+str("%04d" % int(lines["num2"]))+'.jpg'
        img1_index = img_label[data_set.index(img1_name)]
        img2_index = img_label[data_set.index(img2_name)]
        PersonPair.append((img1_index, img2_index))

    return PersonPair

def walk_through_folder(src_folder):
    data_path = []
    data_set = []
    person_label = []
    img_label = []
    
    plabel = 1
    ilabel = 1
    for people_folder in os.listdir(src_folder):
        people_path = src_folder + people_folder + '/'
        img_files  = os.listdir(people_path)
        for img_file in img_files:
            img_path = people_path + img_file
            data_path.append(img_path)
            data_set.append(img_file)
            person_label.append(plabel)
            img_label.append(ilabel)
            ilabel += 1

        plabel += 1
        sys.stdout.write('\rdone: ' + str(plabel))
        sys.stdout.flush()
    print ''
    print 'data set num: %d' % (len(data_set))
    return data_path, data_set, person_label, img_label

def vectorize_imgs(data_paths, image_size):
    image_vector_len = np.prod(image_size)    
    arrs   = []
    i = 0
    for path in data_paths:
        img = Image.open(path)
        # img = Image.open(path).convert("RGB")
        arr_img = np.asarray(img, dtype='float64')
        arr_img = arr_img.transpose(2,0,1).reshape((image_vector_len, ))
        
        arrs.append(arr_img)

        i += 1
        # if i % 100 == 0:
        sys.stdout.write('\rdone: ' + str(i))
        sys.stdout.flush()
    print ''
    arrs = np.asarray(arrs, dtype='float64')
    return arrs

def set_to_txt_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = str(item) + '\n'
        f.write(line)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python %s src_folder pairslist result_folder' % (sys.argv[0])
        sys.exit()
    src_folder     = sys.argv[1]
    pairslist  = sys.argv[2]
    result_folder  = sys.argv[3]
    if not src_folder.endswith('/'):
        src_folder += '/'
    if not result_folder.endswith('/'):
        result_folder += '/'

    data_path, data_set, person_label, img_label = walk_through_folder(src_folder)
    set_to_txt_file(data_path, "lfw_img_pathlist.txt")
    set_to_txt_file(data_set, "lfw_img_namelist.txt")
    set_to_txt_file(person_label, "lfw_img_labellist.txt")

    img_size = (3, 55, 47)
    img_vec = vectorize_imgs(data_path, img_size)

    # save the img vec and label to mat
    savemat(result_folder+'lbp_lfw_cwh.mat', {"lbp_lfw_cwh":img_vec})
    person_label = np.transpose(person_label)
    savemat(result_folder+'id_lfw_cwh.mat', {"id_lfw_cwh":person_label})

    # deal the pairslist
    intra_result, extra_result = read_paris(pairslist)
    IntroPersonPair = pairs_to_index(intra_result, data_set, img_label)
    ExtroPersonPair = pairs_to_index(extra_result, data_set, img_label)

    #save pairlist
    savemat(result_folder+'pairlist_lfw_cwh.mat', {"pairlist_lfw_cwh":{"IntraPersonPair":IntroPersonPair, "ExtraPersonPair":ExtroPersonPair}})

