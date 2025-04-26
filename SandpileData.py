import numpy as np
from scipy.ndimage import convolve
import time

# Znalezienie niestabilnych pozycji i rozsypanie 
def iterate(grid):
    unstable = grid > 3
    topple_count = np.sum(unstable)
    if topple_count == 0:
        return grid, False, 0
    kernel = np.array([[0, 1, 0],
                       [1, 0, 1],
                       [0, 1, 0]])
    grid[unstable] -= 4
    grid += convolve(unstable.astype(int), kernel, mode='constant', cval=0)
    return grid, True, topple_count

# Inicjalizacja siatki
def init(size):
    grid = np.zeros((size, size), dtype=int)
    N = size * size *3
    for i in range(N):  # Początkowe dodanie N ziaren 
        x = np.random.randint(0, size - 1)
        y = np.random.randint(0, size - 1)
        grid[x, y] += 1
        percent = (i + 1) / N * 100
        print(f"\rPostęp początkowego zapełniania siatki {size}x{size}: {percent:.1f}%", end="", flush=True)
    print("\n")
    return grid

# Uaktualnianie siatki, obliczanie rozmiarów lawiny
def update(grid, total_topples, size, data):
    grid, changed, topple_count = iterate(grid)

    if changed:
        total_topples += topple_count
    else:
        if total_topples > 0:
            data.append(total_topples) 
            total_topples = 0
        for _ in range(1): 
            x = np.random.randint(0, size - 1)
            y = np.random.randint(0, size - 1)
            grid[x, y] += 1
    return grid, total_topples, data

# Główna funkcja, iteruje po rozmiarze siatki i zapisuje wartości lawin
def sim(start, end, Npoints):
    filenames = []
    data = []
    total_topples = 0
    log_points = np.logspace(np.log10(start), np.log10(end), Npoints)
    sizes = [int(size) for size in log_points]
    for j in range(Npoints):
        start_time = time.time()
        grid = init(sizes[j])
        pointstogrid = sizes[j]*sizes[j]*4*20
        for i in range(pointstogrid):
            grid, total_topples, data = update(grid, total_topples, sizes[j], data)
            percent = (i + 1) / pointstogrid * 100
            print(f"\rPostęp symulacji dla siatki {sizes[j]}x{sizes[j]}: {percent:.2f}%", end="", flush=True)
        print("\n")
        f = open(f"SandpileData_size{sizes[j]}x{sizes[j]}.txt", "w")
        filenames.append(f"SandpileData_size{sizes[j]}x{sizes[j]}.txt")
        f.write("\n".join(map(str, data)))
        f.close()
        data.clear()
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"Czas działania dla siatki {sizes[j]}x{sizes[j]}: {minutes} min {seconds} s\n")
    return filenames, sizes

