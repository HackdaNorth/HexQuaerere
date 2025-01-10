import pygame
import grid
import legend

def main():
    pygame.init()


    grid_width = 128
    grid_height = 128
    cell_size = 8

    screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size))
    pygame.display.set_caption("AI Village Game")

    grid.create_grid()
    grid.generate_random_objects()
    legend_data = legend.legend_data

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        grid.update_player(keys)
        
        grid.checkCollision()

        screen.fill((0, 0, 0))

        grid.draw_grid(screen, legend_data, cell_size)
        grid.draw_player(screen, cell_size)
        
        legend.render_legend(screen, legend_data, cell_size)
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
