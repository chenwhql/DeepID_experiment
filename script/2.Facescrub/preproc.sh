#!/bin/bash
# image shrink
python ../src/data_prepare/img_crop.py /home/chenweihang/faces/Facescrub/faceonly/ ../2.Facescrub/facescrub/
# image split
python ../src/data_prepare/data_split_facescrub.py ../2.Facescrub/facescrub/ testset_img_list.csv trainset_img_list.csv
# image vectorize
python ../src/data_prepare/vectorize_img.py testset_img_list.csv trainset_img_list.csv test_vector_folder train_vector_folder
