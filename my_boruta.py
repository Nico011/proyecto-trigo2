# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from boruta import BorutaPy

def string_to_int(lista):
        for i in range(len(lista)):
            lista[i] = int(lista[i])
        return lista

def my_boruta_init(target, firma, control):
    print("Ejecutando Boruta...")
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
    boruta.fit(np.array(firma), np.array(control.loc[ : , target]))
    
    # print results grupo control
    green_area = firma.columns[boruta.support_].to_list()
    blue_area = firma.columns[boruta.support_weak_].to_list()
    
    green_area = string_to_int(green_area)
    
    print("Atributos importantes:", green_area)
    print("Atributos tentativos:", blue_area)
    #print("Rangos:", rangos_clustering(green_area_control))
    
    print("")
    
    return green_area # fin boruta -------------------------------------------------------
        

    