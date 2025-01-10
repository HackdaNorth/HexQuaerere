# grid.py
import pygame
import random


grid_width = 128
grid_height = 128


# Legend data
legend_data = {
    'H': ('House', (255, 0, 0)),
    'T': ('Tree', (0, 255, 0)),
}


grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

player_x, player_y = grid_width // 2, grid_height // 2  # Starting position

num_houses = 5
num_trees = 20

def create_grid():
    global grid
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

def generate_random_objects():
    # Generate a group of 4-5 houses grouped together
    group_size = random.randint(4, 8)
    group_x, group_y = random.randint(0, grid_width - group_size), random.randint(0, grid_height - 1)
    for _ in range(group_size):
        grid[group_y + random.randint(2,7)][group_x + random.randint(3,5)] = 'H'  # 'H' represents a house
        group_x += 1

    # Generate the remaining houses and scatter them randomly
    # for _ in range(num_houses - group_size):
    #     x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
    #     if grid[y][x] != 'H':
    #         grid[y][x] = 'H'  # 'H' represents a house

    # Generate the trees randomly
    for _ in range(num_trees):
        x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
        if grid[y][x] != 'H':
            grid[y][x] = 'T'  # 'T' represents a tree


# Modify the update_player function to use the collision check
def update_player(keys):
    global player_x, player_y

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if player_y > 0:
            player_y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if player_y < grid_height - 1:
            player_y += 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x < grid_width - 1 :
            player_x += 1

    return player_x, player_y

def draw_grid(screen, legend_data ,cell_size): 
    # Redraw the grid and player
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] in legend_data:
                # Get the cell data and draw a colored rectangle
                name,color = legend_data[grid[y][x]]
                pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

def draw_player(screen, cell_size):
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_x * cell_size, player_y * cell_size, cell_size * 2, cell_size * 2))

def checkCollision():
    global player_x, player_y
    if grid[player_y][player_x] == 'T' or grid[player_y + 1][player_x] == 'T' or grid[player_y][player_x + 1] == 'T' or grid[player_y + 1][player_x + 1] == 'T':   
        # If there's a tree at the player's position, reset the player's position
     
        
        return True  # Collision detected
    return False  # No collision