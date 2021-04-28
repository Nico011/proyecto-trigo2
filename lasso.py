# -*- coding: utf-8 -*-

from sklearn.linear_model import LassoCV
import numpy as np


def lasso_init(target, data):
    
    firma = data.loc[: , "350":"2499"]
    target_col = data.loc[: , target]
    
    lasso = LassoCV(max_iter = 15000).fit(firma, target_col)
    important = np.abs(lasso.coef_)
    
    # Create list with the selected wavelength, search through coef_ list, when it
    # finds an item != 0, add to the new list the wavelength in that index
    wave_selected = []
    for i in range(len(important)):
        if important[i] != 0:
            wave_selected.append(i + 350)
    
    return wave_selected
