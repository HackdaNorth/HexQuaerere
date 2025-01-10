import pygame
import clock
import random

pygame.init()

#set variables for harvesting
harvesting = False
harvest_start_time = 0
wood_total = 0
wood_gathered = 0
treeHarvestTime = 1000 #in milliseconds

#Mill building variables
storing_start_time = 0
storing = False
storageMax = False

storeWoodTime = 3000 # in milliseconds

#change how much wood needed for spawning houses
spawnTrees_woodNeeded = 4

#change amount of Trees to spawn
spawnTreesStart = 5
spawnTreesEnd = 6

#change houses group spawn
spawnHousesStart = 5
spawnHousesEnd = 13

#Set your grid size and cell size
grid_width = 150
grid_height = 150
cell_size = 8

#Spawn Variables
group_x=0
group_y=0
num_houses = 5
num_trees = 20

# Define player
player_size = 2  # Double the size of the trees



# Create a clock to measure time
clock = pygame.time.Clock()

# Create the game window
screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size))
pygame.display.set_caption("AI Village Game")

# Set the game clock
clock = pygame.time.Clock()

#define grid
def create_grid():
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
    return grid
#create the grid and store it
grid = create_grid()


#dev-debug
# def display_grid_to_console():
#     for row in grid:
#         print(" ".join(row))


def generate_houses():
    global group_x, group_y
    # Generate a group of 4-5 houses grouped together
    group_size = random.randint(spawnHousesStart, spawnHousesEnd)
    group_x = random.randint(0, grid_width - group_size)
    group_y = random.randint(0, grid_height - 1)
        
    for _ in range(group_size):
        x = group_x + random.randint(3, 5)
        y = group_y + random.randint(2, 7)

        if 0 <= x < grid_width and 0 <= y < grid_height:
            grid[y][x] = 'H'  # 'H' represents a house
            group_x += 1

    # Generate the remaining houses and scatter them randomly
    for _ in range(num_houses - group_size):
        x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
        if grid[y][x] != 'H':
            grid[y][x] = 'H'  # 'H' represents a house
    
def generate_mills():
    global group_x, group_y

    mill_group = 1

    # Generate mill (3x3 grid of "M")
    for _ in range(mill_group):
        for i in range(3):
            for j in range(3):
                x = group_x + i
                y = group_y + j
                if 0 <= x < grid_width and 0 <= y < grid_height and grid[y][x] != 'H':
                    grid[y][x] = 'M'  # 'M' represents a mill
                    
def generate_trees():
    # Generate the trees randomly
    for _ in range(num_trees):
        x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
        if grid[y][x] != 'H':
            grid[y][x] = 'T'  # 'T' represents a tree
            
def respawn_trees():
    global wood_total
    num_trees_spawned = random.randint(spawnTreesStart, spawnTreesEnd) 
    print("Spawned: " + str(num_trees_spawned))
    if wood_total == spawnTrees_woodNeeded: 
        for _ in range(num_trees_spawned):
            x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
            if grid[y][x] != 'H':
                grid[y][x] = 'T'  # 'T' represents a tree
                
                draw_grid(screen, legend_data, cell_size)

generate_houses()

generate_mills()

generate_trees()


player_x, player_y = group_x + 3, group_y + 3  # Starting position

# Legend data
legend_data = {
    'H': ('House', (255, 0, 0)),
    'T': ('Tree', (0, 255, 0)),
}

def checkCollision():
    global player_x, player_y, player_size

    mill_collision = False
    tree_collision = False
    house_collision = False

    # Define the proximity area around the player
    proximity_area = 1  # Adjust this value as needed

    for dx in range(-proximity_area, player_size + proximity_area):
        for dy in range(-proximity_area, player_size + proximity_area):
            cell_x = player_x + dx
            cell_y = player_y + dy

            if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height:
                if grid[cell_y][cell_x] == 'T':
                    tree_collision = True
                elif grid[cell_y][cell_x] == 'H':
                    house_collision = True
                elif grid[cell_y][cell_x] == 'M':
                    mill_collision = True

    if tree_collision:
        harvest_tree(player_x, player_y)
        # If there's a tree collision at the player's position, handle it (e.g., call the harvest_tree function)
        return tree_collision
    elif house_collision:
        # If there's a house collision, you can handle it differently
        # For example, print a message or decrease the player's score
        return house_collision
    elif mill_collision:
        global wood_gathered
        store_wood()
        
        #fix wood being added twice every time we sit beside it for 4000 seconds.
        
def store_wood():
    global wood_total, storing, storing_start_time, storageMax, wood_gathered
    if wood_gathered < 0:
        #do something if we have no wood.
        pass
    elif wood_gathered > 0:
        if not storing:
            # If harvesting is not in progress, check if the player is touching a tree on their edges
            for dx in range(-1, player_size + 1):
                for dy in range(-1, player_size + 1):
                    cell_x = player_x + dx
                    cell_y = player_y + dy
                    if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height and grid[cell_y][cell_x] == 'M':
                        storing = True
                        storing_start_time = pygame.time.get_ticks()

        elif pygame.time.get_ticks() - storing_start_time >= storeWoodTime:
            # After the 10-second delay, remove the tree that the player was touching
            for dx in range(-1, player_size + 1):
                for dy in range(-1, player_size + 1):
                    cell_x = player_x + dx
                    cell_y = player_y + dy
                    if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height and grid[cell_y][cell_x] == 'M':
                        wood_total += wood_gathered
                        wood_gathered = 0
                        respawn_trees() #call respawn trees once we deposit, maybe we have enough wood
                        storing_start_time = pygame.time.get_ticks()
                        return wood_gathered

def harvest_tree(player_x, player_y):
    global harvesting, harvest_start_time, wood_gathered

    if not harvesting:
        # If harvesting is not in progress, check if the player is touching a tree on their edges
        for dx in range(-1, player_size + 1):
            for dy in range(-1, player_size + 1):
                cell_x = player_x + dx
                cell_y = player_y + dy
                if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height and grid[cell_y][cell_x] == 'T':
                    harvesting = True
                    harvest_start_time = pygame.time.get_ticks()

    elif pygame.time.get_ticks() - harvest_start_time >= treeHarvestTime:
        # After the 10-second delay, remove the tree that the player was touching
        for dx in range(-1, player_size + 1):
            for dy in range(-1, player_size + 1):
                cell_x = player_x + dx
                cell_y = player_y + dy
                if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height and grid[cell_y][cell_x] == 'T':
                    grid[cell_y][cell_x] = ' '
                    wood_gathered += 2
                    harvest_start_time = pygame.time.get_ticks()

        draw_grid(screen, legend_data, cell_size)
        harvesting = False

def update_player(keys):
    global player_x, player_y, player_size

    dx, dy = 0, 0

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy = 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx = 1

    # Check all cells in the player square for collisions
    collision_detected = False
    for i in range(player_size):
        for j in range(player_size):
            cell_x = player_x + dx + i
            cell_y = player_y + dy + j

            if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height and grid[cell_y][cell_x] in ('H', 'T', 'M'):
                # If there's a collision with a house ('H') or tree ('T'), set a flag
                collision_detected = True
                break

    if not collision_detected:
        # If no collisions, update the player's position
        player_x += dx
        player_y += dy
    return player_x, player_y

def draw_player():
    # Draw the player
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_x * cell_size, player_y * cell_size, player_size * cell_size, player_size * cell_size))
    
def draw_mill():
    mill_color = (112, 73, 29)
    mill_size = 1.8  # Adjust this value to match the size of the 'M' grid
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == 'M':
                mill_x = x * cell_size - (mill_size - 1) * cell_size / 2
                mill_y = y * cell_size - (mill_size - 1) * cell_size / 2
                pygame.draw.rect(screen, mill_color, pygame.Rect(mill_x, mill_y, mill_size * cell_size, mill_size * cell_size))

def draw_legend(legend_data):
    # Draw the legend
    legend_x, legend_y = 10, 10
    for symbol, (name, color) in legend_data.items():
        pygame.draw.rect(screen, color, pygame.Rect(legend_x, legend_y, cell_size, cell_size))
        font = pygame.font.Font(None, 36)
        legend_text = font.render(f"{symbol}: {name}", True, (255, 255, 255))
        screen.blit(legend_text, (legend_x + cell_size + 5, legend_y))
        legend_y += cell_size + 5
        
    # Add player icon to the legend
    legend_x += 5
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(legend_x, legend_y, cell_size, cell_size))
    legend_text = font.render("Player", True, (255, 255, 255))
    screen.blit(legend_text, (legend_x + cell_size + 5, legend_y))

def draw_grid(screen, legend_data, cell_size):
        # Redraw the grid and player
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] in legend_data:
                # Get the cell data and draw a colored rectangle
                name, color = legend_data[grid[y][x]]
                pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
                
    draw_mill()
    
    draw_player()
    
    #draw_legend(legend_data)

# Initialize the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    # Player movement controls
    update_player(keys)
        
    checkCollision()

    draw_legend(legend_data)

    # Clear the screen
    screen.fill((0, 0, 0))

    draw_grid(screen, legend_data, cell_size)

    pygame.display.flip()
    


    clock.tick(30)
    
pygame.quit()
