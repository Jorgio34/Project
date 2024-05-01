import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CITY_RADIUS = 20
PLAYER_COLOR = (0, 255, 0)
OPPONENT_COLOR = (255, 0, 0)
CITY_COLOR = (100, 100, 100)
FONT_SIZE = 24

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Travel Game")

# Player attributes
player_money = 100
current_city = "Start City"

# City data (modify as needed)
cities = {
    "Start City": {"x": 100, "y": 300},
    "Mountain City": {"x": 300, "y": 100},
    "Lake City": {"x": 500, "y": 400},
    "Destination City": {"x": 700, "y": 200},
}

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw cities
    screen.fill((255, 255, 255))
    for city, pos in cities.items():
        pygame.draw.circle(screen, CITY_COLOR, (pos["x"], pos["y"]), CITY_RADIUS)
        pygame.draw.circle(screen, (0, 0, 0), (pos["x"], pos["y"]), CITY_RADIUS, 2)
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(city, True, (0, 0, 0))
        screen.blit(text, (pos["x"] - CITY_RADIUS, pos["y"] + CITY_RADIUS))

    # Draw player
    pygame.draw.circle(screen, PLAYER_COLOR, (cities[current_city]["x"], cities[current_city]["y"]), 10)

    # Update display
    pygame.display.flip()