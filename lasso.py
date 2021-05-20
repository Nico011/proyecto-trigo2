# -*- coding: utf-8 -*-

from sklearn.linear_model import LassoCV
import numpy as np
import pandas
from sklearn.preprocessing import StandardScaler


def lasso_init(target, data):
    # Standardize signature (z-score)
    # the standard score of the sample x is calculated as:
    # z = (x - u)/s
    # where u is the mean of the training samples,
    # and s is the standard deviation of the training samples
    cols = list(data.columns.values)
    signature = data.iloc[ : , 1:]
    signature = pandas.DataFrame(StandardScaler().fit_transform(signature))
    data = pandas.concat([data.loc[ : , target].reset_index(drop=True), signature], axis = 1)
    data.columns = cols
    
    signature = data.iloc[ : , 1:]
    target_col = data.loc[: , target]
    
    lasso = LassoCV(max_iter = 15000).fit(signature, target_col)
    important = np.abs(lasso.coef_)
    
    # Create list with the selected wavelength, search through coef_ list, when it
    # finds an item != 0, add to the new list the wavelength in that index
    wave_selected = []
    for i in range(len(important)):
        if important[i] != 0:
            wave_selected.append(i + 350)
    
    return wave_selected
