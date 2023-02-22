import json
import os

from pizza_vs_cats.config import decks_folder
from pizza_vs_cats.game.game import Game

if __name__ == "__main__":
    deck_path = os.path.join(decks_folder, "test.json")
    deck = json.load(open(deck_path))
    game = Game(['a', 'b'], deck, 3)

    game.game_loop()
