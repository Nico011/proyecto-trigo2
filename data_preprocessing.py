# -*- coding: utf-8 -*-

import pandas
from sklearn.preprocessing import StandardScaler

# Data preprocessing for a year given as parameter
def data_any_year(target, datos, year):
    # get data for given year
    filter_year = datos[datos["ANIO"] == year]
    
    # separete data sets (secano/control)
    filter_control = filter_year[filter_year["CONDICION"] != "SECANO"]
    filter_secano = filter_year[filter_year["CONDICION"] == "SECANO"]
    
    # get target column
    df_target_control = filter_control.loc[ : , target]
    
    # get signature columns, and column names as list
    df_firma_control = filter_control.loc[ : , "350":"2499"]
    cols = list(df_firma_control.columns.values) 
    
    # Standardize signature
    # the standard score of the sample x is calculated as:
    # z = (x - u)/s
    # where u is the mean of the training samples,
    # and s is the standard deviation of the training samples
    df_firma_control = pandas.DataFrame(StandardScaler().fit_transform(df_firma_control))
    
    # assign column names to dataframe
    df_firma_control.columns = cols
    
    df_target_secano = filter_secano.loc[ : , target]
    df_firma_secano = filter_secano.loc[ : , "350":"2499"]
    
    # Estandadize secano
    df_firma_secano = pandas.DataFrame(StandardScaler().fit_transform(df_firma_secano)) 
    df_firma_secano.columns = cols
    
    # join target column to predictors
    control = pandas.concat([df_target_control.reset_index(drop=True), df_firma_control], axis = 1)
    secano = pandas.concat([df_target_secano.reset_index(drop=True), df_firma_secano], axis = 1)
    
    print("Number of NaN (control dataset):", control.isna().sum().sum())
    print("Number of NaN (dry land dataset):", secano.isna().sum().sum())
    
    # drop rows with NAs
    control.dropna(inplace = True)
    secano.dropna(inplace = True)
    
    # return control dataframe and dry land dataframe
    return control, secano
