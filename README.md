# Identificación de rangos de longitud de onda relacionados a variables fisiológicas de trigo usando algoritmos de selección de atributos.

### Resumen
En este proyecto se utilizan algoritmos de selección de atributos para optimizar la lectura de firma espectral de plantas de trigo para alguna variable objetivo o **target**.
Los datos para este proyecto contienen observaciones fisiológicas, de fluorescencia de la clorofila y firma hiper-espectral de distintos genotipos de trigo, en distintas etapas de madurez, condición de riego y lugar geográfico, las que fueron tomadas entre los años 2014 y 2017. Los métodos de obtención de los datos varían entre mediciones de campo o en laboratorio. Para el caso de la firma hiper-espectral se decidió usar las medidas tomadas con reflectómetro de clip, que mide la reflectancia entre 350 a 2500nm, y además, mide directamente desde la hoja y no percibe ruido.


### Los datos
Los datos se encuentran en el archivo **data-total.csv**. Este archivo combina las medidas tomadas los cuatro años antes mencionados, de ambas localidades (Cauquenes y Santa Rosa). De las columnas se pueden separar en cuatro grupos: el primero contiene datos sobre la medición (ID, fecha, condición de riego, parcela, etc); un segundo grupo con las variables fisiológicas de cada medición (clorofila, flavonoides, conductancia estomática, etc.); un tercer grupo con meddiciones de fluorescencia de la clorfila; y por último, las columnas que contienen las medidas de reflectancia donde cada columna es una longitud de onda desde 350 a 2500nm. Dando un total de 2197 columnas y 1579 observaciones
Para este se consideran los grupos dos y tres como variables objetivos y predictores respectivamente. En caso de existir datos faltantes se elimina la fila.

Ejemplo de dataframe de los datos antes de filtrar:

```
                                Wavelength       FECHA  ANIO  ...  2498  2499  2500
0                                      NaN  24-11-2014  2014  ...  0.07  0.07  0.07
1                                      NaN  24-11-2014  2014  ...  0.06  0.06  0.06
2                                      NaN  24-11-2014  2014  ...  0.06  0.06  0.06
3                                      NaN  24-11-2014  2014  ...  0.06  0.06  0.06
4                                      NaN  24-11-2014  2014  ...  0.05  0.05  0.05
                                   ...         ...   ...  ...   ...   ...   ...
1574  FONT_16-11-2017_R4_Sec_CLIP00102.asd  16-11-2017  2017  ...  0.06  0.06  0.06
1575  FONT_16-11-2017_R4_Sec_CLIP00111.asd  16-11-2017  2017  ...  0.07  0.07  0.07
1576  FONT_16-11-2017_R4_Sec_CLIP00120.asd  16-11-2017  2017  ...  0.08  0.08  0.08
1577  FONT_16-11-2017_R4_Sec_CLIP00129.asd  16-11-2017  2017  ...  0.07  0.07  0.07
1578  FONT_16-11-2017_R4_Sec_CLIP00138.asd  16-11-2017  2017  ...  0.07  0.07  0.07

[1579 rows x 2197 columns]
```
Ejemplo de dataframe luego de filtrar:

```
       Chl       350       351  ...      2497      2498      2499
0    39.15  1.386952  1.500577  ... -0.189699 -0.183563 -0.181818
1    48.82  0.422116  0.515583  ... -0.903858 -0.895565 -0.909091
2    42.42 -0.542720 -0.469411  ... -0.903858 -0.895565 -0.909091
3    45.74 -0.542720 -0.469411  ... -0.903858 -0.895565 -0.909091
4    47.97 -0.542720 -0.469411  ... -1.618017 -1.607566 -1.636364
..     ...       ...       ...  ...       ...       ...       ...
123  17.29  1.386952  1.500577  ...  0.524461  0.528439  0.545455
124  34.54  0.422116  0.515583  ...  0.524461  0.528439  0.545455
125  14.71  1.386952  1.500577  ... -0.189699 -0.183563 -0.181818
126  39.69  1.386952  1.500577  ...  0.524461  0.528439  0.545455
127   5.08  0.422116  0.515583  ...  0.524461  0.528439  0.545455

[128 rows x 2151 columns]
```
Para este ejemplo, se muestran los datos del año 2014 de las plantas de riego. La variable objetivo en este caso es clorofila (Chl) y se han estandarizado los valores de las columnas predictoras (el valor estandarizado es dado por el resultado de `(x - u) / s`, donde `x` es el valor antes de estandarizar, `u` es el promedio y `s` la desviación estándar.


### Los algoritmos
Se han implementado 4 algoritmos de selección de atributos, divididos en distintos archivos. A continuación se listan los módulos y los algoritmos que contiene cada uno:
* my_boruta.py: Algoritmo Boruta.
* lasso.py: Algoritmo Least absolute shrinkage and selection operator (LASSO).
* kbest.py: Algoritmo Select K-Best, utilizando dos funciones de score,
  * Mutual information: Función kbest_mi().
  * Correlation: Función kbest_corr().


### Referencias
* S. Romero-Bravo et al., “Thermal Imaginig Reliability for Estimating Grain Yield and Carbon Isotope Discrimination in Wheat Genotypes: Importance of the Enviromental Conditions,” pp. 1–16.
* G. Chandrashekar and F. Sahin, “A survey on feature selection methods,” Comput. Electr. Eng., vol. 40, no. 1, pp. 16–28, 2014, doi: 10.1016/j.compeleceng.2013.11.024.
* J. Luo et al., “Evaluation of spectral indices and continuous wavelet analysis to quantify aphid infestation in wheat,” Precis. Agric., vol. 14, no. 2, pp. 151–161, 2013, doi: 10.1007/s11119-012-9283-4.
