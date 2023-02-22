import json
import os

from pizza_vs_cats.config import decks_folder
from pizza_vs_cats.deck.collect_votes import evaluation_loop

if __name__ == "__main__":
    deck_path = os.path.join(decks_folder, 'test.json')
    deck = json.load(open(deck_path, 'r'))

    evaluation_loop(deck)

    out_path = os.path.join(decks_folder, 'test_with_new_votes.json')
    with open(out_path, 'w') as out_file:
        json.dump(deck, out_file, indent=4)
