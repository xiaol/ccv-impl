import numpy as np
import matplotlib.pyplot as plt
import theano.tensor as T

import morb
from morb import rbms, stats, updaters, trainers, monitors


plt.ion()

from videoSearch.morb.utils import generate_data, get_context

# DEBUGGING

# mode = theano.ProfileMode(optimizer='fast_run', linker=theano.gof.OpWiseCLinker())
# mode = theano.compile.DebugMode(check_py_code=False, require_matching_strides=False)
mode = None


# generate data
print ">> Generating dataset..."
data = generate_data(1000) # np.random.randint(2, size=(10000, n_visible))
data_context = get_context(data)

data_train = data[:-1000, :]
data_eval = data[-1000:, :]
data_context_train = data_context[:-1000, :]
data_context_eval = data_context[-1000:, :]

n_visible = data.shape[1]
n_context = data_context.shape[1]
n_hidden = 100


print ">> Constructing RBM..."
rbm = rbms.BinaryBinaryCRBM(n_visible, n_hidden, n_context)
initial_vmap = { rbm.v: T.matrix('v'), rbm.x: T.matrix('x') }

# try to calculate weight updates using CD-1 stats
print ">> Constructing contrastive divergence updaters..."
s = stats.cd_stats(rbm, initial_vmap, visible_units=[rbm.v], hidden_units=[rbm.h], context_units=[rbm.x], k=1)

umap = {}
for var in rbm.variables:
    pu = var + 0.0005 * updaters.CDUpdater(rbm, var, s)
    umap[var] = pu

print ">> Compiling functions..."
t = trainers.MinibatchTrainer(rbm, umap)
m = monitors.reconstruction_mse(s, rbm.v)
mce = monitors.reconstruction_crossentropy(s, rbm.v)
free_energy = T.mean(rbm.free_energy([rbm.h], s['data'])) # take the mean over the minibatch.

# train = t.compile_function(initial_vmap, mb_size=32, monitors=[m], name='train', mode=mode)
train = t.compile_function(initial_vmap, mb_size=32, monitors=[m, mce, free_energy], name='train', mode=mode)
evaluate = t.compile_function(initial_vmap, mb_size=32, monitors=[m, mce, free_energy], train=False, name='evaluate', mode=mode)

epochs = 200
print ">> Training for %d epochs..." % epochs


for epoch in range(epochs):
    costs_train = [costs for costs in train({ rbm.v: data_train, rbm.x: data_context_train })]
    costs_eval = [costs for costs in evaluate({ rbm.v: data_eval, rbm.x: data_context_eval })]
    mses_train, ces_train, fes_train = zip(*costs_train)
    mses_eval, ces_eval, fes_eval = zip(*costs_eval)
    
    mse_train = np.mean(mses_train)
    ce_train = np.mean(ces_train)
    fe_train = np.mean(fes_train)
    mse_eval = np.mean(mses_eval)
    ce_eval = np.mean(ces_eval)
    fe_eval = np.mean(fes_eval)
    
    print "Epoch %d" % epoch
    print "training set: MSE = %.6f, CE = %.6f, FE = %.2f" % (mse_train, ce_train, fe_train)
    print "validation set: MSE = %.6f, CE = %.6f, FE = %.2f" % (mse_eval, ce_eval, fe_eval)


