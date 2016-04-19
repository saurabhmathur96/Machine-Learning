#!/usr/bin/env python

from numpy import asarray, array, array_str, exp, square, sqrt, uint8, vectorize, zeros
from numpy.random import rand, seed
from operator import itemgetter
from PIL import Image
import random


class Node(object):

    def __init__(self, x, y, n_weights):
        self.x = x
        self.y = y
        self.weights = zeros(n_weights)

    def weight_distance_to(self, target):
        return square(self.weights - target).sum()

    def distance_to(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def adjust_weights(self, target, learning_rate, influence):
        delta_weights = learning_rate * influence * (target - self.weights)
        self.weights += delta_weights

    def __str__(self):
        return 'Node{0}'.format(array_str(self.weights, precision=2))


class SelfOrganizingMap(object):

    def __init__(self, n_rows, n_columns, n_weights=3):
        self.nodes = [[Node(x=i, y=j, n_weights=3) for j in range(n_columns)]
                            for i in range(n_rows)]
        self.radius = max(n_rows, n_columns) / 2

    def find_best_matching_node(self, target):
        node_distance_pairs = ((node, node.weight_distance_to(target))
                               for row in self.nodes for node in row)
        closest_node = min(node_distance_pairs, key=itemgetter(1))[0]
        return closest_node

    def train(self, data, n_iterations=100, initial_learning_rate=0.5):
        learning_rate = initial_learning_rate
        for iteration_index in range(n_iterations):
            target = random.choice(data)
            winner = self.find_best_matching_node(target)
            neighbourhood_radius = self.radius * \
                exp(-float(iteration_index) / n_iterations)
            for i, row in enumerate(self.nodes):
                for j, node in enumerate(row):
                    distance_to_winner = self.nodes[i][j].distance_to(winner)
                    if distance_to_winner < neighbourhood_radius:
                        influence = exp(
                            float(
                                distance_to_winner ** 2) / (
                                    2 * neighbourhood_radius ** 2))
                        self.nodes[i][j].adjust_weights(
                            target, learning_rate, influence)
            learning_rate = initial_learning_rate * \
                exp(-float(iteration_index) / n_iterations)
                
    def __str__(self):
        return '\n'.join(' '.join(str(node) for node in row) for row in self.nodes)


if __name__ == '__main__':
    seed(0)
    import sys
    ## Shape of SOM is mxn
    m = 4
    n = 3
    som = SelfOrganizingMap(m, n, 3)
    print('==== Before Training ===')
    image = Image.open(sys.argv[1])
    pixels = asarray(image)
    print ('image:' + str(pixels.shape))
    if len(pixels.shape) > 2:
        pixel_data = pixels.reshape(pixels.shape[0]*pixels.shape[1], pixels.shape[2])
    else :
        pixel_data = pixels.reshape(pixels.shape[0]*pixels.shape[1])
    print('==== Training Started ===')
    som.train(pixel_data, 4000)
    print('==== Training Complete ===')
    print som
