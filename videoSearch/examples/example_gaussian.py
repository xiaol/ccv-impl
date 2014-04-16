import time

import numpy as np
import matplotlib.pyplot as plt
import theano.tensor as T

import morb
from morb import rbms, stats, updaters, trainers, monitors, units, parameters

plt.ion()

from videoSearch.morb.utils import generate_data


# DEBUGGING

# mode = theano.ProfileMode(optimizer='fast_run', linker=theano.gof.OpWiseCLinker())
# mode = theano.compile.DebugMode(check_py_code=False, require_matching_strides=False)
mode = None

# generate data
data = generate_data(200)

# use the predefined binary-binary RBM, which has visible units (rbm.v), hidden units (rbm.h),
# a weight matrix W connecting them (rbm.W), and visible and hidden biases (rbm.bv and rbm.bh).
n_visible = data.shape[1]
n_hidden = 100

rbm = rbms.GaussianBinaryRBM(n_visible, n_hidden)

initial_vmap = { rbm.v: T.matrix('v') }

# We use single-step contrastive divergence (CD-1) to train the RBM. For this, we can use
# the CDParamUpdater. This requires symbolic CD-1 statistics:
s = stats.cd_stats(rbm, initial_vmap, visible_units=[rbm.v], hidden_units=[rbm.h], k=1)

# We create an updater for each parameter variable
umap = {}
for var in rbm.variables:
    pu =  var + 0.001 * updaters.CDUpdater(rbm, var, s) # the learning rate is 0.001
    umap[var] = pu
 
# training
t = trainers.MinibatchTrainer(rbm, umap)
mse = monitors.reconstruction_mse(s, rbm.v)
train = t.compile_function(initial_vmap, mb_size=32, monitors=[mse], name='train', mode=mode)

epochs = 200

start_time = time.time()
for epoch in range(epochs):
    print "Epoch %d" % epoch
    costs = [m for m in train({ rbm.v: data })]
    print "MSE = %.4f" % np.mean(costs)

print "Took %.2f seconds" % (time.time() - start_time)
