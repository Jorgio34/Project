import random
from lab11.turn_combat import CombatPlayer

class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        # For example, randomly choosing a city number
        return ord(str(random.randint(0, 9)))  # Assumes there are 10 cities

class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        # For example, randomly choosing a weapon
        self.weapon = random.choice([0, 1, 2])  # Assumes there are 3 weapon types
        return self.weapon