"""
pygame 2048
-----------
This script is loading a constants from a setting's json and then it is launching
a game using Game class. After game is shut down if best score was beaten it saves new best
back to setting's json
Run
---
>>> python main.py
"""

import json
import pygame
from game import Game


if __name__ == "__main__":
    with open('settings/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    game = Game(config)
    try:
        game.show_menu()
    except pygame.error as pygame_error:
        print(str(pygame_error))
    finally:
        config['best_score'] = int(game.best_score)
        with open('settings/config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
