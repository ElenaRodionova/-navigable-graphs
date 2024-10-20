
import sys
import numpy as np
import time
import random
from math import log2
from heapq import heapify, heappop, heappush, heapreplace, nlargest, nsmallest
import argparse
from tqdm import tqdm
from heapq import heappush, heappop
import random
import itertools
random.seed(108)

class Graph(object):
    
    def __init__(self, k, dist_func, data, M):
        self.k = k
        self.distance_func = dist_func
        self.data = data
        self.M = M

        print('Building Graph')
        self.edges = [] # рёбра графа
        
        for x_id, x_coord in tqdm(enumerate(self.data)):
            other_points = sorted(enumerate(self._vectorized_distance(x_coord, self.data)), key=lambda a: a[1])[1:200]
            for i in range(1, k):
                self.edges.append([other_points[i]])

            for y_id, y_dist in other_points[2:]:
                if y_dist < min([self.distance_func(data[y_id], data[x_neighbor[0]]) for x_neighbor in self.edges[x_id]]):
                    self.edges[x_id].append((y_id, y_dist))

    
    def beam_search(self, q, k, eps, ef, ax=None, marker_size=20, return_observed=False):
        '''
        q - query
        k - number of closest neighbors to return
        eps – entry points [vertex_id, ..., vertex_id]
        ef – size of the beam
        observed – if True returns the full of elements for which the distance were calculated
        returns – a list of tuples [(vertex_id, distance), ... , ]
        '''
        # Priority queue: (negative distance, vertex_id)
        candidates = []
        visited = set()  # set of vertex used for extending the set of candidates
        observed = dict() # dict: vertex_id -> float – set of vertexes for which the distance were calculated

        if ax:
            ax.scatter(x=q[0], y=q[1], s=marker_size, color='red', marker='^')
            ax.annotate('query', (q[0], q[1]))

        # Initialize the queue with the entry points
        for ep in eps:
            dist = self.distance_func(q, self.data[ep])
            heappush(candidates, (dist, ep))
            observed[ep] = dist

        while candidates:
            # Get the closest vertex (furthest in the max-heap sense)
            dist, current_vertex = heappop(candidates)

            if ax:
                ax.scatter(x=self.data[current_vertex][0], y=self.data[current_vertex][1], s=marker_size, color='red')
                ax.annotate( len(visited), self.data[current_vertex] )

            # check stop conditions #####
            observed_sorted = sorted( observed.items(), key=lambda a: a[1] )
            # print(observed_sorted)
            ef_largets = observed_sorted[ min(len(observed)-1, ef-1 ) ]
            # print(ef_largets[0], '<->', -dist)
            if ef_largets[1] < dist:
                break
            #############################

            # Add current_vertex to visited set
            visited.add(current_vertex)

            # Check the neighbors of the current vertex
            for neighbor, _ in self.edges[current_vertex]:
                if neighbor not in observed:
                    dist = self.distance_func(q, self.data[neighbor])
                    heappush(candidates, (dist, neighbor))
                    observed[neighbor] = dist
                    if ax:
                        ax.scatter(x=self.data[neighbor][0], y=self.data[neighbor][1], s=marker_size, color='yellow')
                        # ax.annotate(len(visited), (self.data[neighbor][0], self.data[neighbor][1]))
                        ax.annotate(len(visited), self.data[neighbor])

        # Sort the results by distance and return top-k
        observed_sorted =sorted( observed.items(), key=lambda a: a[1] )
        if return_observed:
            return observed_sorted
        return observed_sorted[:k]

    def l2_distance(a, b):
        return np.linalg.norm(a - b)
   
    def _vectorized_distance(self, x, ys):
        return [self.distance_func(x, y) for y in ys]

    def brute_force_knn_search(self, k, x):
        '''
        Return the list of (idx, dist) for k-closest elements to {x} in {data}
        '''
        return sorted(enumerate(self._vectorized_distance(x, self.data)), key=lambda a: a[1])[:k]


def _calculate_recall(kg, test, groundtruth, k, ef, m):
    if groundtruth is None:
        print("Ground truth not found. Calculating ground truth...")
        groundtruth = [ [idx for idx, dist in kg.brute_force_knn_search(k, query)] for query in tqdm(test)]

    print("Calculating recall...")
    recalls = []
    total_calc = 0
    for query, true_neighbors in tqdm(zip(test, groundtruth), total=len(test)):
        true_neighbors = true_neighbors[:k]  # Use only the top k ground truth neighbors
        entry_points = random.sample(range(len(kg.data)), m)
        observed = [neighbor for neighbor, dist in kg.beam_search(query, k, entry_points, ef, return_observed = True)]
        total_calc = total_calc + len(observed)
        results = observed[:k]
        intersection = len(set(true_neighbors).intersection(set(results)))
        # print(f'true_neighbors: {true_neighbors}, results: {results}. Intersection: {intersection}')
        recall = intersection / k
        recalls.append(recall)

    return np.mean(recalls), total_calc/len(test)