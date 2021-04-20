# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from boruta import BorutaPy

def string_to_int(lista):
        for i in range(len(lista)):
            lista[i] = int(lista[i])
        return lista

# Original algorithm from
# https://towardsdatascience.com/boruta-explained-the-way-i-wish-someone-explained-it-to-me-4489d70e154a
def my_boruta_init(target, dataset):
    # get signature columns
    firma = dataset.loc[ : , "350":"2499"]
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
    boruta.fit(np.array(firma), np.array(target_col))
    
    # results
    # green_area: features admitted as confirmed
    # blue_area: features claimed as tetative
    green_area = firma.columns[boruta.support_].to_list()
    blue_area = firma.columns[boruta.support_weak_].to_list()
    
    green_area = string_to_int(green_area)
    
    return green_area # fin boruta -------------------------------------------------------
        

    