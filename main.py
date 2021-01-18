import json
import pygame
from game import Game


if __name__ == "__main__":
    with open('settings/constants.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    game = Game(config)
    try:
        game.show_menu()
    except pygame.error:
        pass
    finally:
        config['best_score'] = int(game.best)
        with open('settings/constants.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
