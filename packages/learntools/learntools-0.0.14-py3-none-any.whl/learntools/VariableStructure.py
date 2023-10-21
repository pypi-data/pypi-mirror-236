from turtle import st
from learntools import Network, Learning
import numpy as np

def VariableStructure(n_in:int, n_out: int, loss_fun, epochs: int, max_its: int, max_mutations: int, depth_add_prob: float, act_layer, threshold = 1e-3, info = False): #max_mutations should be max pertubations?
    net = Network.network(n_in, n_out)
    net.add_layer(Network.layer_dense(n_in,n_out))

    net.random_initilisation()

    total_loss = []

    for epoch in range(epochs): #go through the epochs

        loss, (its, total_mutations) = Learning.random_learning(net,loss_fun,max_its,max_mutations,threshold=threshold, info=info)
        total_loss += loss
        if info == True:
            print(f'Epoch-{epoch}-loss-{total_loss[-1]}')
        if total_loss[-1] < threshold:
            break

        rem_its = max_its - its
        mutation_prob = rem_its / max_its
        print(mutation_prob)
        if np.random.uniform(0,1) < mutation_prob:
            # change the structure

            if np.random.uniform(0,1) < depth_add_prob or len(net.mutateable_layers) == 1: # add layer

                net.add_layer(act_layer())
                net.add_layer(Network.layer_dense(net.n_out,net.n_out))
                net.layers[-1].weights += 1 / net.n_out
            else:
                layers = net.layers[:]
                mutate_loc = np.random.choice(list(range(len(net.mutateable_layers[:-1])))) #exclude last one as we edit n_out
                mutate_index = net.mutateable_layers[mutate_loc]

                old_layer = layers[mutate_index]
                new_layer = Network.layer_dense(old_layer.n_in,old_layer.n_out + 1)
                new_layer.weights[:old_layer.weights.shape[0],:old_layer.weights.shape[1]] = old_layer.weights
                new_layer.biases[:old_layer.biases.shape[0]] = old_layer.biases
                layers[mutate_index] = new_layer

                mutate_index = net.mutateable_layers[mutate_loc+1]
                old_layer = layers[mutate_index]
                new_layer = Network.layer_dense(old_layer.n_in+1,old_layer.n_out)
                new_layer.weights[:old_layer.weights.shape[0],:old_layer.weights.shape[1]] = old_layer.weights
                new_layer.biases[:old_layer.biases.shape[0]] = old_layer.biases
                layers[mutate_index] = new_layer

                net.layers = layers

            if net.check_integrity() == False:
                raise Exception("Failed Integrity")
            
    return net, total_loss