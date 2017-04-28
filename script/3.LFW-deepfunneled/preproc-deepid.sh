#!/bin/bash
# image shrink
# python ../src/verify_pre/lfw_img_crop.py ~/Faces/lfw-deepfunneled ./lfw/
# image split
python ../src/joint_bayesian/deepid_data_split.py ./lfw/ img_list.csv
# image vectorize
python ../src/joint_bayesian/deepid_vectorize_img.py img_list.csv data_vec
