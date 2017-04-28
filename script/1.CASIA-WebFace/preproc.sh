#!/bin/bash
# image shrink
python ../src/data_prepare/wf_img_crop.py /home/chenweihang/faces/faces_aligned_croped/CASIA-WebFace ../1.CASIA-WebFace/webface/
# image split
python ../src/data_prepare/wf_data_split.py ../1.CASIA-WebFace/webface/ testset_img_list.csv trainset_img_list.csv
# image vectorize
python ../src/data_prepare/vectorize_img.py testset_img_list.csv trainset_img_list.csv test_vector_folder train_vector_folder
