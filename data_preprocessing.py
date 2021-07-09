# -*- coding: utf-8 -*-

import pandas
import numpy

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
    
    # Read xlsx
    # xl_file = pandas.ExcelFile("Datos trigo CLIP SR-CAU.xlsx")
    # data = {sheet_name: xl_file.parse(sheet_name)
    #         for sheet_name in xl_file.sheet_names}
   
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
    
    # assign column names to dataframe
    df_firma_control.columns = cols
    
    df_target_water_stress = filter_water_stress.loc[ : , target]
    df_firma_water_stress = filter_water_stress.loc[ : , "350":"2499"]
    
    df_firma_water_stress.columns = cols
    
    # join (horizontaly) target column to predictors
    control = pandas.concat(
        [df_target_control.reset_index(drop=True), 
         df_firma_control.reset_index(drop=True)], 
        axis = 1
        )
    water_stress = pandas.concat(
        [df_target_water_stress.reset_index(drop=True), 
         df_firma_water_stress.reset_index(drop=True)], 
        axis = 1
        )
    
    # count outliers for control
    # https://stackoverflow.com/questions/39068214/how-to-count-outliers-for-all-columns-in-python
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
    print("")
    
    # drop rows with NAs
    control.dropna(inplace = True)
    water_stress.dropna(inplace = True)
    
    # return control dataframe and water stress dataframe
    return control, water_stress


# Return dataset only with signature to long format
def wide_to_long(wide_dataset):
    
    wide_dataset_t = wide_dataset.transpose()
    wide_dataset_t.index.name = "wavelength"
    
    wide_dataset_t.reset_index(inplace = True)
    long_dataset = pandas.melt(
        wide_dataset_t,
        id_vars = "wavelength"
        )
    
    return long_dataset


# This function converts a list of selected wavelengths (from feature selection
# algorithms) to a dataframe with only selected columns. This also converts 
# ranges (from ranges function) to a dataframe with only the columns between
# ranges.
def selected_or_ranges_to_dataset(selected, ranges, whole_dataset, target):
    
    if len(ranges) == 1:
        ranges_dataframe = whole_dataset[[target, str(ranges[0][0])]]
    
    elif len(ranges) > 1:
        ranges_list = [[target]]
        for r in ranges:
            ranges_list.append(list(range(r[0], r[1] + 1)))
            
        # 2D list to 1D list
        ranges_list = list(numpy.concatenate(ranges_list).flat)
        # ints to strs
        ranges_list = [str(int) for int in ranges_list]
        
        # select columns in dataset
        ranges_dataframe = whole_dataset[ranges_list]
    else:
        ranges_dataframe = None
            

    if len(selected) != 0:
        sel = [target] + [str(i) for i in selected]
        selected_dataframe = whole_dataset[sel]
    else:
        selected_dataframe = None
        
    
    
    return selected_dataframe, ranges_dataframe



