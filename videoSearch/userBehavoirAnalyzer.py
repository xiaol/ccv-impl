__author__ = 'Ivan liu'

from morb import base, units, parameters, stats, updaters, trainers, monitors
import numpy
import theano.tensor as T


def main():
    ## define hyperparameters
    learning_rate = 0.01
    weight_decay = 0.02
    minibatch_size = 32
    epochs = 50

    ## load dataset
    data = numpy.array([[1,1,1,0,0,0],[1,0,1,0,0,0],[1,1,1,0,0,0],[0,0,1,1,1,0], [0,0,1,1,0,0],[0,0,1,1,1,0]]) # A 6x6 matrix where each row is a training example and each column is a visible unit.

    ## construct RBM model
    rbm = base.RBM()

    rbm.v = units.BinaryUnits(rbm) # visibles
    rbm.h = units.BinaryUnits(rbm) # hiddens

    initial_W = []
    initial_bv = []
    initial_bh = []

    rbm.W = parameters.ProdParameters(rbm, [rbm.v, rbm.h], initial_W) # weights
    rbm.bv = parameters.BiasParameters(rbm, rbm.v, initial_bv) # visible bias
    rbm.bh = parameters.BiasParameters(rbm, rbm.h, initial_bh) # hidden bias

    ## define a variable map, that maps the 'input' units to Theano variables.
    initial_vmap = { rbm.v: T.matrix('v') }

    ## compute symbolic CD-1 statistics
    s = stats.cd_stats(rbm, initial_vmap, visible_units=[rbm.v], hidden_units=[rbm.h], k=1)

    ## create an updater for each parameter variable
    decay = 0.7 #TODO decay?
    umap = {}
    for variable in [rbm.W.W, rbm.bv.b, rbm.bh.b]:
        new_value = variable + learning_rate * (updaters.CDUpdater(rbm, variable, s) - decay * updaters.DecayUpdater(variable))
        umap[variable] = new_value

    ## monitor reconstruction cost during training
    mse = monitors.reconstruction_mse(s, rbm.v)

    ## train the model
    t = trainers.MinibatchTrainer(rbm, umap)
    train = t.compile_function(initial_vmap, mb_size=minibatch_size, monitors=[mse])

    for epoch in range(epochs):
        costs = [m for m in train({ rbm.v: data })]
        print "MSE = %.4f" % numpy.mean(costs)

if __name__ == '__main__':
    main()


