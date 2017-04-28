    #!/usr/bin/env python
# -*- coding:utf8 -*-

from layers import *
from deepid_class import *

import cPickle
import gzip
import os
import sys
import time
import theano

import numpy as np
from common import *
from scipy.io import loadmat, savemat
from sklearn import metrics
from sklearn.externals import joblib
from joint_bayesian import *

class DeepIDGenerator:
    def __init__(self, exist_params):
        self.rng = numpy.random.RandomState(1234)
        self.exist_params = exist_params

    def layer_params(self, nkerns, batch_size):
        src_channel = 3
        self.layer1_image_shape  = (batch_size, src_channel, 55, 47)
        self.layer1_filter_shape = (nkerns[0],  src_channel, 4, 4)
        self.layer2_image_shape  = (batch_size, nkerns[0], 26, 22)
        self.layer2_filter_shape = (nkerns[1], nkerns[0], 3, 3)
        self.layer3_image_shape  = (batch_size, nkerns[1], 12, 10)
        self.layer3_filter_shape = (nkerns[2], nkerns[1], 3, 3)
        self.layer4_image_shape  = (batch_size, nkerns[2], 5, 4)
        self.layer4_filter_shape = (nkerns[3], nkerns[2], 2, 2)
        self.result_image_shape  = (batch_size, nkerns[3], 4, 3)

    def build_layer_architecture(self, n_hidden, acti_func=relu):
        '''
        simple means the deepid layer input is only the layer4 output.
        layer1: convpool layer
        layer2: convpool layer
        layer3: convpool layer
        layer4: conv layer
        deepid: hidden layer
        '''
        x = T.matrix('x')

        print '\tbuilding the model ...'
        
        layer1_input = x.reshape(self.layer1_image_shape)
        self.layer1 = LeNetConvPoolLayer(self.rng,
                input        = layer1_input,
                image_shape  = self.layer1_image_shape,
                filter_shape = self.layer1_filter_shape,
                poolsize     = (2,2),
                W = self.exist_params[5][0],
                b = self.exist_params[5][1],
                activation   = acti_func)

        self.layer2 = LeNetConvPoolLayer(self.rng,
                input        = self.layer1.output,
                image_shape  = self.layer2_image_shape,
                filter_shape = self.layer2_filter_shape,
                poolsize     = (2,2),
                W = self.exist_params[4][0],
                b = self.exist_params[4][1],
                activation   = acti_func)

        self.layer3 = LeNetConvPoolLayer(self.rng,
                input        = self.layer2.output,
                image_shape  = self.layer3_image_shape,
                filter_shape = self.layer3_filter_shape,
                poolsize     = (2,2),
                W = self.exist_params[3][0],
                b = self.exist_params[3][1],
                activation   = acti_func)

        self.layer4 = LeNetConvLayer(self.rng,
                input        = self.layer3.output,
                image_shape  = self.layer4_image_shape,
                filter_shape = self.layer4_filter_shape,
                W = self.exist_params[2][0],
                b = self.exist_params[2][1],
                activation   = acti_func)

        layer3_output_flatten = self.layer3.output.flatten(2)
        layer4_output_flatten = self.layer4.output.flatten(2)
        deepid_input = T.concatenate([layer3_output_flatten, layer4_output_flatten], axis=1)

        self.deepid_layer = HiddenLayer(self.rng,
                input = deepid_input,
                n_in  = numpy.prod( self.result_image_shape[1:] ) + numpy.prod( self.layer4_image_shape[1:] ),
                n_out = n_hidden,
                W = self.exist_params[1][0],
                b = self.exist_params[1][1],
                activation = acti_func)
    
        self.generator = theano.function(inputs=[x],
                outputs=self.deepid_layer.output)

    def generate_deepid(self, x):
        print '\tgenerating ...'
        deepid_data = self.generator(x)
        return deepid_data

def deepid_generating(dataset_path, params_file, result_folder, nkerns, n_hidden, acti_func=relu):
    if not result_folder.endswith('/'):
        result_folder += '/'
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    pd_helper = ParamDumpHelper(params_file)
    exist_params = pd_helper.get_params_from_file()
    if len(exist_params) != 0:
        exist_params = exist_params[-1]
    else:
        print 'error, no trained params'
        return
    
    data = load_data_mat(dataset_path)
    deepid = DeepIDGenerator(exist_params)
    deepid.layer_params(nkerns, data.shape[0])
    deepid.build_layer_architecture(n_hidden, acti_func)
    new_data = deepid.generate_deepid(data)
	# cPickle_output((new_x, y), result_path)
    savemat(result_folder + 'lbp_lfw_deepid.mat', {"lbp_lfw_deepid":new_data})

def load_data_mat(dataset_path):
    print 'loading data of %s' % (dataset_path)
    data  = loadmat(dataset_path)['lbp_lfw_cwh']
    # data  = data_pre(data)
    print data.shape
    return data

def cPickle_output(vars, file_name):
    print '\twriting data to %s' % (file_name)
    import cPickle
    f = open(file_name, 'wb')
    cPickle.dump(vars, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python %s dataset_path params_file result_folder' % (sys.argv[0])
        sys.exit()

    dataset_path = sys.argv[1]
    params_file    = sys.argv[2]
    result_folder  = sys.argv[3]
    nkerns  = [20,40,60,80]
    n_hidden = 160

    deepid_generating(dataset_path, params_file, result_folder, nkerns, n_hidden, acti_func=relu)
