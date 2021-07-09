# -*- coding: utf-8 -*-
from plotnine import ggplot, aes, labs, geom_line, theme, geom_rect#, geom_vline
import matplotlib.pyplot as plt
import numpy as np
import pandas
import os

PLOT_DIR = 'plots'
# Graphics for spectral signatures    
def ranges_graphics(target, signatures_long, ranges, hydro_state, year, algorithm):
    if ranges is None:
        return
    
    alg = ''
    if algorithm == "boruta":
        alg = "Boruta"
    elif algorithm == "lasso":
        alg = "LASSO"
    elif algorithm == "kbestcorr":
        alg = "SelectKBest (correlation)"
    elif algorithm == "kbestmi":
        alg = "SelectKBest (mutual information)"
    elif algorithm == "ga":
        alg = "Genetic Algorithm"
        
    
    signatures_long["wavelength"] = pandas.to_numeric(signatures_long["wavelength"])
    # signatures_long["value"] = pandas.to_numeric(signatures_long["value"])
    
    y_max = signatures_long["value"].max()
    
    graph_signatures = ggplot(signatures_long) \
        + theme(legend_position = "none") \
        + aes(x = "wavelength", y = "value", color = "variable") \
        + labs(
            x = "Wavelength (nm)",
            y = "Reflectance (%)",
            title = f"Ranges in signature: {target} {hydro_state} {alg}, {year}.",
            subtitle = f"{alg}, {hydro_state} set."
            ) 
    
    if ranges is not None:
        for i in range(len(ranges)):
            i_range = []
            for j in range(len(ranges[i])):
                # graph_signatures = graph_signatures + geom_vline(xintercept = ranges[i][j], color="black", alpha = 0.2) 
                i_range.append(ranges[i][j])
            graph_signatures = graph_signatures + geom_rect(aes(xmin = i_range[0], xmax = i_range[1], ymin = 0.0, ymax = y_max), fill = "steelblue", alpha = 0.1, color = None)
        graph_signatures = graph_signatures + geom_line()
        
    else:
        graph_signatures = graph_signatures + geom_line()
    
    print(graph_signatures)
    graph_signatures.save(filename = os.path.join(PLOT_DIR, 
                                                  f"{hydro_state}-{year}-{algorithm}-ranges-{target}"))

    return 

def plot_rages(target, signatures, ranges, hydro_state, year, algorithm):
    with plt.style.context('ggplot'):
        xticks = np.arange(350, 2500)
        plt.plot(xticks, signatures.iloc[0:20 , 1: ].T)
        
        plt.xlabel('Wavelengths (nm)')
        # plt.xticks = xticks
        plt.ylabel("Reflectance (%)")
        plt.title('Spectral signatures')
        
        plt.show()
    return