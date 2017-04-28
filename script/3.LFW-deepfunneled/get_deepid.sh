#!/bin/bash
python ../src/conv_net/deepid_generate.py left_vec params_file_webface left_vec_deepid
python ../src/conv_net/deepid_generate.py right_vec params_file_webface right_vec_deepid
