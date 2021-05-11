# Identificación de rangos de longitud de onda relacionados a variables fisiológicas de trigo usando algoritmos de selección de atributos.


## Resumen
### Motivación
El trigo, junto al maíz, arroz y otros cereales, son la base alimenticia de la civilización y su cultivo se enfrenta a grandes problemas como: poder entregar un alto valor nutritivo, alcanzar en términos de cantidad para una población en constante crecimiento, disminuir el impacto ambiental que conlleva cumplir los requisitos mencionados. La selección de plantas en etapas tempranas de desarrollo para producción o cruce ahorraría bastante tiempo y recursos a los investigadores, por eso este trabajo busca encontrar indicadores para realizar dicha selección.   
Una firma espectral es la variación de reflectancia de un material respecto a la longitud de onda, es medida con un espectómetro y a través de esta firma es posible conocer la estructura y composición de dicho material, así que se usa en distintos campos de la ciencia. Este trabajo se enfoca en su uso en la agronomía, en específico, la medición de la firma espectral de la planta de trigo, ya que esta medición podría entregar información sobre la salud o fisiología de la planta [3].


### Objetivo general
Encontrar rangos de longitudes de onda en la firma espectral que describan características fisiológicas del trigo.


### Objetivo específico
Aplicar algoritmos de selección de atributos sobre la firma hiper-espectral para encontrar longitudes de onda que caractericen variables fisiológicas para optimización de la lectura de la firma.


### Hipótesis preliminar
¿Es posible identificar rangos de longitud de onda de la firma hiper-espectral que permitan estimar variables fisiológicas del trigo utilizando algoritmos de selección de atributos?


### Datos
Los datos para este proyecto contienen observaciones fisiológicas, de fluorescencia de la clorofila y firma hiper-espectral de distintos genotipos de trigo, en distintas etapas de madurez, condición de riego y lugar geográfico, las que fueron tomadas entre los años 2014 y 2017 [1]. Los métodos de obtención de los datos varían entre mediciones de campo o en laboratorio. Para el caso de la firma hiper-espectral se decidió usar las medidas tomadas con reflectómetro de clip, que mide la reflectancia entre 350 a 2500nm directamente desde la hoja y no percibe ruido.    
Los datos se encuentran en el archivo **data-total.csv**. Este archivo combina las medidas tomadas los cuatro años antes mencionados, de ambas localidades (Cauquenes y Santa Rosa). De las columnas se pueden separar en cuatro grupos: el primero contiene datos sobre la medición (ID, fecha, condición de riego, parcela, etc); un segundo grupo con las variables fisiológicas de cada medición (clorofila, flavonoides, conductancia estomática, etc.); un tercer grupo con meddiciones de fluorescencia de la clorfila; y por último, las columnas que contienen las medidas de reflectancia donde cada columna es una longitud de onda desde 350 a 2500nm. Dando un total de 2197 columnas y 1579 observaciones.    
Para este se consideran los grupos de variables fisiológicas y medidas de reflectancia como variables objetivos y predictores respectivamente. En caso de existir datos faltantes se elimina la fila.

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


### Métodos
El método de preprocesamiento consta de filtrar los datos, sepárandolos por año y por estado hídrico (irrigación completa o control y secano o estrés hídrico) y se estandarizan las columnas predictoras calculando los z-scores.

Ejemplo de dataframe luego de filtrar para el año 2014, grupo control, estandarizada y cuya variable objetivo es Chl (clorofila):

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
Por falta de datos, se eliminó la columna para la longitud de onda 2500.   
Las posibles variables objetivo son: Chl, Flav, Anth, NBI, Pot.Hoja(Bar), Transmitted, LAI, EVAP, GS, PN, CI y VPD.   
Se implementaron distintos algoritmos de selección de atributos para seleccionar longitudes de onda importantes, con el objetivo de reducir la dimensionalidad del problema, entender mejor los datos, reducir los requisitos de cómputo y mejorar el rendimiento de los predictores [2], los que se listan a continuación:
* Algoritmo Boruta.
* Least absolute shrinkage and selection operator (LASSO).
* SelectkBest.
* Algoritmo genético.   

La lista de atributos considerados como importantes por estos algoritmos se entregan como parámetro a una función de clusterización jerárquico aglomerativo que los agrupa según su distancia, y luego obteniendo el mínimo y máximo de cada clúster retorna una lista con los rangos de longitudes de onda que caracterízarían a la variable entregada como objetivo.    
Los métodos de regresión son:
* PLS.
* SVR.
* Regresión logística.
* Ridge.   

(Falta unidades de medición y validación)


### Resultados esperados
Se espera que los distintos algoritmos usados entreguen rangos similares para las mismas variables fisiológicas, estos rangos funcionarían como indicadores característicos y ayudarían a optimizar la lectura de la firma hiper-espectral.


### Resultados específicos


## El programa en Python
### Los algoritmos de selección de atributos
Se han implementado 4 algoritmos de selección de atributos, divididos en distintos archivos. A continuación se listan los módulos y los algoritmos que contiene cada uno:
* my_boruta.py: Algoritmo Boruta.
* lasso.py: Algoritmo Least absolute shrinkage and selection operator (LASSO).
* kbest.py: Algoritmo Select K-Best, utilizando dos funciones de score,
  * Mutual information: Función kbest_mi().
  * Correlation: Función kbest_corr().
* ga.py: Algoritmo genético para selección de atributos.

### Uso
Abrir el archivo `main.py` desde la terminal y entregar los parámetros:

```main.py -t <target> [-a <algoritmo> -y <año>]```

En caso de especificar un algorito es necesario especificar un año, en caso contrario se ejecutarán todos los algoritmos para todos los años. Se puede no especificar el target y tomará la clorofila (Chl) por default.

Targets disponibles: Chl, Flav, Anth, NBI, Pot.Hoja(Bar), Transmitted, LAI, EVAP, GS, PN, CI, VPD.

Algoritmos disponibles: 
* boruta: Ejecuta algoritmo Boruta.
* lasso: Ejecuta algoritmo LASSO
* kbestcorr: Ejecuta algoritmo SelectkBest usando correlación.
* kbestmi: Ejecuta algoritmo SelectkBest usando información mutua.

Años disponibles: 2014, 2015, 2016 y 2017.

Puede usar el comando `-h` o `--help` para obtener una ayuda similar a la descripción anterior.

Ej: `main.py --help`

[1]: https://www.mdpi.com/1424-8220/19/12/2676?type=check_update&version=2 'S. Romero-Bravo et al., “Thermal Imaginig Reliability for Estimating Grain Yield and Carbon Isotope Discrimination in Wheat Genotypes: Importance of the Enviromental Conditions,” pp. 1–16.'
[2]: https://www.sciencedirect.com/science/article/abs/pii/S0045790613003066?via%3Dihub 'G. Chandrashekar and F. Sahin, “A survey on feature selection methods,” Comput. Electr. Eng., vol. 40, no. 1, pp. 16–28, 2014, doi: 10.1016/j.compeleceng.2013.11.024.'