# -*- coding: utf-8 -*-

import pandas
import matplotlib.pyplot as plt
import seaborn
from sklearn.preprocessing import StandardScaler

# Data preprocessing for a year given as parameter
def data_any_year(target, year):
    
    # Switch commented functions to read data from file or url
    # Read csv from file 
    data = pandas.read_csv("data-total.csv", header=0, delimiter=";", encoding='ISO-8859-1')
    
    # Read csv from url
    # url = "https://raw.githubusercontent.com/Nico011/proyecto-trigo2/master/data-total.csv"
    # get_content = requests.get(url).content
    # data = pandas.read_csv(io.StringIO(get_content.decode('ISO-8859-1')), 
    #                        header = 0, delimiter = ";", encoding = 'ISO-8859-1')
   
    # possible filters:
    # Fenologia != antesis
    # condición != secano
    # Genotipo = "QUP 2569-2009"
    
    # get data for given year
    filter_year = data[data["ANIO"] == year]
    
    # separete data sets (water_stress/control)
    filter_control = filter_year[filter_year["CONDICION"] != "SECANO"]
    filter_water_stress = filter_year[filter_year["CONDICION"] == "SECANO"]
    
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
    
    df_target_water_stress = filter_water_stress.loc[ : , target]
    df_firma_water_stress = filter_water_stress.loc[ : , "350":"2499"]
    
    # Estandadize water_stress
    df_firma_water_stress = pandas.DataFrame(StandardScaler().fit_transform(df_firma_water_stress)) 
    df_firma_water_stress.columns = cols
    
    # join target column to predictors
    control = pandas.concat([df_target_control.reset_index(drop=True), df_firma_control], axis = 1)
    water_stress = pandas.concat([df_target_water_stress.reset_index(drop=True), df_firma_water_stress], axis = 1)
    
    # count outliers for control
    c_q1 = control.loc[ : , target].quantile(0.25)
    c_q3 = control.loc[ : , target].quantile(0.75)
    c_iqr = c_q3 - c_q1
    
    print(f"Outliers in target column (control set):\n{((control.loc[ : , target] < (c_q1 - 1.5 * c_iqr)) | (control.loc[ : , target] > (c_q3 + 1.5 * c_iqr))).sum()}")
    
    # count outliers for water stress
    ws_q1 = water_stress.loc[ : , target].quantile(0.25)
    ws_q3 = water_stress.loc[ : , target].quantile(0.75)
    ws_iqr = ws_q3 - ws_q1
    
    print(f"Outliers in target column (water stress set):\n{((water_stress.loc[ : , target] < (ws_q1 - 1.5 * ws_iqr)) | (water_stress.loc[ : , target] > (ws_q3 + 1.5 * ws_iqr))).sum()}")
    
    # show number of NaN in datasets
    print("Number of NaN (control dataset):", control.isna().sum().sum())
    print("Number of NaN (water stress dataset):", water_stress.isna().sum().sum())
    
    # drop rows with NAs
    control.dropna(inplace = True)
    water_stress.dropna(inplace = True)
    
    # return control dataframe and water stress dataframe
    return control, water_stress
