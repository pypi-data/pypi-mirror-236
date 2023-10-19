import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
import random
import sys

def initialize_grid(x,y):
    grid = np.random.choice([0, 1], size=(x,y), p=[0.3, 0.7])
    return grid

def get_neighbour_count(grid, i, j):
    neighbours = [(i-1, j-1), (i-1, j), (i-1, j+1),
                  (i, j-1),             (i, j+1),
                  (i+1, j-1), (i+1, j), (i+1, j+1)]

    count = 0
    for x, y in neighbours:
        if x >= 0 and x < grid.shape[0] and y >= 0 and y < grid.shape[1]:
            count += grid[x, y]

    return count

def update_grid(grid):
    new_grid = grid.copy()

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbour_count = get_neighbour_count(grid, i, j)

            if grid[i, j] == 1:
                if neighbour_count < 2 or neighbour_count > 3:
                    new_grid[i, j] = 0
            else:
                if neighbour_count == 3:
                    new_grid[i, j] = 1

    return new_grid

def plot_grid(grid,i):
    plt.imshow(grid, cmap='cubehelix')
    plt.axis('off')
    plt.savefig(f'temp/temp{i}.png', bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

# 设置网格大小和迭代次数
grid_size = 30
iterations = 75

# 初始化网格
grid = initialize_grid(100,100)

# 创建空白图像列表
images = []

def main(x,y,seed,worldNumber,number):
    iterations = number

    # 初始化网格
    grid = initialize_grid(x,y)

    # 创建空白图像列表
    images = []
    for iss in range(0,worldNumber):
        if seed == "None":
            seeds = random.randint(0,4294967295)
        else:
            seeds = seed
        np.random.seed(seeds)
        os.makedirs("temp",exist_ok=True)
        # 迭代更新并绘制网格
        for i in range(iterations):
            print(f"第{iss}张动图的第{i+1}张图片")
            plot_grid(grid,i)
            image = Image.open(f'./temp/temp{i}.png')
            images.append(image)
            grid = update_grid(grid)

        # 保存为GIF动图
        images[0].save(f'./out/life_game_{iss}.gif', format='GIF', append_images=images[1:], save_all=True, duration=300, loop=1)
        f = open(f"./out/life_game_{iss}.txt","w",encoding="utf-8")
        f.write(f"随机数种子：{seed}")
        f.close()
        shutil.rmtree("temp")