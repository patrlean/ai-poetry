# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 14:16:46 2022

@author: 赵天佑
"""

import numpy as np

def KnnDensityEstimation( X , knn ):
    """
    X is the sample;
    knn is the number of sample
    prob = kn / N / V
    """
    
    N = np.size(X)
    distances = Distance(X)
    
    return distances

def Distance(X):
    distance = np.zeros( np.size(X) )
    Y = X
    for x in X:
        distance_y = np.array([])
        for y in Y:
            x_norm = np.linalg.norm( x - y )
            distance_y = np.append( distance_y , x_norm )
        distance = np.vstack( (distance , distance_y) )
    return np.triu( distance )     