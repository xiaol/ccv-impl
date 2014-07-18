#coding= utf-8

import caffe
caffe_root = '../'  # this file is expected to be in {caffe_root}/examples

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = 'imagenet/imagenet_deploy.prototxt'
PRETRAINED = 'imagenet/caffe_reference_imagenet_model'
IMAGE_FILE = 'images/cat.jpg'


net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean_file=caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy',
                       channel_swap=(2,1,0),
                       input_scale=255)

net.set_phase_test()
net.set_mode_cpu()
