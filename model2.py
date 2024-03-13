import random
import time

import numpy as np


def create2dArray(rows, cols, probability):
  array = [[1 if random.random() < probability else 0 for _ in range(cols)]
           for _ in range(rows)]
  return array


def proportions(array):
  rows = len(array)
  cols = len(array[0])
  total = rows * cols
  count = 0
  for row in array:
    for element in row:
      if element == 1:
        count += 1
  return round((count / total) * 100, 3)


def create2dArrayBalanced(rows, cols, probability):
  total_elements = rows * cols
  num_ones = int(total_elements * probability)
  num_zeros = total_elements - num_ones

  # rozrzuc 1'ki
  flat_array = [1] * num_ones + [0] * num_zeros
  random.shuffle(flat_array)

  # zamien w macierz
  array = [flat_array[i:i + cols] for i in range(0, total_elements, cols)]

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
  target = array[row_index][col_index]
  neighbours = ((0, 1), (0, -1), (1, 0), (-1, 0))
  pair = ((row_index, col_index), (next_row, next_col))

  for element in pair:
    row, col = element
    for neighbour in neighbours:
      new_row = (row + neighbour[0]) % rows
      new_col = (col + neighbour[1]) % cols

      array[new_row][new_col] = target


rows = 20
cols = 20
probability = 0.5
model = create2dArrayBalanced(rows, cols, probability)
displayModel(model)
print(proportions(model))
match = 0
cycles = 0
deadline = 0
print("\nPełna symulacja.\n")

timer_start = time.time()

while 0.1 <= proportions(model) <= 99.9:
  check = checkPair(model)

  if type(check) is tuple:
    match += 1
    proportion = proportions(model)

    print(f"Pozycja pary: ({check[0]}, {check[1]}), ({check[2]}, {check[3]})")
    changeOpinion(model, check[0], check[1], check[2], check[3])
    displayModel(model)

    print(f"Procent 1'ek: {proportions(model)}%\n")

    if proportion == proportions(model):
      deadline += 1
    else:
      deadline = 0

  timer_check = time.time() - timer_start
  cycles += 1

  if timer_check > 600:
    print("Mineło 10 minut")
    break

  if deadline == 100:
    print("100 cykli bez zmian")
    break

timer_end = time.time()
timer_result = round(timer_end - timer_start, 2)
print("\nWykonane cykle:", cycles, "w", timer_result, "sekund.")


