# -*- coding: utf-8 -*-
import time
import pandas
import sys
import getopt
import numpy as np
from sklearn.preprocessing import StandardScaler

import scipy.cluster.hierarchy as hcluster

import data_preprocessing
import my_boruta
import lasso
import kbest
import ga


def datos():
    # Read csv
    datos = pandas.read_csv("data-total.csv", header=0 ,delimiter=";", encoding='ISO-8859-1')
    
   
    # possible filters:
    # Fenologia != antesis
    # condición != secano
    # Genotipo = "QUP 2569-2009"
    
    return datos
    

# This function uses hierarchical clustering to group a list of 
# wavelength (integer) into a set of ranges.
def rangos_clustering(data):
    # returns nothing when list is empty
    if len(data) == 0:
        print("No hay datos.")
        return
    
    # returns one range when list has one value
    if len(data) == 1:
        return [(data, data)]
    
    
    ndata = [[d, d] for d in data]
    new_data = np.array(ndata)
    
    t = (11.0/100.0) * (max(data) - min(data)) # threshold 11% of the total range of data
    
    # Clusters by using the euclidean distance metric, performs 
    # hierarchical clustering using the single linkage algorithm, and 
    # forms clusters using the inconsistency method with t
    # as the cut-off threshold
    # Distance criterion: forms flat clusters so that the original observations in
    # each flat cluster have no greater a cophenetic distance than t.
    # Returns: A vector of the same length as the number of ovservations, where
    # T[i] is the flat cluster number to which the original observation i belongs.
    clusters = hcluster.fclusterdata(new_data, t, criterion = "distance")
    tot_clusters = max(clusters)
    
    # create an empty list with the same amount of lists as the clusters
    clustered_index = []
    for i in range(tot_clusters):
        clustered_index.append([])
    
    # append the index of the cluster to its respectvie list
    for i in range(len(clusters)):
        clustered_index[clusters[i] - 1].append(i)
        
    # create a new list, then for each list of indexes replace min and max for
    # the data value to express it as a range.
    rngs = []
    for x in clustered_index:
        clustered_index_x = [data[y] for y in x]
        rngs.append((min(clustered_index_x), max(clustered_index_x)))
    
    # return the sorted list of ranges
    return sorted(rngs)

# cast resturned list of strings to integers
def string_to_int(lista):
    for i in range(len(lista)):
        lista[i] = int(lista[i])
    return lista


def run_boruta(target, year, data):
    control, secano = data_preprocessing.data_any_year(target, data, int(year))
    print("Running Boruta Algorithm...")
    elegidos_control = my_boruta.my_boruta_init(target, control)
    elegidos_secano = my_boruta.my_boruta_init(target, secano)
    rangos_control = rangos_clustering(elegidos_control)
    rangos_secano= rangos_clustering(elegidos_secano)
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print(f"Selected wavelength ranges (dry land set): {rangos_secano}")
    return

def run_lasso(target, year, data):
    control, secano = data_preprocessing.data_any_year(target, data, int(year))
    print("Running LASSO...")
    elegidos_control = lasso.lasso_init(target, control)
    elegidos_secano = lasso.lasso_init(target, secano)
    rangos_control = rangos_clustering(elegidos_control)
    rangos_secano = rangos_clustering(elegidos_secano)
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print(f"Selected wavelength ranges (dry land set): {rangos_secano}")
    return

def run_kbest_corr(target, year, data):
    control, secano = data_preprocessing.data_any_year(target, data, int(year))
    print("Running SelectK-Best (Correlation)...")
    elegidos_control = kbest.kbest_corr(target, control)
    elegidos_secano = kbest.kbest_corr(target, secano)
    rangos_control = rangos_clustering(elegidos_control)
    rangos_secano = rangos_clustering(elegidos_secano)
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print(f"Selected wavelength ranges (dry land set): {rangos_secano}")
    return

def run_kbest_mi(target, year, data):
    control, secano = data_preprocessing.data_any_year(target, data, int(year))
    print("Running SelectK-Best (Mutual Information)...")
    elegidos_control = kbest.kbest_mi(target, control)
    elegidos_secano = kbest.kbest_mi(target, secano)
    rangos_control = rangos_clustering(elegidos_control)
    rangos_secano = rangos_clustering(elegidos_secano)
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print(f"Selected wavelength ranges (dry land set): {rangos_secano}")
    return

def main(argv):
    # default values for line commands
    years_default = [2014, 2015, 2016, 2017]
    target = 'Chl'
    alg = 'all'
    year = 'all'
    
    try:
        opts, arg = getopt.getopt(argv, "ht:a:y:", ["target=", "algorithm=", "year="])
    except getopt.GetoptError:
        print("my_main.py -t <target> -a <algorithm> -y <year>")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print("my_main.py -t <target> -a <algorithm> -y <year>")
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-a", "--algorithm"):
            alg = arg 
        elif opt in ("-y", "--year"):
            year = arg
            
    print(f"Target: {target}")
            
    if year != 'all' and alg != 'all':
        if alg == 'boruta':
            start = time.perf_counter()
            print(f"Year {year}:")
            print("Extracting data...")
            data = datos ()
            run_boruta(target, year, data)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'lasso':
            start = time.perf_counter()
            print(f"Year {year}:")
            print("Extracting data...")
            data = datos ()
            run_lasso(target, year, data)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestcorr':
            start = time.perf_counter()
            print(f"Year {year}:")
            print("Extracting data...")
            data = datos ()
            run_kbest_corr(target, year, data)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestmi':
            start = time.perf_counter()
            print(f"Year {year}:")
            print("Extracting data...")
            data = datos ()
            run_kbest_mi(target, year, data)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
    else:
        start = time.perf_counter()
        for i in range(len(years_default)):
            print(f"Year {years_default[i]}")
            print("Extracting data...")
            data = datos()
            run_kbest_corr(target, years_default[i], data)
            print()
            run_kbest_mi(target, years_default[i], data)
            print()
            run_boruta(target, years_default[i], data)
            print()
            run_lasso(target, years_default[i], data)
            print()
        end = time.perf_counter()
        print(f"Execution time: {end - start:0.2f} seconds.")

if __name__ == "__main__":
    main(sys.argv[1:])










