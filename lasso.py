# -*- coding: utf-8 -*-

from sklearn.linear_model import LassoCV
import numpy as np


#### LASSO feature selection ####################
def lasso_init(target, data):
    max = 150
    
    firma = data.loc[: , "350":"2499"]
    target_col = data.loc[: , target]
    cols = data.columns
    
    lasso_control = LassoCV(max_iter = 10000).fit(firma, target_col)
    importancia_c = np.abs(lasso_control.coef_)
    
    # Este bucle busca en la lista de valores de importancia ordenadas
    # de mayor a menor el índice del primer valor en 0 para mostrar 
    # esa cantidad o un máximo 150 (max) elementos.
    for i in range(len(importancia_c)):
        if importancia_c[importancia_c.argsort()[::-1][i]] == 0 or i >= max:
            attr_n = i
            # print("indice del primer valor 0: " + str(attr_n))
            break
    
    attrs_c = importancia_c.argsort()[::-1][:attr_n]
    cols_aux = np.array(cols)[attrs_c]
    
    # convertir str a int
    cols_aux = cols_aux.astype(int)
        
    # ordenamos en orden ascendente
    cols_aux = np.sort(cols_aux)
    
    return cols_aux 
