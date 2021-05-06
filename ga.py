# -*- coding: utf-8 -*-
import random
import pandas

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


model_target = 0.3 # r2 target
length = 1 # number of the dataset col (will be changed in ga)()
population_number = 70
pressure = 10 # individuals selected to reproduction
mutation_chance = 0.33
generations = 200
X = pandas.DataFrame({'col': []}) # create empty dataframe (will be changed in ga())
y = pandas.DataFrame({'col': []}) # create empty dataframe (will be changed in ga())

def regression(individual):
    
    X_train, X_test, y_train, y_test = train_test_split(
        X.loc[ : , individual],
        y,
        train_size = 0.8,
        test_size = 0.2,
        random_state = 1234,
        shuffle = True
    )
    
    # Model
    model = LinearRegression()
    model.fit(X = X_train, y = y_train)
    
    predictions = model.predict(X = X_test)
    r2 = r2_score(y_test, predictions)
    
    return r2


# Create an individual
def individual(min, max):
    # ind = [random.randint(min, max) for i in range(length)]
    ind = []
    n1 = 0
    for i in range(length):
        r = random.random()
        if r >= 0.00 and r <= 0.05:
            ind.append(1)
            n1 += 1
        else:
            ind.append(0)
    # print(f"cantidad seleccionada: {n1}")
    return ind

# Create population of new individuals
def create_population():
    return [individual(0, 1) for i in range(population_number)]

# Caluculate fitness
# Adds 1 to the fitness if the results of regression is equal or better than model target
def fitness_func(individual):
    fitness = 0
    # create list with col names selected to regression
    cols = []
    for i in range(len(individual)):
        if individual[i] == 1:
            cols.append(str(i + 350)) 
    # print(f"len/cols:{len(cols)} / {cols}")
    
    r2 = regression(cols)
    # print(f"r2: {r2}")
    if r2 >= model_target:
        fitness += 1
        
    return fitness

def selection_reproduction(population):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).

        Por ultimo muta a los individuos.

    """
    # calculate fitness of every individual and save it as a pair
    # print(f"largo pop: {len(population)}")
    # print(f"pop: {population[0]}")
    
    scored = [(fitness_func(i), i) for i in population] # ex: (5, [1, 0, 0, 1, ...])
    
    # print(f"largo scored1: {len(scored)}")
    # print(f"largo del 1er elemento: {len(scored[0])}")
    # print(f"scored1 last: {scored[-1]}")
    
    # ordena en forma ascendente según su valor de fitness y se queda solo 
    # con los individuos
    scored = [i[1] for i in sorted(scored)]
    
    # print(f"largo scored2: {len(scored)}")
    # print(f"largo del 1er elemento: {len(scored[0])}")
    # print(f"scored2: {scored[0]}")
    
    # population pasa a ser una lista de individuos donde lo que tienen
    # mayor valor de fitness quedan al final
    population = scored 
    
    # print(f"largo pop: {len(population)}")
    # print(f"largo 1er el: {len(population[0])}")
    # print(f"population: {population[0]}")
    
    # select 'n' last individuals, where n = pressure
    selected = scored[(len(scored) - pressure) : ] 
    # print(f"largo selected: {len(selected)}")
    # print(f"largo del 1er elemento: {len(selected[0])}")
    # print(f"selected: {selected[0]}")
    
    # crossover
    for i in range(len(population) - pressure):
        where = random.randint(1, length - 1)
        parents = random.sample(selected, 2) # select 2 parents
        
        population[i][ : where] = parents[0][ : where]
        population[i][where : ] = parents[1][where : ]
    
    return population

def mutation(population):
    
    for i in range(len(population) - pressure):
        if random.random() <= mutation_chance:
            where = random.randint(0, length - 1)
            new_value = random.randint(0, 1)
            
            # new value must be != old value
            while new_value == population[i][where]:
                new_value = random.randint(0, 1)
                
            population[i][where] = new_value
        
    return population

# main function
def ga(target, dataset):
    global X
    X = dataset.loc[ : , "350":"2499"]
    
    global y
    y = dataset.loc[ : , target]
    
    global length
    length = len(X.columns)
    
    population = create_population()
    
    for i in range(0, generations):
        # print(f"generación {i+1}")
        population = selection_reproduction(population)
        population = mutation(population)
        
    # print(f"pop: {population[-1]}")
    # print("fin ga()")
    # retorna el último individuo de la población, que es el que debería
    # tener mayor valor de fitness, convertido en lista de atributos elegidos
    best_ind = population[-1]
    selected = []
    for i in range(len(best_ind)):
        if best_ind[i] == 1:
            selected.append(i + 350)
    
    return selected























