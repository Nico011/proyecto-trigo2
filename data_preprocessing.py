# -*- coding: utf-8 -*-

import pandas
from sklearn.preprocessing import StandardScaler


def data_any_year(target, datos, year):
    filtro1 = datos[datos["ANIO"] == year]
    filtro2 = datos[datos["ANIO"] == year]
    
    filtro1 = filtro1[filtro1["CONDICION"] != "SECANO"]
    filtro2 = filtro2[filtro2["CONDICION"] == "SECANO"]
    
    df_chl_control = filtro1.loc[ : , target]
    df_firma_control = filtro1.loc[ : , "350":"2500"]
    cols = list(df_firma_control.columns.values) # recuperamos los nombres de columnas
    
    # Estandarizar control
    df_firma_control = pandas.DataFrame(StandardScaler().fit_transform(df_firma_control)) 
    df_firma_control.columns = cols
    
    df_chl_secano = filtro2.loc[ : , target]
    df_firma_secano = filtro2.loc[ : , "350":len(filtro2)-1]
    
    # Estandarizar secano
    df_firma_secano = pandas.DataFrame(StandardScaler().fit_transform(df_firma_secano)) 
    df_firma_secano.columns = cols
    
    # Unir columna a predecir con predictores
    control = pandas.concat([df_chl_control.reset_index(drop=True), df_firma_control], axis = 1)
    secano = pandas.concat([df_chl_secano.reset_index(drop=True), df_firma_secano], axis = 1)
    
    # eliminar NAs
    control.dropna(inplace = True)
    secano.dropna(inplace = True)
    
    # Reasignamos estas variables, pero ahora se eliminaron los NAs y se estandarizó
    firma_control = control.loc[ : , "350":"2500"]
    firma_secano = secano.loc[ : , "350":"2500"]
    return firma_control, control, firma_secano, secano



def data_2014(target, datos):
    # filtro por año (2014)------------------------------------
    filtro1_2014 = datos[datos["ANIO"] == 2014]
    filtro2_2014 = datos[datos["ANIO"] == 2014]
    
    filtro1_2014 = filtro1_2014[filtro1_2014["CONDICION"] != "SECANO"]
    filtro2_2014 = filtro2_2014[filtro2_2014["CONDICION"] == "SECANO"]
    
    df_chl_control_2014 = filtro1_2014.loc[ : , target]
    df_firma_control_2014 = filtro1_2014.loc[ : , "350":"2500"]
    cols = list(df_firma_control_2014.columns.values) # recuperamos los nombres de columnas
    
    # Estandarizar control 2014
    df_firma_control_2014 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_control_2014)) 
    df_firma_control_2014.columns = cols
    
    df_chl_secano_2014 = filtro2_2014.loc[ : , target]
    df_firma_secano_2014 = filtro2_2014.loc[ : , "350":"2500"]
    
    # Estandarizar secano 2014
    df_firma_secano_2014 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_secano_2014)) 
    df_firma_secano_2014.columns = cols
    
    # Unir columna a predecir con predictores
    control_2014 = pandas.concat([df_chl_control_2014.reset_index(drop=True), df_firma_control_2014], axis = 1)
    secano_2014 = pandas.concat([df_chl_secano_2014.reset_index(drop=True), df_firma_secano_2014], axis = 1)
    
    # eliminar NAs
    control_2014.dropna(inplace = True)
    secano_2014.dropna(inplace = True)
    
    # Reasignamos estas variables, pero ahora se eliminaron los NAs y se estandarizó
    firma_control_2014 = control_2014.loc[ : , "350":"2500"]
    firma_secano_2014 = secano_2014.loc[ : , "350":"2500"]
    return firma_control_2014, control_2014

def data_2015(target, datos):
    # filtro por año (2015) -----------------------------------
    filtro1_2015 = datos[datos["ANIO"] == 2015]
    filtro2_2015 = datos[datos["ANIO"] == 2015]
    
    filtro1_2015 = filtro1_2015[filtro1_2015["CONDICION"] != "SECANO"]
    filtro2_2015 = filtro2_2015[filtro2_2015["CONDICION"] == "SECANO"]
    
    df_chl_control_2015 = filtro1_2015.loc[ : , target]
    df_firma_control_2015 = filtro1_2015.loc[ : , "350":"2500"]
    cols = list(df_firma_control_2015.columns.values) # recuperamos los nombres de columnas
    
    # Estandarizar control 2015
    df_firma_control_2015 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_control_2015)) 
    df_firma_control_2015.columns = cols
    
    df_chl_secano_2015 = filtro2_2015.loc[ : , target]
    df_firma_secano_2015 = filtro2_2015.loc[ : , "350":"2500"]
    
    # Estandarizar secano 2015
    df_firma_secano_2015 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_secano_2015)) 
    df_firma_secano_2015.columns = cols
    
    # Unir columna a predecir con predictores
    control_2015 = pandas.concat([df_chl_control_2015.reset_index(drop=True), df_firma_control_2015], axis = 1)
    secano_2015 = pandas.concat([df_chl_secano_2015.reset_index(drop=True), df_firma_secano_2015], axis = 1)
    
    # eliminar NAs
    control_2015.dropna(inplace = True)
    secano_2015.dropna(inplace = True)
    
    # Reasignamos estas variables, pero ahora se eliminaron los NAs y se estandarizó
    firma_control_2015 = control_2015.loc[ : , "350":"2500"]
    firma_secano_2015 = secano_2015.loc[ : , "350":"2500"]
    return

def data_2016(target, datos):
    # filtro por año (2016) -----------------------------------------------
    filtro1_2016 = datos[datos["ANIO"] == 2016]
    filtro2_2016 = datos[datos["ANIO"] == 2016]
    
    filtro1_2016 = filtro1_2016[filtro1_2016["CONDICION"] != "SECANO"]
    filtro2_2016 = filtro2_2016[filtro2_2016["CONDICION"] == "SECANO"]
    
    
    df_chl_control_2016 = filtro1_2016.loc[ : , target]
    df_firma_control_2016 = filtro1_2016.loc[ : , "350":"2499"]
    cols = list(df_firma_control_2016.columns.values) # recuperamos los nombres de columnas
    
    # Estandarizar control 2016
    df_firma_control_2016 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_control_2016)) 
    df_firma_control_2016.columns = cols
    
    df_chl_secano_2016 = filtro2_2016.loc[ : , target]
    df_firma_secano_2016 = filtro2_2016.loc[ : , "350":"2499"]
    
    # Estandarizar secano 2016
    df_firma_secano_2016 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_secano_2016)) 
    df_firma_secano_2016.columns = cols
    
    # Unir columna a predecir con predictores
    control_2016 = pandas.concat([df_chl_control_2016.reset_index(drop=True), df_firma_control_2016], axis = 1)
    secano_2016 = pandas.concat([df_chl_secano_2016.reset_index(drop=True), df_firma_secano_2016], axis = 1)
    
    # eliminar NAs
    control_2016.dropna(inplace = True)
    secano_2016.dropna(inplace = True)
    
    # Reasignamos estas variables, pero ahora se eliminaron los NAs y se estandarizó
    firma_control_2016 = control_2016.loc[ : , "350":"2499"]
    firma_secano_2016 = secano_2016.loc[ : , "350":"2499"]
    return

def data_2017(target, datos):
    
    # filtro por año 2017 -----------------------------------------------
    filtro1_2017 = datos[datos["ANIO"] == 2017]
    filtro2_2017 = datos[datos["ANIO"] == 2017]
    
    filtro1_2017 = filtro1_2017[filtro1_2017["CONDICION"] != "SECANO"]
    filtro2_2017 = filtro2_2017[filtro2_2017["CONDICION"] == "SECANO"]
    
    df_chl_control_2017 = filtro1_2017.loc[ : , target]
    df_firma_control_2017 = filtro1_2017.loc[ : , "350":"2500"]
    cols = list(df_firma_control_2017.columns.values) # recuperamos los nombres de columnas
    
    # Estandarizar control 2017
    df_firma_control_2017 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_control_2017)) 
    df_firma_control_2017.columns = cols
    
    df_chl_secano_2017 = filtro2_2017.loc[ : , target]
    df_firma_secano_2017 = filtro2_2017.loc[ : , "350":"2500"]
    
    # Estandarizar secano 2017
    df_firma_secano_2017 = pandas.DataFrame(StandardScaler().fit_transform(df_firma_secano_2017)) 
    df_firma_secano_2017.columns = cols
    
    # Unir columna a predecir con predictores
    control_2017 = pandas.concat([df_chl_control_2017.reset_index(drop=True), df_firma_control_2017], axis = 1)
    secano_2017 = pandas.concat([df_chl_secano_2017.reset_index(drop=True), df_firma_secano_2017], axis = 1)
    
    # eliminar NAs
    control_2017.dropna(inplace = True)
    secano_2017.dropna(inplace = True)
    
    # Reasignamos estas variables, pero ahora se eliminaron los NAs y se estandarizó
    firma_control_2017 = control_2017.loc[ : , "350":"2500"]
    firma_secano_2017 = secano_2017.loc[ : , "350":"2500"]
    return