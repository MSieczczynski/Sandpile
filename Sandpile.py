import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
from scipy.ndimage import convolve

total_topples = 0

def iterate(grid, change_mask):
    unstable = grid > 3
    topple_count = np.sum(unstable)
    if topple_count == 0:
        return grid, False, change_mask, 0
    grid[unstable] -= 4
    kernel = np.array([[0, 1, 0],
                       [1, 0, 1],
                       [0, 1, 0]])
    grid += convolve(unstable.astype(int), kernel, mode='constant', cval=0)
    new_mask = convolve(unstable.astype(int), kernel, mode='constant', cval=0)
    new_mask = np.clip(new_mask, 0, 1)
    new_mask = new_mask.astype(float)
    change_mask = np.maximum(change_mask - 0.5, new_mask)

    return grid, True, change_mask, topple_count


def update(frame):
    global grid, change_mask, total_topples
    # Ewolucja sandpile
    grid, changed, change_mask, topple_count = iterate(grid, change_mask)
    if changed:
        time.sleep(0.1)
        total_topples += topple_count
    else:
        if total_topples > 20:
            print(f"Avalanche size: {total_topples}") 
        total_topples = 0
        for _ in range(1):  #Dodawanie x ziaren na klatke
            x = np.random.randint(0, size - 1)
            y = np.random.randint(0, size - 1)
            grid[x, y] += 1
    # Obraz RGB
    color_grid = np.zeros((size, size, 3))
    color_grid[..., 0] = (change_mask > 0).astype(float)
    mask_stable = (grid <= 3)
    color_grid[..., 1] = mask_stable * (grid / 3)
    color_grid[..., 2] = mask_stable * (grid / 3)
    im.set_array(color_grid)
    
    return [im]

# Inicjalizacja siatki
size = 100
grid = np.zeros((size, size), dtype=int)
for _ in range(20000):  # Dodawanie x ziaren do siatki
    x = np.random.randint(0, size - 1)
    y = np.random.randint(0, size - 1)
    grid[x, y] += 1
change_mask = np.zeros((size, size), dtype=int)  # Maska do kolorowania zsypywania

fig, ax = plt.subplots()
ax.set_title("Sandpile Simulation")

im = ax.imshow(np.zeros((size, size, 3)), interpolation='nearest')

# Stworznie animacji
ani = animation.FuncAnimation(fig, update, interval=1, repeat=True)

plt.show()