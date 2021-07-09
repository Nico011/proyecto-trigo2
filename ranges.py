# -*- coding: utf-8 -*-
import numpy as np
import scipy.cluster.hierarchy as hcluster
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import copy
import pandas
import os

PLOT_DIR = 'plots'



# This function uses hierarchical clustering to group a list of 
# wavelengths (integer) selected as important by the feature selection algorithms
# into a set of ranges.
# Original algorithm from:
# https://stackoverflow.com/questions/42415595/group-numbers-into-ranges-in-python
def rangos_clustering(target, selected, state, year, alg):
    # returns nothing when list is empty
    if len(selected) == 0:
        print("None")
        return []
    
    # returns one range when list has one value
    if len(selected) == 1:
        return [(selected[0], selected[0])]
    
    # create a list with every wavelength selected as a pair with itself in 
    # another list and cast it to pandas array
    # ex: selected = [350, 351, 352, ...]
    #    nselected = [[350, 350], [351, 351], [352, 352], ...]
    nselected = [[d, d] for d in selected]
    new_selected = np.array(nselected)
    
    t = (11.0/100.0) * (max(selected) - min(selected)) # threshold 11% of the total range of data
    
    # Clusters by using the euclidean distance metric, performs 
    # hierarchical clustering using the single linkage algorithm, and 
    # forms clusters using the inconsistency method with t
    # as the cut-off threshold
    # Distance criterion: forms flat clusters so that the original observations in
    # each flat cluster have no greater a cophenetic distance than t.
    # Returns: A vector of the same length as the number of ovservations, where
    # T[i] is the flat cluster number to which the original observation i belongs.
    clusters = hcluster.fclusterdata(new_selected, t, criterion = "distance")
    tot_clusters = max(clusters)
    
    # create an empty list with the same amount of lists as the clusters
    clustered_index = []
    for i in range(tot_clusters):
        clustered_index.append([])
    
    # append the index of the list (selected) to its respective cluster
    for i in range(len(clusters)):
        clustered_index[clusters[i] - 1].append(i)
    
    # Sort list in ascending order
    clustered_index = sorted(clustered_index)
    
    # print("Clusters summary:")
    # Copy list to replace index with value, and
    # print each cluster with statistics (count, mean, std, min and max)
    wavelen_clustered = copy.deepcopy(clustered_index)
    for i in range(len(clustered_index)):
        for j in range(len(clustered_index[i])):
            wavelen_clustered[i][j] = selected[clustered_index[i][j]]
        # print(f"Cluster {i+1:}")
        # aux_cluster = pandas.Series(wavelen_clustered[i])
        # statistics = [["count", aux_cluster.count()],
        #               ["mean", aux_cluster.mean()],
        #               ["median", aux_cluster.median()],
        #               ["std", aux_cluster.std()],
        #               ["min", aux_cluster.min()],
        #               ["max", aux_cluster.max()]]
        # print(f"{wavelen_clustered[i]}")
        # print(pandas.DataFrame(statistics, index = ["", "", "", "", "", ""], columns = ["", ""]))
        # print("")
        
    # create a new list, then for each list of indexes replace min and max for
    # the data value to express it as a range.
    rngs = []
    for x in clustered_index:
        clustered_index_x = [selected[y] for y in x]
        rngs.append((min(clustered_index_x), max(clustered_index_x)))
        
    
    # Boxplot of the clusters
    bp = plt.figure().gca()
    plt.boxplot(wavelen_clustered, vert = 0)
    # plt.xlim(350, 2500)
    bp.xaxis.set_major_locator(MaxNLocator(integer = True))
    plt.yticks([i + 1 for i in range(tot_clusters)], rngs)
    plt.title(f"Clusters {target}-{state}-{alg}, {year}")
    plt.savefig(os.path.join(PLOT_DIR, f"{state}-{year}-{alg}-clusters-{target}.png"))  
    plt.show()
    
    # return the sorted list of ranges
    # ex: [(350, 370), (600, 750), ...]
    return rngs

# cast resturned list of strings to integers
def string_to_int(lista):
    for i in range(len(lista)):
        lista[i] = int(lista[i])
    return lista

