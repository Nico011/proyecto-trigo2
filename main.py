# -*- coding: utf-8 -*-
# This function hides warning messages (from lasso algorithm)
# https://stackoverflow.com/questions/32612180/eliminating-warnings-from-scikit-learn
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import time
import pandas
import sys
import getopt
import numpy as np
import io
import requests
import copy
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from sklearn.preprocessing import StandardScaler

import scipy.cluster.hierarchy as hcluster

import data_preprocessing
import my_boruta
import lasso
import kbest
import ga

# This function uses hierarchical clustering to group a list of 
# wavelengths (integer) selected as important by the feature selection algorithms
# into a set of ranges.
# Original algorithm from:
# https://stackoverflow.com/questions/42415595/group-numbers-into-ranges-in-python
def rangos_clustering(selected, state, year, alg):
    # returns nothing when list is empty
    if len(selected) == 0:
        print("None")
        return
    
    # returns one range when list has one value
    if len(selected) == 1:
        return [(selected, selected)]
    
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
    # print(f"clustered_index2: {clustered_index}")
    
    print("Clusters summary:")
    # Copy list to replace index with value, and
    # print each cluster with statistics (count, mean, std, min and max)
    wavelen_clustered = copy.deepcopy(clustered_index)
    for i in range(len(clustered_index)):
        for j in range(len(clustered_index[i])):
            wavelen_clustered[i][j] = selected[clustered_index[i][j]]
        print(f"Cluster {i+1:}")
        print(f"{wavelen_clustered[i]}")
        print(f"{pandas.Series(wavelen_clustered[i]).describe()[['count', 'mean', 'std', 'min', 'max']]}")
    
    # Boxplot of the clusters
    bp = plt.figure().gca()
    plt.boxplot(wavelen_clustered, vert = 0)
    bp.xaxis.set_major_locator(MaxNLocator(integer = True))
    plt.title(f"Boxplot {state}, {year}")
    plt.savefig(f"{alg}-{state}-{year}.png")  
        
    # create a new list, then for each list of indexes replace min and max for
    # the data value to express it as a range.
    rngs = []
    for x in clustered_index:
        clustered_index_x = [selected[y] for y in x]
        rngs.append((min(clustered_index_x), max(clustered_index_x)))
    
    # return the sorted list of ranges
    # ex: [(350, 370), (600, 750), ...]
    return rngs

# cast resturned list of strings to integers
def string_to_int(lista):
    for i in range(len(lista)):
        lista[i] = int(lista[i])
    return lista


# The following functions run each algorithm available and prints their results.
# They all work about the same. They receive as parameters the target (string),
# and the filtered dataset separated as control and water stress.
# They print the name of the algorithm,
# wavelength selected as important by the algorithm, and
# wavelength selected as important in range format.
def run_boruta(target, control, secano, year):
    print("Running Boruta Algorithm...")
    elegidos_control = my_boruta.my_boruta_init(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = rangos_clustering(elegidos_control, "control", year, "boruta")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_secano = my_boruta.my_boruta_init(target, secano)
    print(f"Selected water stress: {len(elegidos_secano)} wavelength(s)\n{elegidos_secano}")
    rangos_secano= rangos_clustering(elegidos_secano, "water stress", year, "boruta")
    print(f"Selected wavelength ranges (water stress set): {rangos_secano}")
    return

def run_lasso(target, control, secano, year):
    print("Running LASSO...")
    elegidos_control = lasso.lasso_init(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = rangos_clustering(elegidos_control, "control", year, "lasso")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_secano = lasso.lasso_init(target, secano)
    print(f"Selected water stress: {len(elegidos_secano)} wavelength(s)\n{elegidos_secano}")
    rangos_secano = rangos_clustering(elegidos_secano, "water stress", year, "lasso")
    print(f"Selected wavelength ranges (water stress set): {rangos_secano}")
    return

def run_kbest_corr(target, control, secano, year):
    print("Running SelectK-Best (Correlation)...")
    elegidos_control = kbest.kbest_corr(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = rangos_clustering(elegidos_control, "control", year, "kbestcorr")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_secano = kbest.kbest_corr(target, secano)
    print(f"Selected water stress: {len(elegidos_secano)} wavelength(s)\n{elegidos_secano}")
    rangos_secano = rangos_clustering(elegidos_secano, "water stress", year, "kbestcorr")
    print(f"Selected wavelength ranges (water stress set): {rangos_secano}")
    return

def run_kbest_mi(target, control, secano, year):
    print("Running SelectK-Best (Mutual Information)...")
    elegidos_control = kbest.kbest_mi(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = rangos_clustering(elegidos_control, "control", year, "kbestmi")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_secano = kbest.kbest_mi(target, secano)
    print(f"Selected water stress: {len(elegidos_secano)} wavelength(s)\n{elegidos_secano}")
    rangos_secano = rangos_clustering(elegidos_secano, "water stress", year, "kbestmi")
    print(f"Selected wavelength ranges (water stress set): {rangos_secano}")
    return

def run_ga(target, control, secano, year):
    print("Running Genetic Algorithm...")
    elegidos_control = ga.ga(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = rangos_clustering(elegidos_control, "control", year, "ga")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_secano = ga.ga(target, secano)
    print(f"Selected water stress: {len(elegidos_secano)} wavelength(s)\n{elegidos_secano}")
    rangos_secano = rangos_clustering(elegidos_secano, "water stress", year, "ga")
    print(f"Selected wavelength ranges (water stress set): {rangos_secano}")
    return


# Main function
def main(argv):
    # default values for line commands
    years_default = [2014, 2015, 2016, 2017]
    target = 'Chl'
    alg = 'all'
    year = 'all'
    
    str_help = """Usage:
main.py -t <target> [-a <algorithm> -y <year>]

-t, --target    : Give a specific target (Deafault: Chl).
-a, --algorithm : Give a specific feature selection algorithm (Optional, default: all).
-y, --year      : Give a specific year (Optional, default: all).

Targets available: Chl, Flav, Anth, NBI, Pot.Hoja(Bar), Transmitted, 
                   LAI, EVAP, GS, PN, CI, VPD.

Algorithms available: 
    boruta     : Run Boruta feature selection algorithm.
    lasso      : Run LASSO feature selection algorithm.
    kbestcorr  : Run SelectkBest using the correlation ranking.
    kbestmi    : Run SelectkBest using mutual information ranking.
    ga         : Run Genetic Algorithm for feature selection.

Years available: 2014, 2015, 2016 and 2017."""

    try:
        opts, arg = getopt.getopt(argv, "ht:a:y:", ["target=", "algorithm=", "year="])
    except getopt.GetoptError as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(str_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(str_help)
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-a", "--algorithm"):
            alg = arg 
        elif opt in ("-y", "--year"):
            year = arg
            
    print(f"Target: {target}")
    print("")
   
            
    if year != 'all' and alg != 'all': 
        
        print(f"Year {year}\n:")
        print("Extracting data...")
        control, secano = data_preprocessing.data_any_year(target, int(year))
        
        if alg == 'boruta':
            start = time.perf_counter()
            run_boruta(target, control, secano, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'lasso':
            start = time.perf_counter()
            run_lasso(target, control, secano, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestcorr':
            start = time.perf_counter()
            run_kbest_corr(target, control, secano, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestmi':
            start = time.perf_counter()
            run_kbest_mi(target, control, secano, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'ga':
            start = time.perf_counter()
            run_ga(target, control, secano, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
    else:
        print("Extracting data...")
        time_total = 0
        for i in range(len(years_default)):
            print(f"\nYear: {years_default[i]}\n")
            control, secano = data_preprocessing.data_any_year(target, years_default[i])
            start = time.perf_counter()
            run_kbest_corr(target, control, secano, years_default[i])
            print("")
            run_kbest_mi(target, control, secano, years_default[i])
            print("")
            run_boruta(target, control, secano, years_default[i])
            print("")
            run_lasso(target, control, secano, years_default[i])
            print("")
            # run_ga(target, control, secano, years_default[i])
            end = time.perf_counter()
            time_total = time_total + (end - start)
        print(f"Execution time: {time_total:0.2f} seconds.")
    
    print(f"Boxplot graphs saved as image in current working directory ({os.getcwd()})")

if __name__ == "__main__":
    main(sys.argv[1:])










