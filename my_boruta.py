# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from boruta import BorutaPy
from sklearn.preprocessing import StandardScaler
import pandas

def string_to_int(lista):
        for i in range(len(lista)):
            lista[i] = int(lista[i])
        return lista

# Original algorithm from
# https://towardsdatascience.com/boruta-explained-the-way-i-wish-someone-explained-it-to-me-4489d70e154a
def my_boruta_init(target, dataset):
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
    target_col = dataset.loc[: , target]
    
    forest = RandomForestRegressor(
        n_jobs = -1, 
        max_depth = 5
    )
    boruta = BorutaPy(
        estimator = forest, 
        n_estimators = 'auto',
        max_iter = 100 # number of trials to perform
    )
    
    # fit Boruta (it accepts np.array, not pd.DataFrame)
    boruta.fit(np.array(signature), np.array(target_col))
    
    # results
    # green_area: features admitted as confirmed
    # blue_area: features claimed as tetative
    green_area = signature.columns[boruta.support_].to_list()
    blue_area = signature.columns[boruta.support_weak_].to_list()
    
    green_area = string_to_int(green_area)
    
    return green_area # fin boruta -------------------------------------------------------
        

    