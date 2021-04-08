# -*- coding: utf-8 -*-

from sklearn.linear_model import LassoCV
import numpy as np


#### LASSO feature selection ####################
def my_lasso_init(target, firma, control, cols):
    print("Ejecutando LASSO...")
    max = 150
    
    lasso_control = LassoCV(max_iter = 10000).fit(firma, control.loc[ : , target])
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
    
    #print("Atributos seleccionados (control 2014): {}".format(cols_aux))
    #print("Rangos: ", rangos_clustering(cols_aux))
    #print("")
    
    # graficamos la importancia de cada atributo
    # plt.bar(height=importancia_c, x=np.array(cols))
    # plt.title("LASSO - Grupo control 2014 (" + target + ")")
    # plt.xlabel("Longitud de onda")
    # plt.ylabel("Importancia")
    # plt.show()
    
    return cols_aux # fin lasso --------------------------------------------------------
