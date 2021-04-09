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
    # leer csv
    datos = pandas.read_csv("data-total.csv", header=0 ,delimiter=";", encoding='ISO-8859-1')
    
    # Variable a predecir
    # target = "Chl"
    
    # filtramos los datos con las siguientes condiciones
    # Año = 2016
    # Fenologia != antesis
    # condición != secano
    # Genotipo = "QUP 2569-2009"
    
    return datos
    


def rangos_clustering(data):
    # se revisa si el parámetro viene vacío
    if len(data) == 0:
        print("No hay datos.")
        return
    
    if len(data) == 1:
        return [(data, data)]
    
    ndata = [[d, d] for d in data]
    new_data = np.array(ndata)
    
    thresh = (11.0/100.0) * (max(data) - min(data))
    
    clusters = hcluster.fclusterdata(new_data, thresh, criterion = "distance")
    tot_clusters = max(clusters)
    
    clustered_index = []
    for i in range(tot_clusters):
        clustered_index.append([])
    
    for i in range(len(clusters)):
        clustered_index[clusters[i] - 1].append(i)
        
    rngs = []
    for x in clustered_index:
        clustered_index_x = [data[y] for y in x]
        rngs.append((min(clustered_index_x), max(clustered_index_x)))
    
    return sorted(rngs)


def string_to_int(lista):
    for i in range(len(lista)):
        lista[i] = int(lista[i])
    return lista

# Inicio del programa ########################################################

def main(argv):
    target = 'Chl'
    alg = 'kbestmi'
    year = '2014'
    
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
            
    if year != 'all':
        if alg == 'boruta':
            start = time.perf_counter()
            print("Extracting data...")
            data = datos()
            control, secano = data_preprocessing.data_any_year(target, data, int(year))
            print("Running Boruta Algorithm...")
            elegidos_control = my_boruta.my_boruta_init(target, control)
            elegidos_secano = my_boruta.my_boruta_init(target, secano)
            rangos_control = rangos_clustering(elegidos_control)
            rangos_secano= rangos_clustering(elegidos_secano)
            print(f"Year {year}:")
            print(f"Selected wavelength ranges (control set): {rangos_control}")
            print(f"Selected wavelength ranges (dry set): {rangos_secano}")
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestcorr':
            start = time.perf_counter()
            print("Extracting data...")
            data = datos ()
            control, secano = data_preprocessing.data_any_year(target, data, int(year))
            print("Running SelectK-Best (Correlation)...")
            elegidos_control = kbest.kbest_corr(target, control)
            elegidos_secano = kbest.kbest_corr(target, secano)
            rangos_control = rangos_clustering(elegidos_control)
            rangos_secano = rangos_clustering(elegidos_secano)
            print(f"Year {year}:")
            print(f"Selected wavelength ranges (control set): {rangos_control}")
            print(f"Selected wavelength ranges (dry set): {rangos_secano}")
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestmi':
            start = time.perf_counter()
            print("Extracting data...")
            data = datos ()
            control, secano = data_preprocessing.data_any_year(target, data, int(year))
            print("Running SelectK-Best (Mutual Information)...")
            elegidos_control = kbest.kbest_mi(target, control)
            elegidos_secano = kbest.kbest_mi(target, secano)
            rangos_control = rangos_clustering(elegidos_control)
            rangos_secano = rangos_clustering(elegidos_secano)
            print(f"Year {year}:")
            print(f"Selected wavelength ranges (control set): {rangos_control}")
            print(f"Selected wavelength ranges (dry set): {rangos_secano}")
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
    
    

if __name__ == "__main__":
    main(sys.argv[1:])




# print("Seleccione el algoritmo de selección de atributos que desea ejecutar: ")
# print("1:\tBoruta.")
# print("2:\tLasso.")
# print("3:\tSelectK-Best (Mutual Information).")
# print("4:\tSelectK-Best (Correlation).")
# print("5:\tGenetic Algorithm.")
# print("6:\tTodos los anteriores.")
# print("7:\tSalir.")

# op = input("Introduzca opción: ")

# print("Variable objetivo:", target)

# while 1:
#     if op == '1':
#         start = time.perf_counter()
#         #boruta()
#         elegidos = my_boruta.my_boruta_init(target, firma_control_2014, control_2014)
#         print(rangos_clustering(elegidos))
#         end = time.perf_counter()
#         print(f"Tiempo de ejecución: {end - start:0.2f} segundos.")
    
#     elif op == '2':
#         start = time.perf_counter()
#         #lasso()
#         elegidos = my_lasso.my_lasso_init(target, firma_control_2014, control_2014, cols)
#         print(rangos_clustering(elegidos))
#         end = time.perf_counter()
#         print(f"Tiempo de ejecución: {end - start:0.2f} segundos.")
        
#     elif op == '3':
#         start = time.perf_counter()
#         elegidos = my_kbest.kbest_mi(target, firma_control_2014, control_2014)
#         print(rangos_clustering(elegidos))
#         end = time.perf_counter()
#         print(f"Tiempo de ejecución: {end - start:0.2f} segundos.")
    
#     elif op == '4':
#         start = time.perf_counter()
#         elegidos = my_kbest.kbest_corr(target, firma_control_2014, control_2014)
#         print(rangos_clustering(elegidos))
#         end = time.perf_counter()
#         print(f"Tiempo de ejecución: {end - start:0.2f} segundos.")
        
#     elif op == '5':
#         start = time.perf_counter()
#         #ga()
#         end = time.perf_counter()
#         print(f"Tiempo de ejecución: {end - start:0.2f} segundos.")
        
#     elif op == '6':
#         start = time.perf_counter()
#         #boruta()
#         #lasso()
#         #kbest_mi()
#         #kbest_corr()
#         end = time.perf_counter()
#         print(f'Tiempo de ejecución: {end - start:0.2f} segundos.')
        
#     elif op == '7':
#         print("Fin del programa.")
#         break
        
#     else:
#         print("Opción no válida, intente nuevamente.")
    
#     print()
#     print("Seleccione el algoritmo de selección de atributos que desea ejecutar: ")
#     print("1:\tBoruta.")
#     print("2:\tLasso.")
#     print("3:\tSelectK-Best (Mutual Information).")
#     print("4:\tSelectK-Best (Correlation).")
#     print("5:\tGenetic Algorithm.")
#     print("6:\tTodos los anteriores.")
#     print("7:\tSalir.")
#     op = input("Introduzca opción: ")
















