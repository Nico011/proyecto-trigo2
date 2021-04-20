# -*- coding: utf-8 -*-

from sklearn.linear_model import LassoCV
import numpy as np


def lasso_init(target, data):
    max = 1500
    
    firma = data.loc[: , "350":"2499"]
    target_col = data.loc[: , target]
    cols = data.columns
    
    lasso_control = LassoCV(max_iter = 10000).fit(firma, target_col)
    importancia_c = np.abs(lasso_control.coef_)
    
    # This loop searches the list of importance values ordered from
    # highest to lowest the index of the first value at 0 to show that amount
    # or a maximum (max) of items.
    for i in range(len(importancia_c)):
        if importancia_c[importancia_c.argsort()[::-1][i]] == 0 or i >= max:
            attr_n = i
            break
    
    attrs_c = importancia_c.argsort()[::-1][:attr_n]
    cols_aux = np.array(cols)[attrs_c]
    
    # cast str to int
    cols_aux = cols_aux.astype(int)
        
    # sort in ascending order
    cols_aux = np.sort(cols_aux)
    
    return cols_aux 
