# -*- coding: utf-8 -*-

import numpy as np
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import r2_score
from sklearn import linear_model
from feature_selection_ga import FeatureSelectionGA


# Creamos una función fitness personalizada
class CustomFitnessFunctionClass:
    def __init__(self,n_total_features,n_splits = 5, alpha=0.01, *args,**kwargs):
        """
            Parameters
            -----------
            n_total_features :int
            	Total number of features N_t.
            n_splits :int, default = 5
                Number of splits for cv
            alpha :float, default = 0.01
                Tradeoff between the classifier performance P and size of 
                feature subset N_f with respect to the total number of features
                N_t.
            
            verbose: 0 or 1
        """
        self.n_splits = n_splits
        self.alpha = alpha
        self.n_total_features = n_total_features

    def calculate_fitness(self,model,x,y):
        alpha = self.alpha
        total_features = self.n_total_features

        cv_set = np.repeat(-1.,x.shape[0])
        skf = RepeatedKFold(n_splits = self.n_splits)
        for train_index,test_index in skf.split(x,y):
            x_train,x_test = x[train_index],x[test_index]
            y_train,y_test = y[train_index],y[test_index]
            if x_train.shape[0] != y_train.shape[0]:
                raise Exception()
            model.fit(x_train,y_train)
            predicted_y = model.predict(x_test)
            cv_set[test_index] = predicted_y
        
        # P = accuracy_score(y, cv_set)
        P = r2_score(y, cv_set)
        fitness = (alpha*(1.0 - P) + (1.0 - alpha)*(1.0 - (x.shape[1])/total_features))
        return fitness



def ga(target, firma, control):
    print("Ejecutando Genetic Algorithm...")
    # Grupo control 2014 ###################################
    x = firma
    y = control.loc[:, target]
    model = linear_model.LinearRegression()
    ff = CustomFitnessFunctionClass(n_total_features=x.shape[1], 
                                    n_splits=3,
                                    alpha=0.05)
    fsga = FeatureSelectionGA(model, x, y, ff_obj = ff)
    pop = fsga.generate(5000)
    print(pop)
    
    return


