import random
import numpy as np
import pandas as pd


def create2dArray(rows, cols, probability):
    array = [[1 if random.random() < probability else 0 for _ in range(cols)] for _ in range(rows)]
    return array


def countOnes(array):
    count = 0
    for row in array:
        count += sum(row)
    return count


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


def checkPair(array):
    rows = len(array)
    cols = len(array[0])

    row_index = random.randint(0, rows - 1)
    col_index = random.randint(0, cols - 1)
    if array[row_index][col_index] == array[row_index][(col_index + 1) % cols] or \
            array[row_index][col_index] == array[(row_index + 1) % rows][col_index] or \
            array[row_index][col_index] == array[row_index][(col_index - 1) % cols] or \
            array[row_index][col_index] == array[(row_index - 1) % rows][col_index]:
        return row_index, col_index
    else:
        return False


rows = 50
cols = 50
probability = 0.5
test = create2dArray(rows, cols, probability)
test2 = create2dArrayBalanced(rows, cols, probability)
print(countOnes(test))
print(countOnes(test2), "\n")
# print(test2)

match = 0
cycles = 0
print("Pierwsze 10 zgodnych par.")

while match < 10:
    aa = checkPair(test2)
    if type(aa) is tuple:
        match += 1
        if aa[1] == 49:
            print(f"Pozycja pary: ({aa[0]}, {aa[1]}), ({aa[0]}, 0)")
        else:
            print(f"Pozycja pary: ({aa[0]}, {aa[1]}), ({aa[0]}, {aa[1] + 1})")
    cycles += 1

print("\nCykle wykonane:", cycles)

# np.set_printoptions(threshold=np.inf)
# print(np.matrix(test2))
df = pd.DataFrame(test2)
# print(df)
# print(df.to_string())
