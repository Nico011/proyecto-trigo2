# -*- coding: utf-8 -*-
import random
import pandas
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error


model_target = 0.5 # r2 target
length = 1 # number of the dataset col (will be changed in ga)()
population_number = 50
pressure = 5 # individuals selected to reproduction
mutation_chance = 0.2
generations = 25
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
    return [random.randint(min, max) for i in range(length)]

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
    print(f"len/cols:{len(cols)} / {cols}")
    
    r2 = regression(cols)
    if r2 >= model_target:
        fitness += 1
        
    return fitness

def selection_reproduction(population):
    # calculate fitness of every individual and save it as a pair
    print(f"largo pop: {len(population)}")
    print(f"pop: {population[0]}")
    scored = [(fitness_func(i), i) for i in population] # ex: (5, [1, 0, 0, 1, ...])
    print(f"largo scored1: {len(scored)}")
    print(f"largo del 1er elemento: {len(scored[0])}")
    print(f"scored1: {scored[0]}")
    scored = [i[1] for i in sorted(scored)]
    print(f"largo scored2: {len(scored)}")
    print(f"largo del 1er elemento: {len(scored[0])}")
    print(f"scored2: {scored[0]}")
    population = scored
    print(f"largo pop: {len(population)}")
    print(f"largo 1er el: {len(population[0])}")
    print(f"population: {population[0]}")
    
    # select 'n' las individuals, where n = pressure
    selected = scored[(len(scored) - pressure) : ] 
    print(f"largo selected: {len(selected)}")
    print(f"largo del 1er elemento: {len(selected[0])}")
    print(f"selected: {selected[0]}")
    
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
    
    print("length", length)
    
    print("creando poblacion")
    population = create_population()
    
    print("reproducción y mutación")
    for i in range(0, generations):
        population = selection_reproduction(population)
        population = mutation(population)
        
    print("fin ga()")
    return population























