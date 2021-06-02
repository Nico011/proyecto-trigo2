# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
import pandas
import numpy as np


def calcular_75_sup(lista_importancia):
    mediana = (np.max(lista_importancia.scores_)) / 2
    val_75_sup = mediana + (mediana * 0.5)
    lista_75_sup = []
    for i in range(len(lista_importancia.scores_)):
        if lista_importancia.scores_[i] >= val_75_sup:
            lista_75_sup.append(i)
    return lista_75_sup


def kbest_corr(target, dataset):
    if dataset.shape[0] == 0:
        return []
    
    # Standardize signature (z-score)
    # the standard score of the sample x is calculated as:
    # z = (x - u)/s
    # where u is the mean of the training samples,
    # and s is the standard deviation of the training samples
    cols = list(dataset.columns.values)
    signature = dataset.iloc[ : , 1:]
    signature = pandas.DataFrame(StandardScaler().fit_transform(signature))
    dataset = pandas.concat([dataset.loc[ : , target].reset_index(drop=True), signature], axis = 1)
    dataset.columns = cols
    
    # get signature columns
    signature = dataset.iloc[ : , 1:]
    
    my_k = 'all'
    
    x_train, x_test, y_train, y_test = train_test_split(signature,
                                                        dataset.loc[:, target],
                                                        test_size=0.33,
                                                        random_state=1)
    
    f_selector = SelectKBest(score_func=f_regression, k=my_k)
    f_selector.fit(x_train, y_train)
    train_fs = f_selector.transform(x_train)
    test_fs = f_selector.transform(x_test)
    
    elegidos = calcular_75_sup(f_selector)
    
    for i in range(len(elegidos)):
        elegidos[i] = elegidos[i] + 350
    
    return elegidos 

def kbest_mi(target, dataset):
    if dataset.shape[0] == 0:
        return []
    
    # Standardize signature (z-score)
    # the standard score of the sample x is calculated as:
    # z = (x - u)/s
    # where u is the mean of the training samples,
    # and s is the standard deviation of the training samples
    cols = list(dataset.columns.values)
    signature = dataset.iloc[ : , 1:]
    signature = pandas.DataFrame(StandardScaler().fit_transform(signature))
    dataset = pandas.concat([dataset.loc[ : , target].reset_index(drop=True), signature], axis = 1)
    dataset.columns = cols
    
    signature = dataset.iloc[ : , 1:]
    
    my_k = 'all'
    
    x_train, x_test, y_train, y_test = train_test_split(signature,
                                                        dataset.loc[:, target],
                                                        test_size=0.33,
                                                        random_state=1)
    
    f_selector = SelectKBest(score_func=mutual_info_regression, k=my_k)
    f_selector.fit(x_train, y_train)
    train_fs = f_selector.transform(x_train)
    test_fs = f_selector.transform(x_test)
    
    elegidos = calcular_75_sup(f_selector)
    
    for i in range(len(elegidos)):
        elegidos[i] = elegidos[i] + 350
    
    return elegidos
