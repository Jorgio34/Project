import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_routes

from lab3.travel_cost import get_route_cost

pygame.init()

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)

player_currency = 0
journal_entry = "\n"


def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))

        screen.blit(text_surface, city_locations[i])

def get_randomly_spread_cities(size, num_cities):
    cities = []
    for _ in range(num_cities):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        cities.append((x, y))
    return cities

def calculate_travel_cost(city1, city2):
    # Assume elevation data for each city 
    elevation_city1 = 100  
    elevation_city2 = 150  

    # Calculate elevation difference
    elevation_difference = abs(elevation_city1 - elevation_city2)

    # Assume a fixed cost per unit elevation difference
    cost_per_meter = 0.1  
    # Calculate total travel cost
    total_distance = ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5
    travel_cost = elevation_difference * cost_per_meter * total_distance

    return travel_cost

# New function to generate a journal entry for a city
def generate_journal_entry(city_name):
    entry = f"🌆 **{city_name}**: A place where time dances with cobblestone streets. The scent of freshly baked bread mingles with whispers of forgotten legends. As I wander through narrow alleys, shadows cling to ancient walls, revealing secrets etched in stone. The locals, with eyes like constellations, share tales of lost love and hidden treasures. Tonight, I'll rest beneath a moon that knows every story ever told. 🌙✨"
    return entry

# Example usage:
city1 = (10, 20)  
city2 = (30, 40)  
cost = calculate_travel_cost(city1, city2)
print(f"Travel cost between cities: ${cost:.2f}")

# New function to check if a valid route exists between cities
def has_valid_route(city1, city2, routes):
    for route in routes:
        if city1 in route and city2 in route:
            return True
    return False

# Initialize player skill level (you can adjust this based on player performance)
player_skill_level = 1.0

# Define adaptive difficulty parameters
BASE_ENEMY_STRENGTH = 10
DIFFICULTY_SCALING_FACTOR = 0.2

# Function to adjust enemy strength based on player skill
def adjust_enemy_strength(player_skill_level):
    return BASE_ENEMY_STRENGTH + DIFFICULTY_SCALING_FACTOR * player_skill_level

# Function to generate personalized content (e.g., quest descriptions)
def generate_personalized_quest(player_name):
    return f"Hello, {player_name}! Your mission is to retrieve the ancient artifact from the {random.choice(['cursed', 'enchanted', 'forgotten'])} temple."

class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 1000, 720
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "Game World Gen")

    landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameAIPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    quest_description = generate_personalized_quest("Link")
    print(quest_description)

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        enemy_strength = adjust_enemy_strength(player_skill_level)

       


        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2

            if not state.travelling:
                print('Arrived at', state.destination_city)
                journal_entry = generate_journal_entry(city_names)
                print(journal_entry)



                

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                start = cities[state.current_city]
                destination_city = int(chr(action))
                destination = cities[destination_city]
            
            # Check if a valid route exists
            if has_valid_route(state.current_city, state.destination_city, routes):
                # Calculate travel cost based on elevation 
                travel_cost = calculate_travel_cost(start, state.destination_city)
                # Deduct travel cost from player's currency 
                player_currency -= travel_cost
                
                # Update state and player sprite
                ##state.destination_city = destination_city
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print( f"Travelling from {state.current_city} to {state.destination_city}")
            else:
                print("No valid route exists between cities. Cannot move.")

            pygame.display.update()



        if state.encounter_event:
            run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
        
        if state.current_city == end_city:
            if player_currency >= 0:
                print("Congratulations! You've reached the end city.")
            else:
                print("Game over. You ran out of money.")
            break

   

pygame.quit()