#!/usr/bin/env python
# -*- coding:utf8 -*-

import PIL.Image as Image
import sys
import os


def crop_img_by_half_center(src_file_path, dest_file_path):
    im = Image.open(src_file_path)
    x_size, y_size = im.size
    # start_point_xy = x_size / 4
    # end_point_xy   = x_size / 4 + x_size / 2
    # box = (start_point_xy, start_point_xy, end_point_xy, end_point_xy)
    box = (83, 92, 166, 175)
    new_im = im.crop(box)
    new_new_im = new_im.resize((47,55))
    new_new_im.save(dest_file_path)

def walk_through_the_folder_for_crop(src_folder, result_folder):
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    i = 0
    img_count = 0
    for people_folder in os.listdir(src_folder):
        src_people_path = src_folder + people_folder + '/'
        dest_people_path = result_folder + people_folder + '/'
        if not os.path.exists(dest_people_path):
            os.mkdir(dest_people_path)
        
        for img_file in os.listdir(src_people_path):
            src_img_path  = src_people_path + img_file
            dest_img_path = dest_people_path + img_file
            crop_img_by_half_center(src_img_path, dest_img_path)
        i += 1
        img_count += len(os.listdir(src_people_path))
        sys.stdout.write('\rsub_folder: %d, imgs %d' % (i, img_count) )
        sys.stdout.flush()
    print ''
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s src_folder result_folder' % (sys.argv[0])
        sys.exit()
    src_folder = sys.argv[1]
    result_folder = sys.argv[2]
    if not src_folder.endswith('/'):
        src_folder += '/'
    if not result_folder.endswith('/'):
        result_folder += '/'

    print '1. images crop'

    walk_through_the_folder_for_crop(src_folder, result_folder)
    
