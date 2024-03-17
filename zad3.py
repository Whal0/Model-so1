import random
import time
import cProfile
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def create2dArray(rows, cols, probability):
  array = [[1 if random.random() < probability else 0 for _ in range(cols)]
           for _ in range(rows)]
  return array


def proportions22(array):
  rows = len(array)
  cols = len(array[0])
  total = rows * cols
  count = 0
  for row in array:
    for element in row:
      if element == 1:
        count += 1
  return round((count / total) * 100, 3)

def proportions(array):
    # ilosc jedynek
    count = np.count_nonzero(array == 1)
    
    # ilosc wszystkich elementow
    total = array.size
    
    #zaaokroglij do 2 miejsca po przecinku ( przy 400 elementach, zmiena jednego to 0.25%)
    proportion = round((count / total) * 100, 3)
    
    return proportion

def create2dArrayBalanced2(rows, cols, probability):
  total_elements = rows * cols
  num_ones = int(total_elements * probability)
  num_zeros = total_elements - num_ones

  # rozrzuc 1'ki
  flat_array = [1] * num_ones + [0] * num_zeros
  random.shuffle(flat_array)

  # zamien w macierz
  array = [flat_array[i:i + cols] for i in range(0, total_elements, cols)]

  return array

def create2dArrayBalanced(rows, cols, probability):
    
    # tworzenie macierza numpy array dla szybszych operacji
    total_elements = rows * cols
    num_ones = int(total_elements * probability)
    flat_array = np.concatenate((np.ones(num_ones, dtype=int), np.zeros(total_elements - num_ones, dtype=int)))

    # rozrzuc 1'nki
    np.random.shuffle(flat_array)

    # z listy do macierza
    array = flat_array.reshape((rows, cols))

    return array


def displayModel(model):
  rows = len(model)
  cols = len(model[0])
  result = ''
  for row in range(rows):
    for col in range(cols):
      result += f"{model[row][col]} "
    result += '\n'
  print(result)


def checkPair(array):
  rows = len(array)
  cols = len(array[0])

  offset_list = ((0, 1), (0, -1), (1, 0), (-1, 0))
  selected_offset = random.choice(offset_list)

  row_index = random.randint(0, rows - 1)
  col_index = random.randint(0, cols - 1)

  #print(f"{row_index},{col_index}: {array[row_index][col_index]}")
  #print(selected_offset)

  row_offset, col_offset = selected_offset
  next_row = (row_index + row_offset) % rows
  next_col = (col_index + col_offset) % cols

  pair = array[next_row][next_col]
  #print(f"{next_row},{next_col}: {array[next_row][next_col]}\n")

  if array[row_index][col_index] == pair:
    return row_index, col_index, next_row, next_col
  else:
    return False


def changeOpinion(array, row_index, col_index, next_row, next_col):
  
  rows = len(array)
  cols = len(array[0])
  target = array[row_index][col_index]
  neighbours = ((0, 1), (0, -1), (1, 0), (-1, 0))
  pair = ((row_index, col_index), (next_row, next_col))

  for element in pair:
    row, col = element
    for neighbour in neighbours:
      new_row = (row + neighbour[0]) % rows
      new_col = (col + neighbour[1]) % cols

      array[new_row][new_col] = target


def graphSimulation(cycleCount, proportions):
  x = list(range(cycleCount))
  plt.plot(x, proportions)
  plt.xlabel("Iteracje")
  plt.ylabel("Procent 1'ek")
  plt.title("Procent 1'ek w zależności od liczby iteracji")
  plt.show()
  plt.savefig('graph2.png')

def runSim(prob,cycles_per_sim, amount_of_sim):
  fin_prop = []
  for sim in range(amount_of_sim):
    # Zmienne symulacji
    rows = 20
    cols = 20
    probability = prob
    max_cycles = cycles_per_sim
    match = 0
    cycles = 1
    proportion_list = []

    model = create2dArrayBalanced(rows, cols, probability)
    #displayModel(model)
    #print(proportions(model))
    proportion_list.append(probability * 100)
    
    #print("\nPełna symulacja nr", sim+1,"\n")

    while 0.1 <= proportions(model) <= 99.9 and cycles != max_cycles:
      check = checkPair(model)

      if type(check) is tuple:
        match += 1

        #print(f"Pozycja pary: ({check[0]}, {check[1]}), ({check[2]}, {check[3]})")
        changeOpinion(model, check[0], check[1], check[2], check[3])
        #displayModel(model)

        #print(f"Procent 1'ek: {proportions(model)}%\n")

      cycles += 1
      proportion_list.append(proportions(model))

    #print("\nWykonane iteracje:", cycles)
    fin_prop.append(proportion_list[-1])
    print(proportion_list[-1],sim+1,"\n")

  mean = np.mean(fin_prop)
  sd = round(np.std(fin_prop),2)
  
  if os.path.exists("zad3_wyniki.txt"):
    with open("zad3_wyniki.txt", 'a', encoding="utf-8") as file:
        file.write(f"Prob: {prob}, Ilość symulacji: {amount_of_sim}, Średnia: {mean}, Odchylenie: {sd}" + '\n')
  else:
    with open("zad3_wyniki.txt", 'w', encoding="utf-8") as file:
        file.write(f"Prob: {prob}, Ilość symulacji: {amount_of_sim}, Średnia: {mean}, Odchylenie: {sd}" + '\n')


# time i pr do optymalizacji
#start = time.time()
# pr = cProfile.Profile()
# pr.enable()
        

runSim(0.1,1000,10)
runSim(0.25,10000,10)
runSim(0.5,10000,10)
runSim(0.75,10000,10)
runSim(0.9,1000,10)

# runSim(0.1,1000,10)
# runSim(0.25,1000,10)
# runSim(0.5,10000,10)
# runSim(0.75,1000,10)
# runSim(0.9,1000,10)

# runSim(0.1,1000,1000)
# runSim(0.25,1000,1000)
# runSim(0.5,10000,1000)
# runSim(0.75,1000,1000)
# runSim(0.9,1000,1000)


# pr.disable
# pr.print_stats()
#print(time.time() - start)