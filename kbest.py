# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import mutual_info_regression
import matplotlib.pyplot as plt
import pandas
import math
import numpy as np


def calcular_75_sup(lista_importancia):
    #lista_importancia.describe()
    mediana = (np.max(lista_importancia.scores_)) / 2
    # print("max: " + str(np.max(lista_importancia.scores_)))
    # print("mediana: " + str(mediana))
    val_75_sup = mediana + (mediana * 0.5)
    # print("75%: " + str(val_75_sup))
    lista_75_sup = []
    for i in range(len(lista_importancia.scores_)):
        if lista_importancia.scores_[i] >= val_75_sup:
            lista_75_sup.append(i)
    return lista_75_sup


def kbest_corr(target, dataset):
    
    # get signature columns
    firma = dataset.loc[ : , "350":"2500"]
    
    # my_k = math.ceil(2150*0.02)
    my_k = 'all'
    
    x_train, x_test, y_train, y_test = train_test_split(firma,
                                                        dataset.loc[:, target],
                                                        test_size=0.33,
                                                        random_state=1)
    
    f_selector = SelectKBest(score_func=f_regression, k=my_k)
    f_selector.fit(x_train, y_train)
    train_fs = f_selector.transform(x_train)
    test_fs = f_selector.transform(x_test)
    
    # elegidos = f_selector.get_support(True)
    
    elegidos = calcular_75_sup(f_selector)
    
    for i in range(len(elegidos)):
        elegidos[i] = elegidos[i] + 350
        
    #print("Grupo control 2014: ", elegidos)
    #print("Rangos: ", rangos_clustering(elegidos))
    #print("")
    
    # plot
    # plt.bar([i + 350 for i in range(len(f_selector.scores_))], f_selector.scores_)
    # plt.title("KBest (" + target + ")")
    # plt.xlabel("Longitud de onda")
    # plt.ylabel("Importancia por Correlación")
    # plt.show()
    
    return elegidos # fin k-best-------------------------------------------------------

def kbest_mi(target, dataset):
    firma = dataset.loc[ : , "350":"2500"]
    
    my_k = 'all'
    
    x_train, x_test, y_train, y_test = train_test_split(firma,
                                                        dataset.loc[:, target],
                                                        test_size=0.33,
                                                        random_state=1)
    
    f_selector = SelectKBest(score_func=mutual_info_regression, k=my_k)
    f_selector.fit(x_train, y_train)
    train_fs = f_selector.transform(x_train)
    test_fs = f_selector.transform(x_test)
    
    # elegidos = f_selector.get_support(True)
    
    elegidos = calcular_75_sup(f_selector)
    
    for i in range(len(elegidos)):
        elegidos[i] = elegidos[i] + 350
        
    #print("Grupo control 2014: ", elegidos)
    #print("Rangos: ", rangos_clustering(elegidos))
    # print("tipo datos rangos:", type(elegidos)) # tipo de variable
    #print("")
    
    # plot
    # plt.bar([i + 350 for i in range(len(f_selector.scores_))], f_selector.scores_)
    # plt.title("KBest (" + target + ")")
    # plt.xlabel("Longitud de onda")
    # plt.ylabel("Importancia por Información Mutua")
    # plt.show()
    
    return elegidos
