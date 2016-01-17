#!/usr/bin/env python

import random
import operator
import matplotlib.pyplot as plt

class DataPoint(object):
    def __init__(self, args):
        self.components = tuple(args)
        
    def __getitem__(self, i):
        if i >= len(self.components):
            raise IndexError("DataPoint out of range")
        else:
            return self.components[i]
            
    def __len__(self):
        return len(self.components)
        
    def __iter__(self):
        return iter(self.components)
        
    def __repr__(self):
        return "<DataPoint({})>".format(', '.join("x{0}={1}".format(i, c) for i, c in enumerate(self.components)))
        
    def distance_to(self, other):
            return sum((x-y)**2 for x,y in zip(self, other))**0.5
            
    def as_tuple(self):
        return tuple(self.components)
        
    @staticmethod
    def random_points(n, dimension=2, max_val=1000):
        return [DataPoint(random.sample(xrange(max_val), dimension)) for _ in xrange(n)]
   



   
class Cluster(object):
    def __init__(self, args):
        self.points = tuple(args)
        self.centroid = Cluster.compute_centroid(args)
        
        
    def __getitem__(self, i):
        if i >= len(self.points):
            raise IndexError("Cluster out of range")
        else:
            return self.points[i]
            
    def __len__(self):
        return len(self.points)
        
    def __iter__(self):
        return iter(self.points)
        
    def __repr__(self):
        return "<Cluster({}) centered at {}>".format(self.points, self.centroid)
        
    def insert(self, point):
        self.points.append(point)
        
    def update(self, points):
        self.points = points
        self.centroid = Cluster.compute_centroid(points)
        
    def get_centroid(self):
        return self.centroid
        
    def as_tuple(self):
        return tuple(self.points)
        
    @staticmethod
    def compute_centroid(data_points):
        
        num_components = len(data_points[0])
        components = (sum(point[i] for point in data_points)/len(data_points)  for i in xrange(num_components))
        return DataPoint(components)   
    


def kmeans(points, k, dimension=2, cutoff=10):
    centroids = DataPoint.random_points(k,  dimension)
    
    clusters = [Cluster([p]) for p in centroids]
    
    loop_counter = 0
    done = False
    while not done:
        lists = [[p] for p in centroids]
        delta = 0.0
        
        for point in points:
            distances = map(point.distance_to, centroids)
            #print distances
            min_index, min_val = min(enumerate(distances), key=operator.itemgetter(1))
            
            lists[min_index].append(point)
        
        for i in xrange(k):
            clusters[i].update(lists[i])
            
        delta = sum(cluster.get_centroid().distance_to(centroid) for cluster, centroid in zip(clusters, centroids))
        #print delta
        if delta < cutoff:
            done = True
            
        centroids = [cluster.get_centroid() for cluster in clusters]
        loop_counter += 1
    return (clusters, loop_counter)
    

def main():
    points = DataPoint.random_points(200)

    clusters, niters = kmeans(points, 4)
    
    for color, cluster in zip(['b','g','r','c'], clusters):
        plt.plot([point[0] for point in cluster], [point[1] for point in cluster], color=color, marker='+', ls='.')
        plt.plot(cluster.get_centroid()[0], cluster.get_centroid()[1], color=color, marker='o', ls='.')
        

    #print clusters
    plt.show()
    print niters
    
if __name__ == '__main__':
    main()

#print compute_centroid(points)

#p1 = DataPoint((1,2))
#p2 = DataPoint((1,2))
#print p1.distance_to(p2)
#print p2.distance_to(p1)
