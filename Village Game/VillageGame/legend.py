# legend.py
import pygame

legend_data = {
    'H': ('House', (255, 0, 0)),
    'T': ('Tree', (0, 255, 0)),
}

def render_legend(screen, legend_data, cell_size):
    legend_x, legend_y = 10, 10
    for symbol, (name, color) in legend_data.items():
        pygame.draw.rect(screen, color, pygame.Rect(legend_x, legend_y, cell_size, cell_size))
        font = pygame.font.Font(None, 36)
        legend_text = font.render(f"{symbol}: {name}", True, (255, 255, 255))
        screen.blit(legend_text, (legend_x + cell_size + 5, legend_y))
        legend_y += cell_size + 5

    legend_x += 5
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(legend_x, legend_y, cell_size, cell_size))
    legend_text = font.render("Player", True, (255, 255, 255))
    screen.blit(legend_text, (legend_x + cell_size + 5, legend_y))
