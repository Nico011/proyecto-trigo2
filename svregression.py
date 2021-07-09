# -*- coding: utf-8 -*-

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score
from sklearn.svm import SVR
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas

def svr(target, dataset):
    if dataset is None:
        print("Empty dataset, no regression possible.")
        return
    
    # Separates target from predictors
    y = dataset.loc[ : , target]
    X = dataset.iloc[ : , 1: ]
    
    # standardize predictors
    X = StandardScaler().fit_transform(X)
    
    # split train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
        )
    
    
    # regression
    regressor = SVR(kernel='linear', epsilon=0.2, C=1)
    regressor.fit(X_train, y_train)
    
    # 10 fold cross valiation
    kfold_pred = cross_val_predict(estimator=regressor, X=X, y=y, cv=10)
    
    # print result
    print("SVR r2 score: %.3f" 
          % r2_score(y, kfold_pred))
    
    return