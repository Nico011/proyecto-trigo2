# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import savgol_filter

from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler


def optimise_pls_cv(X, y, n_comp):
    # Define PLS object
    pls = PLSRegression(n_components = n_comp)
    
    # Cross-validation
    y_cv = cross_val_predict(pls, X, y, cv = 10)
    
    # Calculate scores
    r2 = r2_score(y, y_cv)
    mse = mean_squared_error(y, y_cv)
    rpd = y.std()/np.sqrt(mse)
    
    # print(f"r2: {r2}")
    # print(f"mse: {mse}")
    # print(f"rpd: {rpd}")
    
    return (y_cv, r2, mse, rpd)


def plot_metrics(vals, ylabel, objective, xticks):
    with plt.style.context('ggplot'):
        plt.plot(xticks, np.array(vals), '-v', color='blue', mfc='blue')
        if objective == 'min':
            idx = np.argmin(vals)
            print("min: ", idx)
        else:
            idx = np.argmax(vals)
            print("max: ", idx)
        plt.plot(xticks[idx], np.array(vals)[idx], 'P', ms=10, mfc='red')
        
        plt.xlabel('Number of PLS components')
        plt.xticks = xticks
        plt.ylabel(ylabel)
        plt.title('PLS')
        
        plt.show()
    
    return


def pls_regression(target, dataset):
    
    y = dataset.loc[ : , target]
    X = dataset.iloc[ : , 1: ]
    
    # min_col = int(X.columns[0])
    # max_col = int(X.columns[len(X.columns) - 1])
    
    # with plt.style.context('ggplot'):
    #     plt.plot(np.arange(min_col, max_col), X.T)
    #     plt.xlabel("Wavelengths (nm)")
    #     plt.ylabel("Reflectance (%)")
    
    # standardize predictors
    X2 = StandardScaler().fit_transform(X)
    
    # X2 = savgol_filter(X, 17, polyorder = 2, deriv = 2)
    
    # plt.figure(figsize = (8, 4.5))
    # with plt.style.context('ggplot'):
    #     plt.plot(np.arange(min_col, max_col), X2.T)
    #     plt.table("D2")
    #     plt.show()
    
    r2s = []
    mses = []
    rpds = []
    xticks = np.arange(1,51)
    for n_comp in xticks:
        y_cv, r2, mse, rpd = optimise_pls_cv(X2, y, n_comp)
        r2s.append(r2)
        mses.append(mse)
        rpds.append(rpd)
    
    plot_metrics(mses, 'MSE', 'min', xticks)
    plot_metrics(rpds, 'RPD', 'max', xticks)
    plot_metrics(r2s, 'R2', 'max', xticks)
    
    return
