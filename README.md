# Identificación de rangos de longitud de onda relacionados a variables fisiológicas de trigo usando algoritmos de selección de atributos.

### Resumen
En este proyecto se utilizan algoritmos de selección de atributos para optimizar la lectura de firma espectral de plantas de trigo para alguna variable objetivo o **target**.
Los datos para este proyecto contienen observaciones fisiológicas, de fluorescencia de la clorofila y firma hiper-espectral de distintos genotipos de trigo, en distintas etapas de madurez, condición de riego y lugar geográfico, las que fueron tomadas entre los años 2014 y 2017. Los métodos de obtención de los datos varían entre mediciones de campo o en laboratorio. Para el caso de la firma hiper-espectral se decidió usar las medidas tomadas con reflectómetro de clip, que mide la reflectancia entre 350 a 2500nm, y además, mide directamente desde la hoja y no percibe ruido.


### Los datos
Los datos se encuentran en el archivo **data-total.csv**. Este archivo combina las medidas tomadas los cuatro años antes mencionados, de ambas localidades (Cauquenes y Santa Rosa)

### Los algoritmos
Se han implementado 4 algoritmos de selección de atributos, divididos en módulos. A continuación se listan los módulos y los algoritmos que contiene cada uno:
* my_boruta.py: Algoritmo Boruta.
* my_lasso.py: Algoritmo Least absolute shrinkage and selection operator (LASSO).
* my_kbest.py: Algoritmo Select K-Best, utilizando dos funciones de score,
  * Mutual information: Función kbest_mi().
  * Correlation: Función kbest_mi().
* my_ga.py: Algoritmo genético para selección de atributos.
