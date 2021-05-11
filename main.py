# -*- coding: utf-8 -*-
# This function hides warning messages (from lasso algorithm)
# https://stackoverflow.com/questions/32612180/eliminating-warnings-from-scikit-learn
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from plotnine import ggplot, aes, labs, geom_line, geom_vline, geom_rect

import time
import sys
import getopt
import os

import data_preprocessing
import my_boruta
import lasso
import kbest
import ga
import ranges


def graphics(target, control, ranges_control, water_stress, ranges_water_stress):
    
    # Graphics for control set
    control_sample = control.loc[ : , "350":"2499"].sample(frac = 0.1, random_state = 1)
    
    control_sample_t = control_sample.transpose()
    y_min = min(control_sample_t.iloc[ : , 1])
    y_max = max(control_sample_t.iloc[ : , 1])
    
    graph_ctrl = ggplot(control_sample_t) \
        + aes(x = [i for i in range(350, 2500)], y = control_sample_t.iloc[ : , 1]) \
        +labs(
            x = "Wavelength (nm)",
            y = "Reflectance %",
            title = "Ranges selected in a spectral signature (standardized)"
            ) 
        
    for i in range(len(ranges_control)):
        i_range = []
        for j in range(len(ranges_control[i])):
            graph_ctrl = graph_ctrl + geom_vline(xintercept = ranges_control[i][j], color="black", alpha = 0) 
            i_range.append(ranges_control[i][j])
        graph_ctrl = graph_ctrl + geom_rect(aes(xmin = i_range[0], xmax = i_range[1], ymin = y_min, ymax = y_max), fill = "steelblue", alpha = 0.1)
    graph_ctrl = graph_ctrl + geom_line()
    
    print(graph_ctrl)
    graph_ctrl.save(filename = f"ranges control {target}")
   
    # Graphics for water stress set
    ws_sample = water_stress.loc[ : , "350":"2499"].sample(frac = 0.1, random_state = 1)
    
    ws_sample_t = ws_sample.transpose()
    
    y_min = min(ws_sample_t.iloc[ : , 1])
    y_max = max(ws_sample_t.iloc[ : , 1])
    
    graph_ws = ggplot(ws_sample_t) \
        + aes(x = [i for i in range(350, 2500)], y = ws_sample_t.iloc[ : , 1]) \
        +labs(
            x = "Wavelength (nm)",
            y = "Reflectance %",
            title = "Ranges selected in a spectral signature (standardized)"
            ) 
        
    for i in range(len(ranges_water_stress)):
        i_range = []
        for j in range(len(ranges_water_stress[i])):
            graph_ws = graph_ws + geom_vline(xintercept = ranges_water_stress[i][j], color="black", alpha = 0) 
            i_range.append(ranges_water_stress[i][j])
        graph_ws = graph_ws + geom_rect(aes(xmin = i_range[0], xmax = i_range[1], ymin = y_min, ymax = y_max), fill = "steelblue", alpha = 0.1)
    graph_ws = graph_ws + geom_line()
    
    print(graph_ws)
    graph_ws.save(filename = f"ranges water stress {target}")
    return


# The following functions run each algorithm available and prints their results.
# They all work about the same. They receive as parameters the target (string),
# and the filtered dataset separated as control and water stress.
# They print the name of the algorithm,
# wavelength selected as important by the algorithm, and
# wavelength selected as important in range format.
def run_boruta(target, control, water_stress, year):
    print("Running Boruta Algorithm...")
    elegidos_control = my_boruta.my_boruta_init(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = ranges.rangos_clustering(target,elegidos_control, "control", year, "boruta")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_water_stress = my_boruta.my_boruta_init(target, water_stress)
    print(f"Selected water stress: {len(elegidos_water_stress)} wavelength(s)\n{elegidos_water_stress}")
    rangos_water_stress= ranges.rangos_clustering(target, elegidos_water_stress, "water stress", year, "boruta")
    print(f"Selected wavelength ranges (water stress set): {rangos_water_stress}")
    graphics(target, control, rangos_control, water_stress, rangos_water_stress, year)
    return

def run_lasso(target, control, water_stress, year):
    print("Running LASSO...")
    elegidos_control = lasso.lasso_init(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = ranges.rangos_clustering(target, elegidos_control, "control", year, "lasso")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_water_stress = lasso.lasso_init(target, water_stress)
    print(f"Selected water stress: {len(elegidos_water_stress)} wavelength(s)\n{elegidos_water_stress}")
    rangos_water_stress = ranges.rangos_clustering(target, elegidos_water_stress, "water stress", year, "lasso")
    print(f"Selected wavelength ranges (water stress set): {rangos_water_stress}")
    graphics(target, control, rangos_control, water_stress, rangos_water_stress, year)
    return

def run_kbest_corr(target, control, water_stress, year):
    print("Running SelectK-Best (Correlation)...")
    elegidos_control = kbest.kbest_corr(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = ranges.rangos_clustering(target, elegidos_control, "control", year, "kbestcorr")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_water_stress = kbest.kbest_corr(target, water_stress)
    print(f"Selected water stress: {len(elegidos_water_stress)} wavelength(s)\n{elegidos_water_stress}")
    rangos_water_stress = ranges.rangos_clustering(target, elegidos_water_stress, "water stress", year, "kbestcorr")
    print(f"Selected wavelength ranges (water stress set): {rangos_water_stress}")
    graphics(target, control, rangos_control, water_stress, rangos_water_stress, year)
    return

def run_kbest_mi(target, control, water_stress, year):
    print("Running SelectK-Best (Mutual Information)...")
    elegidos_control = kbest.kbest_mi(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = ranges.rangos_clustering(target, elegidos_control, "control", year, "kbestmi")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_water_stress = kbest.kbest_mi(target, water_stress)
    print(f"Selected water stress: {len(elegidos_water_stress)} wavelength(s)\n{elegidos_water_stress}")
    rangos_water_stress = ranges.rangos_clustering(target, elegidos_water_stress, "water stress", year, "kbestmi")
    print(f"Selected wavelength ranges (water stress set): {rangos_water_stress}")
    graphics(target, control, rangos_control, water_stress, rangos_water_stress, year)
    return

def run_ga(target, control, water_stress, year):
    print("Running Genetic Algorithm...")
    elegidos_control = ga.ga(target, control)
    print(f"Selected control: {len(elegidos_control)} wavelength(s)\n{elegidos_control}")
    rangos_control = ranges.rangos_clustering(target, elegidos_control, "control", year, "ga")
    print(f"Selected wavelength ranges (control set): {rangos_control}")
    print("")
    elegidos_water_stress = ga.ga(target, water_stress)
    print(f"Selected water stress: {len(elegidos_water_stress)} wavelength(s)\n{elegidos_water_stress}")
    rangos_water_stress = ranges.rangos_clustering(target, elegidos_water_stress, "water stress", year, "ga")
    print(f"Selected wavelength ranges (water stress set): {rangos_water_stress}")
    graphics(target, control, rangos_control, water_stress, rangos_water_stress, year)
    return

# Main function
def main(argv):
    # default values for line commands
    years_default = [2014, 2015, 2016, 2017]
    target = 'Chl'
    alg = 'kbestcorr'
    year = '2014'
    
    str_help = """Usage:
main.py -t <target> [-a <algorithm> -y <year>]

-t, --target    : Give a specific target (Deafault: Chl).
-a, --algorithm : Give a specific feature selection algorithm (Optional, default: all).
-y, --year      : Give a specific year (Optional, default: all).

Targets available: Chl, Flav, Anth, NBI, Pot.Hoja(Bar), Transmitted, 
                   LAI, EVAP, GS, PN, CI, VPD.

Algorithms available: 
    boruta     : Run Boruta feature selection algorithm.
    lasso      : Run LASSO feature selection algorithm.
    kbestcorr  : Run SelectkBest using the correlation ranking.
    kbestmi    : Run SelectkBest using mutual information ranking.
    ga         : Run Genetic Algorithm for feature selection.

Years available: 2014, 2015, 2016 and 2017."""

    try:
        opts, arg = getopt.getopt(argv, "ht:a:y:", ["target=", "algorithm=", "year="])
    except getopt.GetoptError as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(str_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(str_help)
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-a", "--algorithm"):
            alg = arg 
        elif opt in ("-y", "--year"):
            year = arg
            
    print(f"Target: {target}")
    print("")
   
            
    if year != 'all' and alg != 'all': 
        
        print(f"Year {year}:\n")
        print("Extracting data...")
        control, water_stress = data_preprocessing.data_any_year(target, int(year))
        
        if alg == 'boruta':
            start = time.perf_counter()
            run_boruta(target, control, water_stress, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'lasso':
            start = time.perf_counter()
            run_lasso(target, control, water_stress, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestcorr':
            start = time.perf_counter()
            run_kbest_corr(target, control, water_stress, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'kbestmi':
            start = time.perf_counter()
            run_kbest_mi(target, control, water_stress, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
        elif alg == 'ga':
            start = time.perf_counter()
            run_ga(target, control, water_stress, year)
            end = time.perf_counter()
            print(f"Execution time: {end - start:0.2f} seconds.")
            
    else:
        print("Extracting data...")
        time_total = 0
        for i in range(len(years_default)):
            print(f"\nYear: {years_default[i]}\n")
            control, water_stress = data_preprocessing.data_any_year(target, years_default[i])
            start = time.perf_counter()
            run_kbest_corr(target, control, water_stress, years_default[i])
            print("")
            run_kbest_mi(target, control, water_stress, years_default[i])
            print("")
            run_boruta(target, control, water_stress, years_default[i])
            print("")
            run_lasso(target, control, water_stress, years_default[i])
            print("")
            run_ga(target, control, water_stress, years_default[i])
            print("")
            end = time.perf_counter()
            time_total = time_total + (end - start)
        print(f"Execution time: {time_total:0.2f} seconds.")
    
    print(f"Boxplot and graphs saved as image in current working directory ({os.getcwd()})")

if __name__ == "__main__":
    main(sys.argv[1:])










